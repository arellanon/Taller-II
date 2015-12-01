#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import math
import os
import random
import socket
import indexer
from Msg import Msg

class NodoMapper(object):

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
        task_id, task_text = Msg(client_socket).recv()        
        task_text = unicode(task_text)
        # cerrar sockets
        client_socket.close()
        # indexar la porción del texto recibida
        tokenizer = indexer.Tokenizer(self._stopwords(self._stopwsfile))
        index = indexer.Index(tokenizer)
        index.index_str(task_text)
        # enviar los resultados
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(tuple(self._reducer))
        Msg(sock).send(task_id, str( index.dict() ) )
        sock.close()

    def _stopwords(self, filename):
        'Devuelve una lista con stopwords en español.'
        fh = open(filename, 'r')
        stopw = fh.readlines()
        fh.close()
        return stopw
