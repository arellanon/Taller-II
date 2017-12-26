#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random
#from AcceptClient import AcceptClient
from threading import Thread
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname
import time

class NodoMaster:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 1024, listen = 5):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = listen
        self.log = log

    def iniciar_server(self):
    ### Iniciar conexion
        self.socket_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket_server.bind((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar_server()
            import sys
            sys.exit(1)
        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()

    def esperando_conexiones(self):
        self.socket_server.listen(self.listen)
        try: 
            while True:
                conn_client, addr_client = self.socket_server.accept()
                print "se acepto una conexion"
                ThreadMaster(conn_client).start()
        except KeyboardInterrupt:
            print "\nServidor Apagado"
        self.cerrar_server()

    def cerrar_server(self):
    ### Cerrar conexion
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            self.socket_server.close()            
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e



class ThreadMaster(Thread):
    def __init__(self, conn_client):
        self.conn_client = conn_client
#        self.id_master = 0
        Thread.__init__(self)

    def run(self):
        print "threadMaster", self.conn_client.getpeername()
