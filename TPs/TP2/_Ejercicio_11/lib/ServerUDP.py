#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import AF_INET, SOCK_DGRAM
import datetime
import sys
import socket
from Msg import Msg
#import struct, time

class ServerUDP:
    
    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 1024):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def iniciar_server(self):
        try:
            self.server_socket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            try:
                print "Corriendo servidor %s:%s " % (self.host, self.port)
                self.server_socket.bind(( self.host, self.port))
            except Exception as e:
                print "ERROR: Falla en la conexion del socket."
                sys.exit(1)
            print "Presionar Ctrl+C para salir."
            self.esperando_conexiones()
        except KeyboardInterrupt:
            print "\nServer finalizado."

    def esperando_conexiones(self):
        print "Esperando conexion..."
        while True:
            #data, addr = self.server_socket.recvfrom(self.recv_buffer)
            id, data, addr_client = Msg(self.server_socket).recv()
            print "Conexion desde: ", id, addr_client
            #self.server_socket.sendto(data ,addr)
	    Msg(self.server_socket).send(2, data, addr_client )
