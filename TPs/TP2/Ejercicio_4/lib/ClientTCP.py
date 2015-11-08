#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, string, sys, time

class ClientTCP:
### Cliente

    def __init__(self, host = '0.0.0.0', port = 80, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def ping(self):
    ### Iniciar conexion
        # Tiempo de inicio de ejecución.
        inicio = time.time()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            #self.cerrar()
            import sys
            sys.exit(1)
    ### Cerrar conexion
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
        # Tiempo de fin de ejecución.
        fin = time.time()
        # Tiempo de ejecución.
        print "inicio: ", inicio
        print "fin: ", fin
        tiempo_total = fin - inicio
        return tiempo_total
