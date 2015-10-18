#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys, os, subprocess

class ServerSsh:

    def __init__(self, host = '0.0.0.0', port = 5000, recv_buffer = 1024):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = 5

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
        
    def cmd(self, comando, client_sock):
        try:
            output = subprocess.check_output(comando, shell=True)
            client_sock.send(output)
        except Exception as e:
            client_sock.send("Comando no válido.\n")
        
    def esperando_conexiones(self):
        print "Esperando conexion..."
        self.server_socket.listen(self.listen)        
        while True:
            client_sock, addr = self.server_socket.accept()
            print "Conexion desde: ", client_sock.getpeername()
            data = client_sock.recv(self.recv_buffer)
            comando = bytes.decode(data).rstrip('\r\n')
            self.cmd(comando, client_sock)
            while len(data):
                print comando
                data = client_sock.recv(self.recv_buffer)
                comando = bytes.decode(data).rstrip('\r\n')
                self.cmd(comando, client_sock)
            client_sock.close()
