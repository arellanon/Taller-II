# -*- coding: UTF-8 -*-
import logging
import math
import os
import random
import socket

import communication
import indexer


class MasterNode(object):

    def __init__(self, host, port, mappers, reducer, outfile):
        self._mappers = mappers
        self._reducer = reducer
        self._host = host
        self._port = port
        self._outfile = outfile
        self._tcp_buffer_size = 4096
        self._backlog = 5
        self._reuseaddr = 1

    def start_job(self, filename):
        '''Procesa el archivo de texto filename y lo distribuye en los mappers.

        Divide el archivo en tareas que luego son enviadas a cada uno de los
        nodos mappers, y espera a recibir los resultados del reducer.
        '''
        job_id = random.randint(1, 65000)
        logging.info('Comenzando trabajo ID: %d', job_id)
        logging.debug('Calculando segmentos del fichero.')
        parts = self._split_file(filename, len(self._mappers))
        # informar al reducer del trabajo
        logging.info('Enviando el trabajo al reducer')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(tuple(self._reducer))
        conn = communication.CommunicationManager(sock)
        conn.send_job(job_id, len(parts))
        sock.close()

        fh = open(filename, 'r')
        for i in range(len(self._mappers)):
            id, byte_start, byte_end = parts[i]
            logging.info('Enviando tarea a %s:%d.' % self._mappers[i])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(tuple(self._mappers[i]))
            fh.seek(byte_start)
            conn_mapper = communication.CommunicationManager(sock)
            conn_mapper.send_task(
                id, fh.read(byte_end - byte_start))
            sock.close()
        fh.close()
        self._wait_for_results()
        logging.info('Finalizado el trabajo.')

    def _wait_for_results(self):
        '''Bloquea la ejecución esperando los resultados del reducer.

        Inicia el modo servidor para recibir los resultados procesados por
        el nodo reducer. Cuando ser reciben los resultados se escriben en
        el archivo configurado con el parámetro outfile.
        '''
        logging.info(
            'Iniciando la escucha en %s:%d', self._host, self._port)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, self._reuseaddr)
        server_socket.bind((self._host, self._port))
        server_socket.listen(self._backlog)
        logging.info('Esperando conexion')
        client_socket, client_addr = server_socket.accept()
        conn = communication.CommunicationManager(client_socket)
        results = conn.recv_results()
        fh = open(self._outfile, 'w')
        for i in results['index'].iteritems():
            fh.write('%s:%d\n' % i)
        fh.close()
        logging.debug(
            'Los resultados fueron escritos al archivo %s', self._outfile)
        client_socket.close()
        server_socket.close()

    def _split_file(self, filename, numparts):
        '''Divide el archivo en partes.

        Devuelve una lista de tuplas de la forma:
            (id, byte_start, byte_end)
            id es un número entero
            byte_start y byte_end son los offset de inicio y fin de
            la porción del archivo correspondiente
        '''

        fsize = os.path.getsize(filename)
        part_len = math.ceil(fsize / numparts)
        parts = []
        fh = open(filename, 'r')
        byte_start = 0
        for i in range(1, numparts):
            # si la división del texto no cae en un espacio en
            # blanco leo de a un carácter hasta encontrar espacio
            if i == numparts:
                fh.seek(0, 2)  # voy al final del archivo
                byte_end = fh.tell()
            else:
                fh.seek(i * part_len)
                while True:
                    ch = fh.read(1)
                    if ch.strip():
                        break
                # el byte_end tiene que ser uno menos porque el carácter que
                # se comprobó que no es espacio es el anterior
                byte_end = fh.tell() - 1
            parts.append((i, byte_start, byte_end))
            byte_start = byte_end
        parts.append((numparts, byte_start, fsize))
        fh.close()
        return parts


