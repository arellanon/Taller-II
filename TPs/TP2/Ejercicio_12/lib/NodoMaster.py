#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random
#from AcceptClient import AcceptClient
from threading import Thread
from Msg import Msg
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname
import time

DIRECTORIO='SERVIDOR'

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
        lista_nodos = []
        self.socket_server.listen(self.listen)
        try: 
            while True:
                conn_client, addr_client = self.socket_server.accept()
                ThreadMaster(conn_client, lista_nodos).start()
        except KeyboardInterrupt:
            print "\nServidor Apagado"
        self.cerrar_server()

    def cerrar_server(self):
    ### Cerrar conexion
        print "ingreso a cerrar socket"
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            print "SHUT_RDWR"
            self.socket_server.close()
            print "close()"            
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

class ThreadMaster(Thread):
    def __init__(self, conn_client, lista_nodos):
        self.conn_client = conn_client
        self.lista_nodos = lista_nodos
        self.raiz = DIRECTORIO
        Thread.__init__(self)

    def run(self):
        accion, datos = Msg(self.conn_client).recv()
        if  accion == 0:
            self.lista_nodos.append(datos.split(':'))
            print self.lista_nodos
            Msg(self.conn_client).send(0, str(len(self.lista_nodos)))
        elif accion == 1:
            nodo1 = self.lista_nodos[ random.randrange(0, len( self.lista_nodos ) ) ]
            socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_slave.connect((nodo1[0],int(nodo1[1])))
            while len(datos) and accion == 1:
                Msg(socket_slave).send(accion, datos) #reenviamos la instruccion del cliente a un nodo slave
                accion_aux, datos_aux = Msg(socket_slave).recv()    #recivimos la respuesta del nodo slave
                print 'accion: ', accion, ' datos: ', datos
                Msg(self.conn_client).send(accion_aux, datos_aux) #enviamos la respuesta al cliente
                accion, datos = Msg(socket_slave).recv()  #recivimos los paths de sincronizacion
                self.sincronizar(datos)
                accion, datos = Msg(self.conn_client).recv()    #recivimos proxima instruccion
                print "este mensaje se deberia reenviar a un nodo slave"
#        self.iniciarSesion(self.user, datos) # Permite el acceso al cliente. Inicia la maquina remota
        elif accion == 2:
            pathsMaster = self.getPaths()
            for path in pathsMaster:
                archivo=open(path,'r')
                datosArchivo = archivo.read()
                archivo.close()
                datos= path+':'+datosArchivo
                time.sleep(0.01)
                Msg(self.conn_client).send(accion, datos)
            Msg(self.conn_client).send(accion, '')
        self.conn_client.close()
            
#Método getPaths. Devuelve una lista con todos los paths del directorio.
    def getPaths(self):
        paths=[]
        if not exists(self.raiz):
           mkdir(self.raiz)
        for ruta, subdirectorio, ficheros in walk(self.raiz):
           subdirectorio.sort()
           for nombreFichero in ficheros:
              rutaCompleta = join(ruta, nombreFichero)
              paths.append(rutaCompleta)
        return paths
        
    def sincronizar(self, paths):
        print "sincronizar"
        pathsNodoSlave=paths.split(':')
        for index in range(len(pathsNodoSlave)):
            lista = pathsNodoSlave[index].split('/')
            lista[0] = self.raiz
            pathsNodoSlave[index] = join(*lista)
        pathsMaster=self.getPaths()
        for pathMaster in pathsMaster:
            if pathMaster in pathsNodoSlave: #Si el path del directorio raiz esta en el directorio del equipo, no se ha producido ningun cambio 
                pathsNodoSlave.remove(pathMaster) #Eliminar el path de la lista para luego comprobar si se ha agregado un archivo 
            else:  
                #Si el path del directorio raiz no esta en el directorio del equipo,se ha eliminado un archivo. 
                #self.eliminarArchivo(pathServidor,host,puerto) #Eliminar archivo de todos los equipos restantes.
                print 'eliminar ', pathMaster
        for pathNodoSlave in pathsNodoSlave:
             #Los path restantes de la lista de pathNodoSlave son archivos agregados 
            print 'agregar ', pathNodoSlave
