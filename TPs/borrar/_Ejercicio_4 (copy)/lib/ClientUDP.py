#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, string, sys, time, struct

class ClientUDP:
### Cliente

    def __init__(self, host = '0.0.0.0', port = 53, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        
#    def build_packet(self, url):
#        packet = struct.pack("H", 12049)  # Query Ids (Just 1 for now)
#        packet += struct.pack("H", 256)  # Flags
#        packet += struct.pack("H", 1)  # Questions
#        packet += struct.pack("H", 0)  # Answers
#        packet += struct.pack("H", 0)  # Authorities
#        packet += struct.pack("H", 0)  # Additional
#        split_url = url.split(".")
#        for part in split_url:
#            packet += struct.pack("B", len(part))
#            for byte in bytes(part):
#                packet += struct.pack("c", byte)
#        packet += struct.pack("B", 0)  # End of String
#        packet += struct.pack("H", 1)  # Query Type
#        packet += struct.pack("H", 1)  # Query Class
#        return packet
        
    def ping(self):
    ### Iniciar conexion
        # Tiempo de inicio de ejecución.
        inicio = time.time()
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#        data = self.build_packet("www.google.com.ar")
        data = struct.pack('14s','www.google.com')
#        print data
        try:
            self.client_socket.sendto(data,(self.host, self.port))
            data,addr=self.client_socket.recv(512)
            if data:
                print 'paquete ok.'
#            self.client_socket.shutdown(socket.SHUT_RDWR)
#            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
        # Tiempo de fin de ejecución.
        fin = time.time()
        # Tiempo de ejecución.
#        print "inicio: ", inicio
#        print "fin: ", fin
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
