#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select, string, sys

class ClientChat:
### Cliente

    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.settimeout(2)
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar()
            import sys
            sys.exit(1)
        print "Ingreso al chat."
        self.esperando_conexiones()

    def cerrar(self):
    ### Cerrar conexion
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
            
    def prompt(self):
        sys.stdout.write('<Yo> ')
        sys.stdout.flush()

    def esperando_conexiones(self):
        while True:
            socket_list = [sys.stdin, self.client_socket]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
            for socket in read_sockets:
                if socket == self.client_socket:
                    data = socket.recv(self.recv_buffer)
                    if not data :
                        print '\nDesconectado del chat.'
                        sys.exit()
                    else :
                        sys.stdout.write(data)
                        self.prompt()
                else :
                    msg = sys.stdin.readline()
                    self.client_socket.send(msg)
                    self.prompt()
