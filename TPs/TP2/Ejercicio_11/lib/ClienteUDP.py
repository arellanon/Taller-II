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
import errno
from Msg import Msg
from ServiceExit import ServiceExit


QUEUE_WAIT_ACKS = {}
CANT_RETRANSMISIONES = 0
RTT=0
RTT_RETRANSMISION = 2
RTT_MAX = 0.25
ESTADO_RED = 'BAD'


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class ClienteUDP():
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 256):
        self.host_server = host
        self.port_server = port
        self.recv_buffer = recv_buffer
        self.log = log

    def iniciar_cliente(self):
    ### Iniciar servidor
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)        
        
        global CANT_RETRANSMISIONES
        global QUEUE_WAIT_ACKS
        global RTT
        global ESTADO_RED
        try:    
            self.socket_client= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket_client.setblocking(0)   #Socket no bloqueante
            self.socketMsg = Msg(self.socket_client, self.recv_buffer)
            
            threadReliableAcks = ReliableAcks(self.socketMsg)
            threadReliableAcks.start()  #Ejecutamos un Thread esperando por acks
            threadDetectingLostPackets = DetectingLostPackets(self.socketMsg,  self.host_server, self.port_server )
            threadDetectingLostPackets.start() #Ejecutamos un Thread para la deteccion de errores
            threadFlowCongestion = FlowCongestion()
            threadFlowCongestion.start() #Ejecutamos un Thread para la control de flujo         

            tiempoInicio = int(datetime.datetime.now().time().strftime('%s'))
            cantPaquetes=0
            retransmisionesTotales=0            
            secuencia=0
            cont=0
            while True:
                data = 'Paquete: '+ str(secuencia)
                ack = 0
                ack_bitfield = 0
                pdu = [ secuencia, ack, ack_bitfield, data] #armamos la pdu
                #enviamos el paquete
                                
                self.socketMsg.send(pdu, (self.host_server, self.port_server) )
                QUEUE_WAIT_ACKS[secuencia]= ( pdu, int(datetime.datetime.now().time().strftime('%s')) ) #actualizamos la lista de espera por Acks
                print pdu, '- RTT:',RTT, ' - Retransmisiones: ', CANT_RETRANSMISIONES
                #enviamos 30 por segundo en estado GOOD y 10 paquetes en estado BAD
                if ESTADO_RED=='GOOD':
                    time.sleep(1/30)  #Si el estado de la red es bueno envia 30 paquetes por segundos
                else:
                    time.sleep(1/10)   #Si el estado de la red es malo envía 10 paquetes por segundos
                
#                if ( (ESTADO_RED == 'GOOD' and cont >= 30 ) or (ESTADO_RED == 'BAD' and cont >= 10 ) ):
                
                """                
                    print "Cantidad de paquetes por segundo: ", cont , ' retransmisiones: ', CANT_RETRANSMISIONES,'/', retransmisionesTotales, ' - RTT', RTT, ' - ESTADO ', ESTADO_RED
                    cont=0
                    retransmisionesTotales+=CANT_RETRANSMISIONES
                    CANT_RETRANSMISIONES = 0
                    time.sleep(1)


                    threadReliableAcks.shutdown_flag.set()
                    threadDetectingLostPackets.shutdown_flag.set()
                    threadFlowCongestion.shutdown_flag.set()            
                    threadReliableAcks.join()
                    threadDetectingLostPackets.join()
                    threadFlowCongestion.join()
                    self.socket_client.close()
                    
                    sys.exit()
                """                
                cont+=1               
                secuencia+=1 
                cantPaquetes+=1
        except ServiceExit:
            threadReliableAcks.shutdown_flag.set()
            threadDetectingLostPackets.shutdown_flag.set()
            threadFlowCongestion.shutdown_flag.set()            
            threadReliableAcks.join()
            threadDetectingLostPackets.join()
            threadFlowCongestion.join()
            self.socket_client.close()
        print('Exiting main program')


class ReliableAcks(Thread):
    def __init__(self, socketMsg):
        self.socketMsg = socketMsg
        self.shutdown_flag = Event()
        Thread.__init__(self)
   
    def run(self):
        global QUEUE_WAIT_ACKS
        global RTT
        while not self.shutdown_flag.is_set():
            
            try:
                pdu, address = self.socketMsg.recv()
            except IOError as e:  # and here it is handeled
                if e.errno == errno.EWOULDBLOCK:
                    "error por socket non-blockeante"
                    continue
            #descomponemos la pdu en los campos del header y data
            secuencia = pdu[0]
            ack = pdu[1]
            ack_bitfield = pdu[2]   #entero
            data = pdu[3]
            
            binario_bitfield = (bin(ack_bitfield)[2:]).zfill(32) #convertimos el campo bitfield en binario para el control de los flags
            i=0
            for bit in binario_bitfield: #Verificacion de bits del ackbitfield
                if bit=='1': #Si el bit es igual 1 significa que el paquete ha sido recibido
                    secuencia= ack - i
                    pdu, tiempo_paquete = QUEUE_WAIT_ACKS.get(secuencia, (None, None) )
                    if not tiempo_paquete is None:
                        rtt_paquete = int(datetime.datetime.now().time().strftime('%s')) - tiempo_paquete
                        RTT = RTT + ( (rtt_paquete - RTT) * 0.1)   #promedio móvil exponencialmente suavizado
                        QUEUE_WAIT_ACKS.pop(secuencia, None) #si recibimos ack, lo eliminamos de la lista de espera por ACKs
                else :
                    secuencia= ack - i
