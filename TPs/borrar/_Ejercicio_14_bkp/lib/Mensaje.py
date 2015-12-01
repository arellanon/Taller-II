# -*- coding: UTF-8 -*-
import struct

class Mensaje():

    def __init__(self, sock):
        self.socket = sock

    def send(self, id, data):
        id = struct.pack('<I', id)
        bytes = struct.pack('<I', len(data))
        self.socket.sendall(id + bytes + data)

    def recv(self):
        id = self.recvall(struct.calcsize('<I'))
        id = struct.unpack('<I', id)[0]
        bytes = self.recvall(struct.calcsize('<I'))
        data = self.recvall(struct.unpack('<I', bytes)[0])
        return id, data

    def recvall(self, bytes):
    #Recuperamos la cantidad informada en bytes
        buff = bytes
        data_total = ''
        while buff > 0:
            data = self.socket.recv(buff)
            buff -= len(data)
            data_total += data
        return data_total
