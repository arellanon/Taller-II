#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct

#Clase implementada para el envio de mensajes
#Esta compuesta por accion - len data - data

class Msg():

    def __init__(self, sock):
        self.socket = sock
        self.buff = 256

    def send(self, secuencia, ack, ack_bitfield, data, host, port):
        secuencia = struct.pack('<I', secuencia)
        ack  = struct.pack('<I', ack)
        ack_bitfield  = struct.pack('<I', ack_bitfield)
        pdu = secuencia + ack + ack_bitfield + data
        #padding = 256 - len(pdu)
        #print 'len: ',len(pdu), ' - padding: ', padding
        self.socket.sendto(pdu, (host, port) )

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
        return secuencia, ack, ack_bitfield, data, address
