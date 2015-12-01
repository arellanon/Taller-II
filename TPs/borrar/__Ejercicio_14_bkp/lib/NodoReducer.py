#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import math
import os
import random
import socket
import indexer
import ast
from Msg import Msg

class NodoReducer():

    def __init__(self, host, port, master):
        self._host = host
        self._port = port
        self._master = master
        self._tcp_buffer_size = 4096
        self._backlog = 5
        self._reuseaddr = 1

    def _start_server(self):
        'Inicializa el socket para recibir tareas.'
        logging.info('Iniciando la escucha en %s:%d', self._host, self._port)
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, self._reuseaddr)
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
            job_id, job_tasks = Msg(client_socket).recv()            
            job_tasks = int( job_tasks )
            logging.info('Esperando resultados de los mappers')
            tasks_completed = []
            self._index = {}
            while len(tasks_completed) < job_tasks:
                mapper_socket, mapper_addr = self._server_socket.accept()
                id_task, result_index = Msg(mapper_socket).recv()
                result_index = ast.literal_eval(result_index)        
                if tasks_completed.count(id_task) > 0:
                    logging.info(
                        'Los resultados se ignorarán debido a que la '
                        'tarea con ID: %d ya se recibió anteriormente.',
                        id_task)
                else:
                    self._update_index(result_index)
                    tasks_completed.append(id_task)
                    logging.info(
                        'Recibidos los resultados (%d/%d)',
                        len(tasks_completed), job_tasks)
                mapper_socket.close()
            # cerrar sockets
            client_socket.close()
            logging.info('Enviando resultados globales al nodo master')
            # enviar los resultados
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(tuple(self._master))
            Msg(sock).send(job_id, str( self._index ) )
            sock.close()
            logging.info('Finalizado el trabajo.')

    def _update_index(self, results):
        'Hace un merge entre el índice global y results, sumando frecuencias.'
        for t, f in results.iteritems():
            self._index[t] = self._index.get(t, 0) + f
