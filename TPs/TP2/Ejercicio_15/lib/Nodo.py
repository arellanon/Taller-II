#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random, sys
#from AcceptClient import AcceptClient
from threading import Thread, Event
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname
import time
import signal
from ServiceExit import ServiceExit

INDICE = {}
INDICE_ARCHIVO = {}

def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit

class Nodo:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8000, folder = "Folder", log = "log.txt", recv_buffer = 1024):
        self.host = host
        self.port = port
        self.folder = folder        
        self.log = log
        self.recv_buffer = recv_buffer

    def iniciar_server(self):
    ### Iniciar conexion
        signal.signal(signal.SIGTERM, service_shutdown)
        signal.signal(signal.SIGINT, service_shutdown)
        
        try:
            threadEnviarActualizaciones = EnviarActualizaciones(self.folder)
            threadEnviarActualizaciones.start()
            threadRecibirActualizaciones = RecibirActualizaciones(self.host, self.port, self.recv_buffer)
            threadRecibirActualizaciones.start()
            while True:
                print "Presionar Ctrl+C para salir."                
                raw_input('Pulse una tecla para mostrar el listado de documentos...')
                system ("clear")

                self.construirIndiceArchivos()

                print "-----------------------------------------------------------------"
                print "ARCHIVO                             - NODO                       |"
                print "-----------------------------------------------------------------"                
                for archivo in INDICE_ARCHIVO.keys():
                    for nodo in INDICE_ARCHIVO[archivo]:
                        print  "Archivo: ", archivo, " - nodo: ", nodo

#                print INDICE_ARCHIVO
                print "\nCantidad de nodos: ", len(INDICE.keys())
                print "Cantidad de archivos: ", len(INDICE_ARCHIVO.keys())
                
                time.sleep(0.5)
                
        except ServiceExit:
            threadEnviarActualizaciones.shutdown_flag.set()
            threadRecibirActualizaciones.shutdown_flag.set()
            threadEnviarActualizaciones.join()
            threadRecibirActualizaciones.join()
        print('Exiting main program')


    def construirIndiceArchivos(self):
        global INDICE_ARCHIVO
        INDICE_ARCHIVO = {}
        for nodo in INDICE.keys():
            for archivo in INDICE[nodo]:
                if not archivo in INDICE_ARCHIVO.keys():
                    INDICE_ARCHIVO[archivo] = []
                    INDICE_ARCHIVO[archivo].append(nodo)
                else: 
                    INDICE_ARCHIVO[archivo].append(nodo)

class EnviarActualizaciones(Thread):
    def __init__(self, folder):
        self.raiz = folder
        self.shutdown_flag = Event()        
        Thread.__init__(self)

    def run(self):
        global INDICE
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        ports = [ 8000, 8001, 8002, 8003, 8004, 8005]
        
        while not self.shutdown_flag.is_set():
#            time.sleep(1)
            data = self.getPaths()
            for port in ports:
                self.socket_client.sendto(data, ('<broadcast>', port) )
        #cerramos el socket
        ### notificamos que nos desconectamos enviando paquetes vacios
        data = ''
        for port in ports:
                self.socket_client.sendto(data, ('<broadcast>', port) )
        self.socket_client.close()

    def getPaths(self):
        paths=''
        if not exists(self.raiz):
            mkdir(self.raiz)
        for ruta, subdirectorio, ficheros in walk(self.raiz):
            ###
            lista = ruta.split('/')
            lista[0] = '$RAIZ'
            ruta = join(*lista)
            ###
            subdirectorio.sort()
            for nombreFichero in ficheros:
                rutaCompleta = join(ruta, nombreFichero)
                paths+=rutaCompleta+':'
        return paths[:-1]


class RecibirActualizaciones(Thread):
    def __init__(self, host, port, recv_buffer):
        self.host_server = host
        self.port_server = port
        self.recv_buffer = recv_buffer
        self.shutdown_flag = Event()        
        Thread.__init__(self)

    def run(self):
        global INDICE
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket_server.bind((self.host_server, self.port_server))
        
        while not self.shutdown_flag.is_set():
#            time.sleep(1)
            data, address = self.socket_server.recvfrom(self.recv_buffer)
            if data != '':
                INDICE[address] = data.split(":")   #agregamos el nodo con sus archivos al indice
            else :
                INDICE.pop(address, None)   #eliminamos el nodo del indice
        #cerramos el socket
        self.socket_server.close()
