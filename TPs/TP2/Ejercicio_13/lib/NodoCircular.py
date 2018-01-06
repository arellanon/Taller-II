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

class NodoCircular(object):
    def __init__(self, id_nodo, host, port, host_dst, port_dst, buff_size = 256, listen = 5):
        self.id_nodo = id_nodo 
        self.host = host
        self.port = port
        self.host_dst = host_dst
        self.port_dst = port_dst
        self.buff_size = buff_size
        self.listen = listen
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
        except KeyboardInterrupt:
            print "\nServidor finalizado."
    
    def conectando_nodos(self):
        print 'NODO ID: ', self.id_nodo
        self.iniciar_server()
        self.listaMensajes = self.loadFile()
        self.socket_server.listen(self.listen)
        self.socket_izq = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        flag_izq = False
        flag_der = False
        inputs = [self.socket_server, self.socket_izq]
        #Bucle hasta establecer conexiones para los nodos izquierdo y derecho
        while (not flag_der or not flag_izq):
            readable, writable, exceptional = select(inputs,[],[])
            for r in readable:
                if r == self.socket_server and not flag_der:
                    self.socket_der, client_der = self.socket_server.accept()
                    self.socket_der.send('OK')
                    print 'Nodo derecho: ', self.socket_der.getpeername()
                    flag_der = True
                elif r == self.socket_server and flag_der:
                    socket_aux, client_aux = self.socket_server.accept()
                    socket_aux.send('NOK')
                    socket_aux.close()
                elif r == self.socket_izq and not flag_izq:
                    nodo_izq = (self.host_dst, self.port_dst)
                    try:
                        self.socket_izq.connect(nodo_izq) #Intenta conectar con el nodo.
                        msg = self.socket_izq.recv(self.buff_size)
                        if msg == 'OK':
                            flag_izq = True
                            print 'Nodo izquierdo: ', self.socket_izq.getpeername()
                        else:
                            print "El nodo ya tiene una conexion establecida"
                            self.socket_izq.close()
                    except:
#                        print  "No se pudo conectar con el cliente"
                        sleep(2)

#Método anilloLogico. Permite el envio de mensaje del nodo origen (cuando corresponda) al nodo saliente y la entrada de PDUs del nodo entrante 
    def anilloLogico(self):
        finalizar = False
        self.MsgIzq = Msg(self.socket_izq)
        self.MsgDer = Msg(self.socket_der)
        inputs = [self.socket_der, sys.stdin]
        nroMsg = 0
        system ("clear")
        print "Cantidad de mensajes: ", len(self.listaMensajes)
        if self.id_nodo ==0:
            print "Presione cualquier tecla para enviar mensajes. Q para finalizar"
        else:
            print "Esperando turno..."
#            print "Presione cualquier tecla para enviar mensajes."
        while not finalizar:
            readable, writable, exceptional = select(inputs,[],[])
            for r in readable:
                #Entrada de input por teclado
                if self.turno == 1:
                    if r == sys.stdin:
                        opcion = sys.stdin.readline()[:-1]
                        if opcion.upper() != "Q":
                            if nroMsg >= len(self.listaMensajes):
                                nroMsg = 0
                            mensaje = self.listaMensajes[nroMsg]
                            id_dst = mensaje[0]
                            datos = mensaje[1]
                            pdu = [self.id_nodo, id_dst, 0, 0, 0, datos]
                            print "Mensaje N° ", nroMsg," : ", pdu,
                            self.MsgIzq.send(pdu)
                            nroMsg+=1
                        self.turno=0
                        TTLinicio = time()
                        if self.id_nodo == 0 and opcion.upper() == "Q" : #Si es el nodo ID 0 puede permitir finalizar el programa.
                            finalizar = True
                            pdu = [self.id_nodo, 0, 0, 0, 1, '']
                            self.MsgIzq.send(pdu)
                #Recepcion de mensaje nodo derecho
                if r == self.socket_der:
                    pdu = self.MsgDer.recv()
                    id_src, id_dst, turno, recibido, fin, mensaje = pdu
                    if fin: #Significa que llegó mensaje con el comando de finalizacion
                        finalizar = True
                        pdu = [id_src, id_dst, turno, recibido, fin, mensaje]
                        self.MsgIzq.send(pdu)
                    elif turno==1: #Significa que el nodo anterior terminó de mandar mensajes por lo que le da el lugar a este nodo.
                        self.turno=1
                        system ("clear")
                        if self.id_nodo == 0:
                            print "Presione cualquier tecla para enviar mensajes. Q para finalizar"
                        else:
                            print "Presione cualquier tecla para enviar mensajes."
                    elif id_dst == self.id_nodo: #Significa que el mensaje del nodo origen era destinado a este nodo.
                        print "Mensaje recibido: ", pdu
                        pdu = [id_src, id_dst, 0, 1, 0, mensaje]
                        self.MsgIzq.send(pdu)
                    elif id_src == self.id_nodo: #Significa que el mensaje volvio al origen por lo que le da lugar al siguiente a nodo a que transmita.
                        if recibido==1: #Si el byte recibido estaba activado entonces significa que el mensaje llego a destino
                            print "- ACK"                            
                        else:
                            print "- NACK"
                        pdu = [self.id_nodo, 0, 1, 0, 0, '']
                        self.MsgIzq.send(pdu)
                    else: #Significa que el mensaje no era destinado para este nodo
                        pdu = [id_src, id_dst, turno, recibido, fin, mensaje]
                        self.MsgIzq.send(pdu)
  
#Método cargarArchivoMensajes. Carga en una lista todos los mensajes a enviar del nodo.
    def loadFile(self):
        listaMensajes=[]
        if exists("mensajes"+str(self.id_nodo)+".txt"):
            archivo = open("mensajes"+str(self.id_nodo)+".txt",'r')
            lista = archivo.readlines()
            for mensaje in lista:
                id_dst = int(mensaje.split(':')[0])
                mensaje = mensaje.split(':')[1]
                listaMensajes.append( [id_dst, mensaje] )
        else: 
            print "No se pudo cargar el archivo de mensajes"+str(self.id_nodo)+".txt Es el turno del siguiente nodo \n"
        return listaMensajes
