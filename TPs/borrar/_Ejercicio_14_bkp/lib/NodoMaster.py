# -*- coding: UTF-8 -*-
import logging
import math
import os
import random
import socket
import indexer
from Mensaje import Mensaje
import ast

class NodoMaster():

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
#        job_id = 1
        logging.info('Comenzando trabajo ID: %d', job_id)
        logging.debug('Calculando segmentos del fichero.')
        parts = self._split_file(filename, len(self._mappers))
        print "Nahuel - parts: ", parts
        # informar al reducer del trabajo
        logging.info('Enviando el trabajo al reducer')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(tuple(self._reducer))
        Mensaje(sock).send(job_id, str( len(parts) ))
        sock.close()

        fh = open(filename, 'r')
        for i in range(len(self._mappers)):
            id, byte_start, byte_end = parts[i]
            logging.info('Enviando tarea a %s:%d.' % self._mappers[i])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(tuple(self._mappers[i]))
            fh.seek(byte_start)
            print "i: ", i , " - asignado: ", byte_end - byte_start
            Mensaje(sock).send(id, fh.read(byte_end - byte_start))
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
        id_job, result_index = Mensaje(client_socket).recv()
        result_index = ast.literal_eval(result_index)
        fh = open(self._outfile, 'w')
        for i in result_index.iteritems():
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
