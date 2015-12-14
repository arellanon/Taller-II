#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from Index import Index
from Tokenizer import Tokenizer
from Msg import Msg

class NodoMapper(object):

    def __init__(self, host, port, reducer):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.listen = 5
        self.reducer = reducer        

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
            print "\nMapper finalizado."
        
    def esperando_conexiones(self):
        self.socket_server.listen(self.listen)
        while True:
            print 'Esperando tareas...'
            #Recibimos tarea del master
            socket_client, client_addr = self.socket_server.accept()
            id_tarea, text_parte = Msg(socket_client).recv()
            print 'Tarea asignada: ', id_tarea
            socket_client.close()

            # procesar parte del texto asignada
            index = Index().indexar(text_parte)
            # enviar los resultados al reducer
            socket_reducer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print 'conectando reducer: ',tuple(self.reducer)
                socket_reducer.connect(tuple(self.reducer))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket.", tuple(self.reducer)
                socket_reducer.close()
                import sys
                sys.exit(1)
                
            Msg(socket_reducer).send(id_tarea, str( index ) )
            socket_reducer.close()
            print 'Tarea finalizada'

    def stopwords(self, filename):
        infile = open(filename, 'r')
        stopw = infile.readlines()
        infile.close()
        return stopw