class MapperNode(object):

    def __init__(self, host, port, reducer):
        self._stopwsfile = 'stopwords.txt'
        self._host = host
        self._port = port
        self._reducer = reducer
        self._tcp_buffer_size = 4096
        self._backlog = 5
        self._reuseaddr = 1

    def start(self):
        'Inicia el nodo y queda a la espera de recibir una nueva tarea.'
        self._start_server()
        while True:
            logging.info('Esperando nueva tarea')
            self._run_task()
            logging.info('Finalizada la tarea.')

    def _start_server(self):
        'Inicializa el socket para recibir tareas.'
        logging.info(
            'Iniciando la escucha en %s:%d', self._host, self._port)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, self._reuseaddr)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(self._backlog)

    def stop(self):
        'Detiene la escucha del socket por nueva tareas.'
        self._server_socket.close()

    def _run_task(self):
        '''Espera a que se le envíe una tarea a procesar.

        Detiene la ejecución hasta recibir una tarea.
        Luego indexa la porción del texto perteneciente a la tarea.
        Al finalizar conecta con el reducer para envíar los resultados.
        '''
        logging.info('Esperando conexiones')
        client_socket, client_addr = self._server_socket.accept()
        conn = communication.CommunicationManager(client_socket)
        task = conn.recv_task()
        # cerrar sockets
        client_socket.close()
        # indexar la porción del texto recibida
        tokenizer = indexer.Tokenizer(self._stopwords(self._stopwsfile))
        index = indexer.Index(tokenizer)
        index.index_str(task['text'])
        # enviar los resultados
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(tuple(self._reducer))
        conn = communication.CommunicationManager(sock)
        conn.send_results(task['id'], index.dict())
        sock.close()

    def _stopwords(self, filename):
        'Devuelve una lista con stopwords en español.'
        fh = open(filename, 'r')
        stopw = fh.readlines()
        fh.close()
        return stopw


class ReducerNode(object):

    def __init__(self, host, port, master):
        self._host = host
        self._port = port
        self._master = master
        self._tcp_buffer_size = 4096
        self._backlog = 5
        self._reuseaddr = 1

    def _start_server(self):
        'Inicializa el socket para recibir tareas.'
        logging.info(
            'Iniciando la escucha en %s:%d', self._host, self._port)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, self._reuseaddr)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(self._backlog)

    def stop(self):
        'Detiene la escucha del socket por nueva tareas.'
        self._server_socket.close()

    def start(self):
        'Inicia el nodo y queda a la espera de recibir resultados.'
        self._start_server()
        while True:
            logging.info('Esperando conexiones')
            client_socket, client_addr = self._server_socket.accept()
            conn = communication.CommunicationManager(client_socket)
            # recibir el job
            job = conn.recv_job()
            logging.info('Esperando resultados de los mappers')
            tasks_completed = []
            self._index = {}
            while len(tasks_completed) < job['tasks']:
                mapper_socket, mapper_addr = self._server_socket.accept()
                conn_mapper = communication.CommunicationManager(mapper_socket)
                results = conn_mapper.recv_results()
                if tasks_completed.count(results['id']) > 0:
                    logging.info(
                        'Los resultados se ignorarán debido a que la '
                        'tarea con ID: %d ya se recibió anteriormente.',
                        results['id'])
                else:
                    self._update_index(results['index'])
                    tasks_completed.append(results['id'])
                    logging.info(
                        'Recibidos los resultados (%d/%d)',
                        len(tasks_completed), job['tasks'])
                mapper_socket.close()
            # cerrar sockets
            client_socket.close()
            logging.info('Enviando resultados globales al nodo master')
            # enviar los resultados
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(tuple(self._master))
            conn = communication.CommunicationManager(sock)
            conn.send_results(job['id'], self._index)
            sock.close()
            logging.info('Finalizado el trabajo.')

    def _update_index(self, results):
        'Hace un merge entre el índice global y results, sumando frecuencias.'
        for t, f in results.iteritems():
            self._index[t] = self._index.get(t, 0) + f
