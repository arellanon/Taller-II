#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket 
from sys import argv
import sys
import os
import argparse
from os.path import exists
from os import system
from threading import Thread, Event
import time
from Msg import Msg
import signal
import errno
from ServiceExit import ServiceExit

REMOTE_SEQUENCE={}

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class ServidorUDP():
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 256):
        self.host = host
        self.port = port
        self.log = log
        self.recv_buffer = recv_buffer

    def iniciar_server(self):
    ### Iniciar servidor
        self.socket_server= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.socket_server.setblocking(0)   #Socket no bloqueante        
        self.socketMsg = Msg(self.socket_server, self.recv_buffer)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket_server.bind((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar_server()
            import sys
            sys.exit(1)
        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()

    def esperando_conexiones(self):
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)
        try: 
            threadSenderAcks = SenderAcks(self.socketMsg)
            threadSenderAcks.start()
#            flag = True
            while True:
                try:
                    pdu, address = self.socketMsg.recv()
                except IOError as e:  # and here it is handeled
                    if e.errno == errno.EWOULDBLOCK:
                        continue
                #descomponemos la pdu en los campos del header y data
                secuencia = pdu[0]
                ack = pdu[1]
                ack_bitfield = pdu[2]
                data = pdu[3]

                """
                if secuencia == 10 and flag:
                    flag = False
                    continue
                """
                if not address in REMOTE_SEQUENCE.keys(): #si el addres no existe se agrega
                    #se guarda secuencias por address de los paquetes recibidos
                    REMOTE_SEQUENCE[address] = []
                    REMOTE_SEQUENCE[address].append(secuencia)
                else:
                    REMOTE_SEQUENCE[address].append(secuencia)
        except ServiceExit:
            threadSenderAcks.shutdown_flag.set()
            threadSenderAcks.join()
            self.socket_server.close()            
        print('Exiting main program')

    def cerrar_server(self):
    ### Cerrar conexion
        try:
            self.socket_server.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e


class SenderAcks(Thread):
    def __init__(self, socketMsg):
        self.socketMsg = socketMsg
        self.shutdown_flag = Event()  
        Thread.__init__(self)

    def run(self):
        global REMOTE_SEQUENCE
        while not self.shutdown_flag.is_set():
            if len(REMOTE_SEQUENCE)>0:
                time.sleep(1)
                for address in REMOTE_SEQUENCE: #Por cada "conexión", envía los datos recibidos
                    secuencia = 0
                    ack=max(REMOTE_SEQUENCE[address])  #El valor de ack es el máximo nro de secuencia recibido  
                    ack_bitfield = self.construirAckbitfield(ack, REMOTE_SEQUENCE[address])
                    data='Paquetes enviados: '+str(len(REMOTE_SEQUENCE[address])) + ' - ack: '+ str(ack) +' - ack_bitfield: ' + str(ack_bitfield)
                    print data
                    pdu = [secuencia, ack, ack_bitfield, data]
                    self.socketMsg.send(pdu, address)    #reeviamos los paquetes que hayan superado el RTT_MAX
                REMOTE_SEQUENCE={}

#Se genera el ack_bitfield - utiliza los 32 bits como flags
    def construirAckbitfield(self, ack, lista_secuencias):
        i=0
        bitfield=''
        for i in range(32):
            if (ack-i) in lista_secuencias: #si existe en la lista de secuencias recibidas
                bitfield = bitfield + '1' #Si el valor de secuencia existe asigna 1
            else:
                bitfield = bitfield + '0' #Si el valor no existe asigna 0
        ack_bitfield = int(bitfield, 2) #convertimos el bitfield binario (str) a entero de 4 byte
        return ack_bitfield
