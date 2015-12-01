#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import ast
from Msg import Msg

class NodoReducer():

    def __init__(self, host, port, master):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.listen = 5
        self.master = master

    def iniciar_server(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket_server.bind((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.socket_server.close()
            import sys
            sys.exit(1)
        self.esperando_conexiones()

    def esperando_conexiones(self):
        self.socket_server.listen(self.listen)
        while True:
            print 'Esperando conexiones'
            #Recibimos nro de tareas a procesar
            socket_client, client_addr = self.socket_server.accept()
            id_proceso, nro_tareas = Msg(socket_client).recv()
            nro_tareas = int( nro_tareas )
            print 'Nro. de tareas a procesar: ', nro_tareas
            print 'Esperando resultados de los mappers'
            tareas_terminadas = []
            self.index = {}
            while len(tareas_terminadas) < nro_tareas:
                socket_mapper, mapper_addr = self.socket_server.accept()
                id_tarea, mapper_index = Msg(socket_mapper).recv()
                mapper_index = ast.literal_eval(mapper_index)        
                if id_tarea in tareas_terminadas:
                    print 'Resultado ignorado, la tarea ya fue informada'
                else:
                    self.actualizar_index_total(mapper_index)
                    tareas_terminadas.append(id_tarea)
                    print 'Resultado: (',len(tareas_terminadas),'/', nro_tareas,')'
                socket_mapper.close()
            socket_client.close()
            print 'enviar los resultados al master'
            # enviar los resultados
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(tuple(self.master))
            Msg(sock).send(id_proceso, str( self.index ) )
            sock.close()
            print 'Fin del proceso.'

    def actualizar_index_total(self, results):
        for t, f in results.iteritems():
            self.index[t] = self.index.get(t, 0) + f
