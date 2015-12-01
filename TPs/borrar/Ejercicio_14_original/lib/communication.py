# -*- coding: UTF-8 -*-
import json
import logging
import struct

class JSONConnection(object):
    '''Permite el envío y recepción de objetos utilizando JSON.

    Esta clase permite generar una capa de abrstracción sobre un socket TCP
    de modo que puedan enviarse directamente cualquier tipo de objeto que pueda
    serializarse utilizando la librería json de Python 2.6+.
    '''

    def __init__(self, sock):
        self._socket = sock

    def send(self, obj):
        jsondata = json.dumps(obj)
        bytes = struct.pack('<I', len(jsondata))
        self._socket.sendall(bytes + jsondata)

    def recv(self):
        bytes = self._sock_recv(struct.calcsize('<I'))
        jsondata = self._sock_recv(struct.unpack('<I', bytes)[0])
        return json.loads(jsondata)

    def _sock_recv(self, bytes):
        'Lee del socket exactamente la cantidad del argumento bytes.'
        remaining = bytes
        data = ''
        while remaining > 0:
            d = self._socket.recv(remaining)
            remaining -= len(d)
            data += d
        return data

    def close(self):
        self._socket.close()


class CommunicationManager(object):

    def __init__(self, sock):
        self._jsonconn = JSONConnection(sock)

    def send_results(self, id, results):
        logging.debug(
            'Enviando resultados')
        data = {
            'id': id,
            'index': results
        }
        self._jsonconn.send(data)
        logging.debug('Se enviaron los resultados.')

    def recv_results(self):
        logging.debug(
            'Recibiendo los resultados')
        data = self._jsonconn.recv()
        logging.debug(
            'Se recibieron los resultados.')
        return data

    def send_task(self, id, task_text):
        data = {
            'id': id,
            'text': task_text
        }
        self._jsonconn.send(data)

    def recv_task(self):
        logging.debug(
            'Recibiendo la tarea')
        data = self._jsonconn.recv()
        logging.debug('Se recibió la tarea ID: %d', data['id'])
        return data

    def send_job(self, id, tasks_count):
        data = {
            'id': id,
            'tasks': tasks_count
        }
        self._jsonconn.send(data)

    def recv_job(self):
        logging.info('Recibiendo trabajo')
        data = self._jsonconn.recv()
        logging.info(
            'Se recibió el trabajo ID: %d, TASKS:%d',
            data['id'], data['tasks'])
        return data
