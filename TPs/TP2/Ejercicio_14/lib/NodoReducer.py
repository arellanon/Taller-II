#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, ast
from Msg import Msg

class NodoReducer():

    def __init__(self, host, port, master):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.listen = 5
        self.master = master

    def iniciar_server(self):
        try:
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
        except KeyboardInterrupt:
            print "\Reducer finalizado."

    def esperando_conexiones(self):
        self.socket_server.listen(self.listen)
        while True:
            print 'Esperando conexiones'
            #Recibimos nro de tareas a procesar
            socket_client, client_addr = self.socket_server.accept()
            id_proceso, nro_tareas = Msg(socket_client).recv()
            nro_tareas = int( nro_tareas )
            print 'Cantidad de tareas a procesar: ', nro_tareas
            print 'Esperando resultados de los mappers'
            tareas_terminadas = []
            resultado = {}
            while len(tareas_terminadas) < nro_tareas:
                socket_mapper, mapper_addr = self.socket_server.accept()
                id_tarea, mapper_index = Msg(socket_mapper).recv()
                mapper_index = ast.literal_eval(mapper_index)        
                if id_tarea in tareas_terminadas:
                    print 'Resultado ignorado, la tarea ya fue informada'
                else:
                # unimos los index de los mapper en un unico resultado
                    for t, f in mapper_index.iteritems():
                        resultado[t] = resultado.get(t, 0) + f                   
                    tareas_terminadas.append(id_tarea)
                    print 'Resultado del mapper ' , socket_mapper.getpeername(),': (',len(tareas_terminadas),'/', nro_tareas,')'
                socket_mapper.close()
            socket_client.close()
            print 'enviar los resultados al master'
            # enviar los resultados
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect(tuple(self.master))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket.", tuple(self.master)
                sock.close()
                import sys
                sys.exit(1)
            Msg(sock).send(id_proceso, str( resultado ) )
            sock.close()
            print 'Fin del proceso.'
