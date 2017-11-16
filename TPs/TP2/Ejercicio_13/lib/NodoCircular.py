#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from select import select
import socket 
from sys import argv
import sys
import argparse
from datetime import datetime
from os import system
from os.path import exists
from time import time, sleep
from Msg import Msg

RELLENO = ' '
TAMANO_ID= 4
BUFF_SIZE = 256

class NodoCircular(object):
    def __init__(self, id_nodo, host, port, buff_size = 256, listen = 5, TTL = 10):
        self.id_nodo = id_nodo 
        self.host = host
        self.port = port
        self.buff_size = buff_size #Definirá el tamano de la PDU
        self.listen = listen
        self.socket_izq = None
        self.socket_der = None
        if self.id_nodo == 0 :
            self.turno = True
        else :
            self.turno = False
        
    def iniciar_server(self):
        try:
            self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                print "Corriendo servidor - %s:%s" % (self.host, self.port)
                self.socket_server.bind((self.host, self.port))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket."
                self.socket_server.close()
                import sys
                sys.exit(1)            
            #self.conectando_nodos()
        except KeyboardInterrupt:
            print "\nServidor finalizado."

    def conectando_nodos(self, lista_nodos):
        self.iniciar_server()
        self.socket_server.listen(self.listen)
        inputs = [self.socket_server, sys.stdin]
        #Bucle hasta establecer conexciones para los nodos izquierdo y derecho
        while (self.socket_der == None or self.socket_izq == None):
            listo_para_leer,_,_ = select(inputs,[],[])
            for elemento in listo_para_leer:
                if elemento == self.socket_server and self.socket_der == None:
                    self.socket_der, client_der = self.socket_server.accept()
                    self.socket_der.send('OK')
                    print 'Nodo derecho: ', self.socket_der.getpeername()                   
                elif elemento == self.socket_server and self.socket_der != None:
                    socket_aux, client_aux = self.socket_server.accept()
                    socket_aux.send('NOK')
                    socket_aux.close()
                elif elemento == sys.stdin and self.socket_izq == None:
                    opcion = sys.stdin.readline()[:-1]
                    if opcion.upper() == "C":
                        print lista_nodos    
                        id_nodo = raw_input(" Escriba ID del nodo que desea conectarse: ")
                        nodo_izq = lista_nodos[int(id_nodo)]
                        self.socket_izq= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        try:
                            self.socket_izq.connect(nodo_izq) #Intenta conectar con el nodo.
                            print 'Nodo izquierdo: ', self.socket_izq.getpeername()
                            msg = self.socket_izq.recv(self.buff_size)
                            if msg != 'OK':
                                self.socket_izq = None
                                print "El nodo ya tiene una conexion establecida"
                                self.socket_izq.close()    
                        except:
                            print  "No se pudo conectar con el cliente: "
                            sleep(2)
        print 'Nodo derecho: ', self.socket_der.getpeername()
        print 'Nodo izquierdo: ', self.socket_izq.getpeername()
        
        

#Método anilloLogico. Permite el envio de mensaje del nodo origen (cuando corresponda) al nodo saliente y la entrada de PDUs del nodo entrante 
    def anilloLogico(self):
        finalizar = False
        circulando = False
        inputs = [self.socket_der, sys.stdin]
        if self.id_nodo ==0:
            print "Nodo ID 0. Es su turno de enviar mensaje, presione E para enviar. S para finalizar"  
        else:
            print "Nodo ID "+str(self.id_nodo) +". Esperando mensajes... No puede enviar mensajes por que no es su turno"
        while not finalizar:
            listo_para_leer,_,_ = select(inputs,[],[])
            for elemento in listo_para_leer:
                if elemento == sys.stdin: 
                    opcion = sys.stdin.readline()[:-1]                     
                    if opcion.upper() == "E":
                        IDDestino = 2
                        mensaje = "Hola mundo, desde 0"
                        Msg(self.socket_izq).send(self.id_nodo, IDDestino, 0, 0, 0, mensaje)
                        print "se envio: ", mensaje, self.socket_izq.getpeername()                        
                        circulando = True
                    self.turno=0               
                    TTLinicio = time()
                    if self.id_nodo == 0 and opcion.upper() == "S" : #Si es el nodo ID 0 puede permitir finalizar el programa.
                        finalizar = True
                        Msg(self.socket_izq).send(self.id_nodo, 0, 0, 0, 1, '')
                if elemento == self.socket_der :
                    IDOrigen, IDDestino, turno, recibido, fin, mensaje = Msg(self.socket_der).recv()
#                   print 'IDOrigen: ', IDOrigen,'IDDestino :', IDDestino,' : ',mensaje,' turno: ',turno, ' recibido: ', recibido,'fin: ',fin
                    if fin: #Significa que llegó mensaje con el comando de finalizacion
                        finalizar = True
                        Msg(self.socket_izq).send(IDOrigen, IDDestino, turno, recibido, fin, mensaje)
                    elif turno==1: #Significa que el nodo anterior terminó de mandar mensajes por lo que le da el lugar a este nodo.
                        self.turno=1
                        if self.id_nodo == 0:
                            print "Nodo ID 0. Es su turno de enviar mensaje, presione E para enviar. S para finalizar"  
                        else:
                            print "Nodo ID "+str(self.id_nodo) +". Es su turno de enviar mensaje, presione E para enviar"
                    elif IDDestino == self.id_nodo: #Significa que el mensaje del nodo origen era destinado a este nodo.
                        print "Mensaje recibido del nodo ID "+str(IDOrigen)+": "+mensaje  
                        Msg(self.socket_izq).send(IDOrigen, IDDestino, 0, 1, 0, mensaje)
                    elif IDOrigen == self.id_nodo: #Significa que el mensaje volvio al origen por lo que le da lugar al siguiente a nodo a que transmita.
                        if recibido==1: #Si el byte recibido estaba activado entonces significa que el mensaje llego a destino
                            print "EL mensaje ah llegado al destino "+str(IDDestino)
                            print "Fin de envio de mensajes. Es el turno del siguiente nodo\n"
                            Msg(self.socket_izq).send(self.id_nodo, 0, 1, 0, 0, '')                         
                            circulando=False                                
                        else:
                            print "EL mensaje no ah llegado al destino "+str(IDDestino)
                    else: #Significa que el mensaje no era destinado para este nodo                    
                        Msg(self.socket_izq).send(IDOrigen, IDDestino, turno, recibido, fin, mensaje)
            if circulando: #Si los mensajes estan circulando en la red controla que el TTL no sea excedidio.
                TTLfinal=time()
                TTL = TTLfinal - TTLinicio
                if TTL > 10:
                    print "TTL maximo alcanzado! Los mensajes se han perdido en la red, el anillo no esta completo\n"
                    finalizar=True       
