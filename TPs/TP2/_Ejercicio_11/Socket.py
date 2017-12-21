#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

class Socket:
      
    def __init__(self, port, host = '127.0.0.1'):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.listen = 5
        
    def Open(self):
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            try:
                print "Open - %s:%s" % (self.host, self.port)
                self.socket.bind((self.host, self.port))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket."
                self.socket.close()
                import sys
                sys.exit(1)
    #            self.esperando_conexiones()
        except KeyboardInterrupt:
            print "\nSocket finalizado."

    def Send(self, data, host_dst, port_dst):
        self.socket.sendto( data, (host_dst, port_dst) )
    
    def Receive(self):
        self.socket.recvfrom(self.recv_buffer)
        
    def Close(self):
        self.socket.close()

