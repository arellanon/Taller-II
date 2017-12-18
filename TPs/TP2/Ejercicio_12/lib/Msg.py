#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio de mensajes
#Esta compuesta por accion - len data - data

class Msg():

    def __init__(self, sock):
        self.socket = sock

    def send(self, accion, data):
        accion  = struct.pack('<I', accion)
        bytes = struct.pack('<I', len(data))
        self.socket.sendall(accion + bytes + data)

    def recv(self):
    #recuperamos 
        accion  = self.recvall(struct.calcsize('<I'))
        accion = struct.unpack('<I', accion)[0]        
        bytes = self.recvall(struct.calcsize('<I'))
        data = self.recvall(struct.unpack('<I', bytes)[0]) 
        return accion, data

    def recvall(self, bytes):
        buff = bytes
        data_total = ''
        while buff > 0:
            data = self.socket.recv(buff)
            buff -= len(data)
            data_total += data
        return data_total
