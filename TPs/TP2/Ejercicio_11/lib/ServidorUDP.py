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
from ServiceExit import ServiceExit

REMOTE_SEQUENCE={}

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class ServidorUDP():
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 1024):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.log = log

    def iniciar_server(self):
    ### Iniciar servidor
        self.socket_server= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
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
            job = ThreadServer(self.socket_server)
            job.start()
            flag = True
            while True:
                secuencia, ack, ack_bitfield, data, address = Msg(self.socket_server).recv()
#                print secuencia, ack, ack_bitfield, data, address
                """
                if secuencia == 10 and flag:
                    flag = False
                    continue
                """
                if not address in REMOTE_SEQUENCE.keys(): #Almacena la secuencia del paquete recibido en su conexión correspondiente
                    REMOTE_SEQUENCE[address] = []
                    REMOTE_SEQUENCE[address].append(secuencia)
                else: 
                    REMOTE_SEQUENCE[address].append(secuencia)
        except ServiceExit:
            job.shutdown_flag.set()
            job.join()
        print('Exiting main program')

    def cerrar_server(self):
    ### Cerrar conexion
        try:
#            self.socket_server.shutdown(socket.SHUT_RDWR)
            self.socket_server.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e


class ThreadServer(Thread):
    def __init__(self, socket_server):
        self.socket_server = socket_server
        self.shutdown_flag = Event()  
        Thread.__init__(self)

    def run(self):
        global REMOTE_SEQUENCE
        while not self.shutdown_flag.is_set():  
            if len(REMOTE_SEQUENCE)>0:
                time.sleep(0.5)
                for address in REMOTE_SEQUENCE: #Por cada "conexión", envía los datos recibidos
                    secuencia = 0
                    ack=max(REMOTE_SEQUENCE[address])  #El valor de ack es el máximo nro de secuencia recibido  
                    ack_bitfield = self.GetAckbitfield(ack, REMOTE_SEQUENCE[address])
                    data='Paquetes enviados: '+str(len(REMOTE_SEQUENCE[address])) + ' - ack: '+ str(ack) +' - ack_bitfield: ' + str(ack_bitfield)
                    print data 
                    Msg(self.socket_server).send(secuencia, ack, ack_bitfield, data, address[0], address[1] )
                REMOTE_SEQUENCE={}
        self.socket_server.close()
        
#Se genera el ack_bitfield - utiliza los 32 bits como flags del int de 4bytes
    def GetAckbitfield(self, ack, secuencias):
        i=0
        ack_bitfield=''
        for i in range(32):
            if (ack-i) in secuencias: #Si el valor de secuencia existe asigna 1, caso contrario asigna 0
                ack_bitfield = ack_bitfield + '1'
            else:
                ack_bitfield = ack_bitfield + '0'
        return int(ack_bitfield, 2)
