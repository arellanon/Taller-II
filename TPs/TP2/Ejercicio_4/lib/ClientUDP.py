#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, string, sys, time, struct

class ClientUDP:
### Cliente

    def __init__(self, host = '0.0.0.0', port = 53, recv_buffer = 512):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        
    def ping(self):
    ### Iniciar conexion
        # Tiempo de inicio de ejecución.
        inicio = time.time()
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.client_socket.settimeout(10)
        data = struct.pack('14s','www.google.com')
        self.client_socket.sendto(data,(self.host, self.port))
        data =self.client_socket.recv(512)
        fin = time.time()

        tiempo_total = fin - inicio
        return tiempo_total

    def rtt(self, segundos):
        tiempo = 0
        count = 0
        acum = 0
        inicio = time.time()
#        print "segundos: ", segundos
        while tiempo <= segundos:
            count += 1
            acum += self.ping()
#            print "count: ", count, " - acum: ", acum
            fin = time.time()
            tiempo = fin - inicio
        return acum / count