#                        print "Paquete numero "+str(secuencia) +" NO recibido"
                i+=1

class DetectingLostPackets(Thread):
    def __init__(self, socketMsg, host, port):
        self.socketMsg = socketMsg 
        self.host_server = host
        self.port_server = port
        self.shutdown_flag = Event()
        Thread.__init__(self)

    def run(self):
        global QUEUE_WAIT_ACKS
        global CANT_RETRANSMISIONES
        
        while not self.shutdown_flag.is_set():
            time.sleep(0.5)
            for secuencia in QUEUE_WAIT_ACKS.keys():
                pdu, tiempo_paquete = QUEUE_WAIT_ACKS.get(secuencia, (None, None) )
                if not tiempo_paquete is None:
                    delta = int(datetime.datetime.now().time().strftime('%s')) - tiempo_paquete                
                    if secuencia in QUEUE_WAIT_ACKS.keys() and delta >= RTT_RETRANSMISION:
                        self.socketMsg.send(pdu, (self.host_server, self.port_server))    #reeviamos los paquetes que hayan superado el RTT_RETRANSMISION
                        QUEUE_WAIT_ACKS[secuencia]= ( pdu, int(datetime.datetime.now().time().strftime('%s')) )  #actualizamos la lista de espera por Acks
                        CANT_RETRANSMISIONES+=1
                    
class FlowCongestion(Thread):
    def __init__(self):
        self.shutdown_flag = Event()
        Thread.__init__(self)

    def run(self):
        global ESTADO_RED
        penalizacion=4
        tiempoCongestion = int(datetime.datetime.now().time().strftime('%s'))   #iniciamos tiempoCongestion
        tiempoOk = int(datetime.datetime.now().time().strftime('%s'))           #iniciamos tiempoOk
        while not self.shutdown_flag.is_set():
            if ( ESTADO_RED == 'GOOD' ):
                #print RTT, RTT_MAX
                if ( RTT > RTT_MAX ):   #si el rtt es mayor al maximo
                    if( (int(datetime.datetime.now().time().strftime('%s')) - tiempoCongestion) < 10 ): #si estuvo en estado GOOD menos de 10 segundos se penaliza
                        penalizacion = penalizacion * 2 if ( (penalizacion * 2) < 60 ) else 60      # maximo 60 seg de penalizacion
                    
                    print "Cambiamos a estado BAD"
                    ESTADO_RED = 'BAD'
                    tiempoCongestion = int(datetime.datetime.now().time().strftime('%s'))   #reniciamos tiempoCongestion
                    tiempoOk = int(datetime.datetime.now().time().strftime('%s'))           #reniciamos tiempoOk
                    
                    continue    #pasamos a la siguiente iteracion
                
                if( (int(datetime.datetime.now().time().strftime('%s')) - tiempoOk) > 10) :   #si estuvo OK más de 10 segundos se reduce la penalizacion
                    penalizacion = penalizacion / 2 if ( (penalizacion / 2) > 1 ) else 1    #minimo 1 segundo de penalizacion
                    tiempoOk = int(datetime.datetime.now().time().strftime('%s'))
            #fin de GOOD
            #inicio BAD
            if ( ESTADO_RED == 'BAD' ):
                if ( RTT > RTT_MAX ):   #si el rtt es mayor al maximo
                    tiempoCongestion = int(datetime.datetime.now().time().strftime('%s'))   #reniciamos tiempoCongestion
                
                if( (int(datetime.datetime.now().time().strftime('%s')) - tiempoCongestion) > penalizacion ): #si estuvo en estado GOOD menos de 10 segundos se penaliza
                    
                    print "Cambiamos a estado GOOD"
                    ESTADO_RED = 'GOOD'
                    tiempoCongestion = int(datetime.datetime.now().time().strftime('%s'))   #reniciamos tiempoCongestion
                    tiempoOk = int(datetime.datetime.now().time().strftime('%s'))           #reniciamos tiempoOk
            #fin BAD
