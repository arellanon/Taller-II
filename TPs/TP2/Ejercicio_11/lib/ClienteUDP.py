#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket 
from sys import argv
import sys
import os
from threading import Thread, Event
import time
import datetime
import argparse
import signal
from Msg import Msg
from ServiceExit import ServiceExit

RTT_MAX = 1
QUEUE_WAIT_ACKS = {}
STOP = False
CANT_RETRANSMISIONES = 0
CANT_RETRANSMISIONES_TOTAL = 0
ESTADO_RED = 'BAD'

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class ClienteUDP():
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 1024):
        self.host_server = host
        self.port_server = port
        self.recv_buffer = recv_buffer
        self.log = log

    def iniciar_cliente(self):
    ### Iniciar servidor
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)
        global CANT_RETRANSMISIONES
        try:    
            self.socket_client= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#            self.socket_client.setblocking(0)
            job = RecvAck(self.socket_client)
            job.start() #Ejecutamos un Thread esperando por acks
            job2 = DetectingLostPackets(self.socket_client,  self.host_server, self.port_server )
            job2.start() 
            secuencia = 0
            cantPaquetes = 0
            continuar = True
            timeComienzo = int(datetime.datetime.now().time().strftime('%s'))
            while continuar:
                
#            for k in range(30):
                data = 'hola mundo: '+ str(secuencia)
                ack = 0
                ack_bitfield = 0
                Msg(self.socket_client).send(secuencia, ack, ack_bitfield, data, self.host_server, self.port_server )
#                print "enviado: ",secuencia, ack, ack_bitfield, data,
                QUEUE_WAIT_ACKS[secuencia]= { 'ack' : ack, 'ack_bitfield': ack_bitfield, 'data': data, 'time' : int(datetime.datetime.now().time().strftime('%s')) } #Se agrega la secuencia del paquete al diccionario con su hora actual
                secuencia+=1
                if ESTADO_RED=='GOOD':
                    time.sleep(0.0333)  #Si el estado de la red es bueno envia 30 paquetes por segundos
                else:
                    time.sleep(0.1)   #Si el estado de la red es malo envía 10 paquetes por segundos
                cantPaquetes+=1
                tiempoActual = int(datetime.datetime.now().time().strftime('%s'))
                
                if ( (tiempoActual - timeComienzo )  > 1) :
                    print "Cantidad de paquetes por segundo: ", cantPaquetes , CANT_RETRANSMISIONES, ' TOTAL', CANT_RETRANSMISIONES_TOTAL
                    cantPaquetes = 0
                    CANT_RETRANSMISIONES = 0
                    timeComienzo = int(datetime.datetime.now().time().strftime('%s'))
            job.shutdown_flag.set()
            job.join()
            job2.shutdown_flag.set()
            job2.join()    
        except ServiceExit:
            print 'Service EXIT'
            STOP = True
            job.shutdown_flag.set()
            job.join()
            job2.shutdown_flag.set()
            job2.join()
        print('Exiting main program')


class RecvAck(Thread):
    def __init__(self, socket):
        self.socket = socket
        self.buff_size = 256
        self.shutdown_flag = Event()
        Thread.__init__(self)
   
    def run(self):
#        print('Thread #%s started' % self.ident)
#        print 'flag: ', self.shutdown_flag.is_set()
        try:
            while not self.shutdown_flag.is_set():
                secuencia, ack, ack_bitfield, data, address = Msg(self.socket).recv()
#                print "Texto: "+data+ " proveniente de: ", address
                i=0
                ack_bitfield_str = (bin(ack_bitfield)[2:]).zfill(32) #transformo el int en binario para poder contralar los flags
#                print ack_bitfield_str, ack
                for bit in ack_bitfield_str: #Controla los bits de ackbitfield
                    if bit=='1': #Si el bit es igual 1 significa que el paquete ha sido recibido
                        secuencia= ack - i
#                        print "Paquete numero "+str(secuencia) +" recibido"
                        QUEUE_WAIT_ACKS.pop(secuencia, None) #si recibimos ack, lo eliminamos de la lista
                    else :
                        secuencia= ack - i
#                        print "Paquete numero "+str(secuencia) +" NO recibido"
                    i+=1
        except ServiceExit:
            self.socket.close()
#        print 'flag: ', self.shutdown_flag.is_set()
#        print('Thread #%s stopped' % self.ident)


class DetectingLostPackets(Thread):
    def __init__(self, socket, host, port):
#        self.secuencia = secuencia
        self.socket_client = socket 
        self.host_server = host
        self.port_server = port
        self.shutdown_flag = Event()
        Thread.__init__(self)

    def run(self):
        try:
            global STOP
            global CANT_RETRANSMISIONES
            global CANT_RETRANSMISIONES_TOTAL            
            global QUEUE_WAIT_ACKS
            continuar = True
            while not self.shutdown_flag.is_set():
    #        while continuar==True and not STOP:
                time.sleep(0.5)
    #            if secuencia in QUEUE_WAIT_ACKS.keys():
                for secuencia in QUEUE_WAIT_ACKS.keys():
                    try:
                        delta = int(datetime.datetime.now().time().strftime('%s')) - QUEUE_WAIT_ACKS[secuencia]['time']  
                        if secuencia in QUEUE_WAIT_ACKS.keys() and delta >= RTT_MAX:
        #                    print "\nsecuencia: ", str(self.secuencia), ' - delta: ', str(delta)
                            ack= QUEUE_WAIT_ACKS[secuencia]['ack']
                            ack_bitfield =QUEUE_WAIT_ACKS[secuencia]['ack_bitfield']
                            data = QUEUE_WAIT_ACKS[secuencia]['data']
                            #pdu = encapsularPDU(self.secuencia, ack,ackbitfield,texto) #Encapsular la PDU
                            Msg(self.socket_client).send(secuencia, ack, ack_bitfield, data, self.host_server, self.port_server )
                            QUEUE_WAIT_ACKS[secuencia]= { 'ack' : ack, 'ack_bitfield': ack_bitfield, 'data': data, 'time' : int(datetime.datetime.now().time().strftime('%s')) } #Se agrega la secuencia del paquete al diccionario con su hora actual
    #                        print QUEUE_WAIT_ACKS[self.secuencia]
    #                        print "retransmitir: ", secuencia
                            CANT_RETRANSMISIONES+=1
                            CANT_RETRANSMISIONES_TOTAL+=1
                    except:
                        continue
        except ServiceExit:
            self.socket_client.close()
