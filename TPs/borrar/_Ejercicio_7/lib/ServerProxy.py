#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys, os, subprocess
import socket, thread, select
from lib.ConnectionHandler import ConnectionHandler

class ServerProxy:

    def __init__(self, host = '0.0.0.0', port = 5000, recv_buffer = 1024):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = 0
        self.timeout = 60

    def iniciar_server(self):
        self.server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Corriend servidor %s:%s " % (self.host, self.port)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(( self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion del socket."
            sys.exit(1)
        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()
        
    def esperando_conexiones(self):
        print "Esperando conexion..."
        handler=ConnectionHandler
        self.server_socket.listen(self.listen)        
        while True:
            thread.start_new_thread(handler, python self.server_socket.accept()+(self.timeout,))
