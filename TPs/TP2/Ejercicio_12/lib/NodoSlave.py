#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from Msg import Msg
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname, getmtime
from threading import Thread
import subprocess
from datetime import datetime
import os
from sys import argv
import sys
import time

DIRECTORIO='SLAVE'

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
AGREGAR_ARCHIVO=3
ELIMINAR_ARCHIVO=4
MODIFICAR_ARCHIVO=5

class NodoSlave:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8001, log = "log.txt", recv_buffer = 1024, listen = 5):
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = listen
        self.log = log
        self.inicializarNodo()

    def inicializarNodo(self):
        self.host_master = raw_input("Ingrese la IP del Master: ")
        self.port_master = raw_input("Ingrese el puerto del Master: ")       
        self.port_master = int(self.port_master)
        #Me conecto con el socket master
        socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketMaster.connect((self.host_master, self.port_master))
        socketMasterMsg = Msg(socketMaster)

        #Registrar NODO_SLAVE
        datos=str(self.host)+":"+str(self.port)
        pdu = [0, ACCION_REGISTRAR, '', datos]
        socketMasterMsg.send(pdu)
        id_nodo, accion, path, data = socketMasterMsg.recv()
        self.id_nodo = int(data)
        self.raiz = DIRECTORIO+str(self.id_nodo)

        #REPLICAR DIRECTORIO MASTER
        socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketMaster.connect((self.host_master, self.port_master))
        socketMasterMsg = Msg(socketMaster)

        pdu = [self.id_nodo, ACCION_COPIAR, '', '']
        socketMasterMsg.send(pdu)
        id_nodo, accion, path, datos = socketMasterMsg.recv()
        print "Copiar directorio master"
        while path != '':
            subpath=path.split('/')
            subpath[0]= self.raiz #reemplazamos el directorio por el correspondiente del slave
            direct=subpath[0]
            while len(subpath)>1:
                if not exists(direct):
                    mkdir(direct)
                direct+='/'+subpath[1]
                subpath.remove(subpath[0])
            archivo = open(direct,'w')
            archivo.write(datos)
            archivo.close()
            id_nodo, accion, path, datos = socketMasterMsg.recv()

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
                ThreadSlave(sockClientMsg, self.host_master, self.port_master, self.id_nodo, self.recv_buffer, self.raiz, self.log).start() #Por cada conexion aceptada se genera un thread
        except KeyboardInterrupt:
            print "\nServidor Apagado"
        self.cerrar_server()

    def cerrar_server(self):
    ### Cerrar conexion
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            self.socket_server.close()
            import sys
            sys.exit(1)
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
            
            
class ThreadSlave(Thread):
    def __init__(self, sock_client_msg, host_master, port_master, id_nodo, recv_buffer, directorio, log):
        self.sockClientMsg = sock_client_msg
        self.host_master = host_master
        self.port_master = port_master
        self.id_nodo = id_nodo
        self.user = "usuario"
        self.recv_buffer = recv_buffer
        self.raiz = directorio
        self.log = log
        Thread.__init__(self)

    def run(self):
        id_nodo, accion, path, datos = self.sockClientMsg.recv()
        path = self.cambiarDirectorioRaiz(path, self.raiz)
        if accion == ACCION_REMOTO:        
            comando = datos
            while len(comando):
                usuario = 'usuario'                
                print "Inicio de sesion: "+usuario
                p = subprocess.Popen(comando, cwd=self.raiz, stdout=subprocess.PIPE, shell=True) 
                directorioAntes = self.getDirectorios() #guardamos el estado del directorio antes de ejecutar el comando
                (salida, err) = p.communicate()
                directorioDespues = self.getDirectorios() #guardamos el estado del directorio despues de ejecutar el comando
                
                #Verificamos las modificaciones realizadas en el direcorio y las notificamos al nodo master
                modificar = {k:v for (k,v) in directorioAntes.items() if k in directorioDespues and v != directorioDespues.get(k, None) }
                agregar = {k:v for (k,v) in directorioDespues.items() if k not in directorioAntes}
                eliminar = {k:v for (k,v) in directorioAntes.items() if k not in directorioDespues}
                
#                print "modificacion: ", modificar
#                print "agregar: ", agregar
#                print "eliminar: ", eliminar
                
                #Revisamos los diccionario y enviamos las actualizaciones al nodo master               
                for path in agregar.keys():                    
                    archivo=open(path,'r')
                    datosArchivo = archivo.read()
                    archivo.close()
                    time.sleep(0.01)                   
                    socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socketMaster.connect((self.host_master, self.port_master))
                    socketMasterMsg = Msg(socketMaster)
                    pdu = [self.id_nodo, AGREGAR_ARCHIVO, path, datosArchivo]
                    socketMasterMsg.send(pdu)

                for path in eliminar.keys():
                    socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socketMaster.connect((self.host_master, self.port_master))
                    socketMasterMsg = Msg(socketMaster)
                    pdu = [self.id_nodo, ELIMINAR_ARCHIVO, path, '']
                    socketMasterMsg.send(pdu)                
                
                for path in modificar.keys():                    
                    archivo=open(path,'r')
                    datosArchivo = archivo.read()
                    archivo.close()
                    time.sleep(0.01)
                    socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socketMaster.connect((self.host_master, self.port_master))
                    socketMasterMsg = Msg(socketMaster)
                    pdu = [self.id_nodo, MODIFICAR_ARCHIVO, path, datosArchivo]
                    socketMasterMsg.send(pdu)
                
                paths = ''
                pdu = [self.id_nodo, ACCION_REMOTO, paths, str(salida)]
                self.sockClientMsg.send(pdu)
                print "usuario: "+usuario+ " - comando: "+comando
                id_nodo, accion, path, comando = self.sockClientMsg.recv()
        elif accion == AGREGAR_ARCHIVO:
            archivo = open(path,'w')
            archivo.write(datos)
            archivo.close()
            print "Se agrego el archivo: "+path
        elif accion == ELIMINAR_ARCHIVO:
            remove(path)
            print "Se elimino el archivo: "+path
        elif accion == MODIFICAR_ARCHIVO:
            remove(path)
            archivo = open(path,'w')
            archivo.write(datos)
            archivo.close()
            print "Se modifico el archivo: "+path                     
            
    def getDirectorios(self):
        paths={}
        if not exists(self.raiz):
           mkdir(self.raiz)
        for ruta, subdirectorio, ficheros in walk(self.raiz):
#            print ruta, subdirectorio, ficheros
            subdirectorio.sort()
            if len(ficheros) > 0:
                for nombreFichero in ficheros:
                   rutaCompleta = join(ruta, nombreFichero)
                   timeModification = time.ctime(getmtime(rutaCompleta))
                   paths[rutaCompleta] = timeModification
#            else :
#                paths[ruta] = None
        return paths
    
#Cambia el directorio raiz del path
    def cambiarDirectorioRaiz(self, path, raiz):
        lista = path.split('/')
        lista[0] = raiz
        path = join(*lista)
        return path
