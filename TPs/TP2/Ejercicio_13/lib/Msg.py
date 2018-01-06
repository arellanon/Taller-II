#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio de mensajes
#Esta compuesta por id_origen - id_destino - flag_turno - flag_recibido - flag_fin - len data - data

class Msg():

    def __init__(self, sock):
        self.socket = sock

    def send(self, pdu):
        id_origen = pdu[0]
        id_destino = pdu[1]
        turno = pdu[2]
        recibido = pdu[3]
        fin = pdu[4]
        data = pdu[5]
        id_origen  = struct.pack('<I', id_origen)
        id_destino = struct.pack('<I', id_destino)
        turno = struct.pack('<?', turno)
        recibido = struct.pack('<?', recibido)
        fin = struct.pack('<?', fin)
        bytes = struct.pack('<I', len(data))
        self.socket.sendall(id_origen + id_destino + turno + recibido + fin + bytes + data)

    def recv(self):
    #recuperamos 
        id_origen  = self.recvall(struct.calcsize('<I'))
        id_origen = struct.unpack('<I', id_origen)[0]
        id_destino  = self.recvall(struct.calcsize('<I'))
        id_destino = struct.unpack('<I', id_destino)[0]

        turno  = self.recvall(struct.calcsize('<?'))
        turno = struct.unpack('<?', turno)[0]        

        recibido  = self.recvall(struct.calcsize('<?'))
        recibido = struct.unpack('<?', recibido)[0]
        
        fin  = self.recvall(struct.calcsize('<?'))
        fin = struct.unpack('<?', fin)[0]
        
#        id = self.recvall(struct.calcsize('<I'))
#        id = struct.unpack('<I', id)[0]
        bytes = self.recvall(struct.calcsize('<I'))
        data = self.recvall(struct.unpack('<I', bytes)[0])
        pdu = [id_origen, id_destino, turno, recibido, fin, data]
        return pdu 

    def recvall(self, bytes):
        buff = bytes
        data_total = ''
        while buff > 0:
            data = self.socket.recv(buff)
            buff -= len(data)
            data_total += data
        return data_total
