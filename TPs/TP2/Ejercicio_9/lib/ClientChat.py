#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select, string, sys

class ClientChat:
### Class server Chat

    def __init__(self, host = '0.0.0.0', port = 5000, recv_buffer = 4096, listen = 10):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        # Lista de socket
        self.CONNECTION_LIST = []
        
    def iniciar_server(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.settimeout(2)
            self.client_socket.connect((self.host, self.port))
            
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar()
            import sys
            sys.exit(1)

        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()

    def cerrar(self):
    ### Cerrar conexion
        try:
            #self.server_socket.cerrar_server(socket.SHUT_RDWR)
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

    def esperando_conexiones(self):
        while True:
            socket_list = [sys.stdin, s]
             
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
             
            for sock in read_sockets:
                #incoming message from remote server
                if sock == s:
                    data = sock.recv(self.recv_buffer)
                    if not data :
                        print '\nDisconnected from chat server'
                        sys.exit()
                    else :
                        #print data
                        sys.stdout.write(data)
                        prompt()
                 
                #user entered a message
                else :
                    msg = sys.stdin.readline()
                    s.send(msg)
                    prompt()
