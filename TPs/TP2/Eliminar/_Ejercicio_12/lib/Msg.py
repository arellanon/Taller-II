#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio de mensajes
#Esta compuesta por accion - len data - data

class Msg():

    def __init__(self, sock):
        self.socket = sock

    def send(self, id_nodo, accion, path, data):
        id_nodo = struct.pack('<I', id_nodo)
        accion  = struct.pack('<I', accion)
        bytes_path = struct.pack('<I', len(path))
        bytes = struct.pack('<I', len(data))
        self.socket.sendall(id_nodo + accion + bytes_path + path + bytes + data)

    def recv(self):
    #recuperamos 
        id_nodo  = self.recvall(struct.calcsize('<I'))
        id_nodo = struct.unpack('<I', id_nodo)[0]
        accion  = self.recvall(struct.calcsize('<I'))
        accion = struct.unpack('<I', accion)[0]
        bytes_path = self.recvall(struct.calcsize('<I'))
        path = self.recvall(struct.unpack('<I', bytes_path)[0])
        bytes = self.recvall(struct.calcsize('<I'))
        data = self.recvall(struct.unpack('<I', bytes)[0])
        return id_nodo, accion, path, data

    def recvall(self, bytes):
        buff = bytes
        data_total = ''
        while buff > 0:
            data = self.socket.recv(buff)
            buff -= len(data)
            data_total += data
        return data_total
