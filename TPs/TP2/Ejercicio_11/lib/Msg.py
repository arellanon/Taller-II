#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio y recepcion de mensajes
#La pdu esta compuesta por:
#   secuencia       - int 4byte
#   ack             - int 4byte
#   ack_bitfield    - int 4byte
#   data            - string

class Msg():

    def __init__(self, sock, buff):
        self.socket = sock
        self.buff = buff

    def send(self, pdu, address):
        secuencia=pdu[0]
        ack=pdu[1]
        ack_bitfield=pdu[2] 
        data=pdu[3]
        secuencia = struct.pack('<I', secuencia)
        ack  = struct.pack('<I', ack)
        ack_bitfield  = struct.pack('<I', ack_bitfield)
        pdu = secuencia + ack + ack_bitfield + data
        self.socket.sendto(pdu, address)

    def recv(self):
    #recuperamos
        datos, address = self.socket.recvfrom(self.buff)
        secuencia = datos[:4]
        secuencia = struct.unpack('<I', secuencia)[0]
        ack = datos[4:8]
        ack = struct.unpack('<I', ack)[0]        
        ack_bitfield = datos[8:12]
        ack_bitfield = struct.unpack('<I', ack_bitfield)[0]
        data = datos[12:]
        pdu = [secuencia, ack, ack_bitfield, data]
        return pdu, address
