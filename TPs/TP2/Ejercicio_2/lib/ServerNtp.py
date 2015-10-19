#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import AF_INET, SOCK_DGRAM
import datetime
import sys
import socket
import struct, time

class ServerNtp:
    
    def __init__(self, host = '0.0.0.0', port = 5000, recv_buffer = 1024):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def iniciar_server(self):
        self.server_socket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        try:
            print "Corriend servidor %s:%s " % (self.host, self.port)
            self.server_socket.bind(( self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion del socket."
            sys.exit(1)
        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()
    
    def esperando_conexiones(self):
        print "Esperando conexion..."
        while True:
            data, addr = self.server_socket.recvfrom(self.recv_buffer)
            print "Conexion desde: ", addr
            today = datetime.datetime.now().strftime(data)
#            today = self.sincronizar()
            self.server_socket.sendto(str(today) ,addr)
    
    def sincronizar(self):
        # Seteo de variables del servidor NTP
        host = "pool.ntp.org"
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'
        #
        #  Expresamos 1970-01-01 00:00:00 en segundo
        #
        #       1900-01-01
        #   -   1970-01-01
        #       ----------
        #            25567 (dias)
        #     
        #       25567 dias x 24 hs x 60 min x 60 seg = 2208988800 seg

        TIME1970 = 2208988800L # 1970-01-01 00:00:00
        # Conectar al servidor
        client = socket.socket(AF_INET,SOCK_DGRAM)
        client.sendto(msg, address)
        data, address = client.recvfrom(buf)

        # Recuperamos los segundos
        t = struct.unpack("!12I", data)[10]
        # Restamos los segundos 1970
        t -= TIME1970

        date = time.ctime(t)
        return date
