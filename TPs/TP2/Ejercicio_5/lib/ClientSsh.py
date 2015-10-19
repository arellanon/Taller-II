#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select, string, sys

class ClientSsh:
### Cliente

    def __init__(self, host = '0.0.0.0', port = 5000, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar()
            import sys
            sys.exit(1)

        self.prompt()

    def cerrar(self):
    ### Cerrar conexion
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
        
    def prompt(self):
        while True:
            msg = sys.stdin.readline()
            self.client_socket.send(msg)
            datos = self.client_socket.recv(self.recv_buffer)
            print datos
        
