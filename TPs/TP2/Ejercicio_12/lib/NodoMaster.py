#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random
from threading import Thread
from Msg import Msg
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname
import time

DIRECTORIO='SERVIDOR'

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
AGREGAR_ARCHIVO=3
ELIMINAR_ARCHIVO=4
MODIFICAR_ARCHIVO=5

LISTA_NODOS = {}

class NodoMaster:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8000, log = "log.txt", recv_buffer = 1024, listen = 5):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = listen
        self.log = log

    def iniciar_server(self):
    ### Iniciar conexion
        self.socket_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        self.socket_server.listen(self.listen)
        try: 
            while True:
                conn_client, addr_client = self.socket_server.accept()
                sockClientMsg = Msg(conn_client)
                ThreadMaster(sockClientMsg).start()
        except KeyboardInterrupt:
            print "\nServidor Apagado"
        self.cerrar_server()

    def cerrar_server(self):
    ### Cerrar conexion
        print "ingreso a cerrar socket"
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            self.socket_server.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

class ThreadMaster(Thread):
    def __init__(self, conn_client):
        self.sockClientMsg = conn_client
        self.raiz = DIRECTORIO
        self.id_master = 0
        Thread.__init__(self)

    def run(self):
        global LISTA_NODOS
        pdu_original = self.sockClientMsg.recv()
        id_nodo = pdu_original[0]
        accion = pdu_original[1]
        path = pdu_original[2]
        datos = pdu_original[3]
        path = self.cambiarDirectorioRaiz(path, self.raiz)
        if  accion == ACCION_REGISTRAR:
            #Asignamos n° de nodo
            if len(LISTA_NODOS.keys()) > 0:
                id_nodo = max(LISTA_NODOS.keys()) + 1         
            else :
                id_nodo = 1 #si es el primer nodo le asignamos 1
            address = datos.split(':')  #recuperamos la direccion server del nodoSlave
            LISTA_NODOS[id_nodo] = (address[0], int(address[1])) #guardamos la direccion del nodo como tupla
            pdu_out = [self.id_master, ACCION_REGISTRAR, '', str(id_nodo)]
            self.sockClientMsg.send(pdu_out)
        elif accion == ACCION_REMOTO:
            keyRandom = LISTA_NODOS.keys()[ random.randrange(0, len( LISTA_NODOS.keys() ) ) ]  #seleccionamos un nodo al azar
            nodo = LISTA_NODOS[keyRandom]
            socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_slave.connect((nodo[0],int(nodo[1])))
            nodoSlaveMsg = Msg(socket_slave)
            while len(datos):
                pdu_out = [self.id_master, accion, '', datos]
                nodoSlaveMsg.send(pdu_out) #reenviamos la instruccion del cliente a un nodo slave
                pdu_in = nodoSlaveMsg.recv() #recivimos la respuesta del nodo slave
                self.sockClientMsg.send(pdu_in) #enviamos la respuesta al cliente
                id_nodo, accion, path, datos = self.sockClientMsg.recv()    #recivimos proxima instruccion
            #Enviamos el msg de final
            pdu_out = [self.id_master, accion, '', datos]
            nodoSlaveMsg.send(pdu_out) #reenviamos la instruccion del cliente a un nodo slave
        elif accion == ACCION_COPIAR:
            pathsMaster = self.getPaths()
            for path in pathsMaster:
                archivo=open(path,'r')
                datosArchivo = archivo.read()
                archivo.close()
                time.sleep(0.01)
                pdu_out = [self.id_master, accion, path, datosArchivo]
                self.sockClientMsg.send(pdu_out)
            pdu_out = [self.id_master, accion, '', '']
            self.sockClientMsg.send(pdu_out)
        elif accion == AGREGAR_ARCHIVO:
            print "Se agrego el archivo: "+path
            archivo = open(path,'w') #agregamos el archivo en el nodo master y lo restransmitimos a los nodos slaves
            archivo.write(datos)
            archivo.close()
            for key_nodo, address in LISTA_NODOS.items():
                if key_nodo != id_nodo:
                    socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_slave.connect(address)
                    nodoSlaveMsg = Msg(socket_slave)
                    pdu_out = [self.id_master, accion, path, datos]
                    nodoSlaveMsg.send(pdu_out)
                    socket_slave.close()
        elif accion == ELIMINAR_ARCHIVO:
            print "Se elimino el archivo: "+path            
            remove(path) #eliminamos el archivo en el nodo master y lo restransmitimos a los nodos slaves
            for key_nodo, address in LISTA_NODOS.items():
                if key_nodo != id_nodo:
                    socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_slave.connect(address)
                    nodoSlaveMsg = Msg(socket_slave)
                    pdu_out = [self.id_master, accion, path, datos]
                    nodoSlaveMsg.send(pdu_out)
                    socket_slave.close()
        elif accion == MODIFICAR_ARCHIVO:
            print "Se modifico el archivo: "+path
            remove(path)
            archivo = open(path,'w')
            archivo.write(datos)
            archivo.close()
            for key_nodo, address in LISTA_NODOS.items():
                if key_nodo != id_nodo:
                    socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_slave.connect(address)
                    nodoSlaveMsg = Msg(socket_slave)
                    pdu_out = [self.id_master, accion, path, datos]
                    nodoSlaveMsg.send(pdu_out)
                    socket_slave.close()
        self.sockClientMsg.close()
            
#Cambia el directorio raiz del path
    def cambiarDirectorioRaiz(self, path, raiz):
        lista = path.split('/')
        lista[0] = raiz
        path = join(*lista)
        return path
        
#Devuelve una lista con los paths del directorio raiz
    def getPaths(self):
        paths=[]
        if not exists(self.raiz):
           mkdir(self.raiz)
           print "no existe raiz"
        for ruta, subdirectorio, ficheros in walk(self.raiz):
           subdirectorio.sort()
           for nombreFichero in ficheros:
              rutaCompleta = join(ruta, nombreFichero)
              paths.append(rutaCompleta)
        return paths
