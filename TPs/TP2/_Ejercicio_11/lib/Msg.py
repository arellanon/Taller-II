#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio de mensajes
#Esta compuesta por Id - len data - data
class Msg():

    def __init__(self, sock):
        self.socket = sock
	self.recv_buffer = 1024

    def send(self, id, data, addr):
        id = struct.pack('<I', id)
        bytes = struct.pack('<I', len(data))
	print "bytes enviados: ", len(data)
        self.socket.sendto(id + bytes + data, addr)

    def recv(self):
        data, addr = self.socket.recvfrom(self.recv_buffer)
	header = data[0:8]
	datos = data[8:]
#	print type(id_recv)
        id = struct.unpack('<I', header[0:4])[0]
	print "id recividos: ", id, addr
        bytes = struct.unpack('<I', header[4:8])[0]
	print "bytes recividos: ", bytes, addr
        return id, datos, addr

"""
        id_recv, addr = self.socket.recvfrom(struct.calcsize('<I'))
        id = struct.unpack('<I', id_recv)[0]
	print "id recivido: ", id, addr
        bytes_recv, addr = self.socket.recvfrom(struct.calcsize('<I'))
	bytes = struct.unpack('<I', bytes_recv)[0]
	print "bytes recividos: ", bytes, addr
        data, addr = self.socket.recvfrom(bytes)
        return id, data, addr

    def recvall(self, bytes):
        buff = bytes
        data_total = ''
        while buff > 0:
            data = self.socket.recv(buff)
            buff -= len(data)
            data_total += data
        return data_total
"""
