#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from Msgg import Msg
#from AcceptClient import AcceptClient
from os import system,remove, walk, mkdir
#from os.path import exists, isdir, join
from os.path import exists, isdir, join, dirname, getmtime
from threading import Thread
import subprocess
from datetime import datetime
import os
from sys import argv
import sys
import time


SEP=':'
DIRECTORIO='SLAVE'

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
ACCION_ELIMINAR_ARCHIVO = 3
ENVIAR_ARCHIVO = 4
MODIFICAR_ARCHIVO=5
AGREGAR_ARCHIVO=6
ELIMINAR_ARCHIVO=7

class NodoSlave:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8001, host_master='0.0.0.0', port_master=8000, id_nodo = 0, log = "log.txt", recv_buffer = 1024, listen = 5):
        self.host = host
        self.port = port
        self.host_master = host_master
        self.port_master = port_master
        self.id_nodo = id_nodo
        self.raiz = DIRECTORIO+str(self.id_nodo)
        self.recv_buffer = recv_buffer
        self.listen = listen
        self.log = log
        self.copiarMaster()

    def copiarMaster(self):
        socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketMaster.connect((self.host_master, self.port_master))
        self.socketMasterMsg = Msg(socketMaster)
        pdu = [self.id_nodo, ACCION_COPIAR, '', '']
        self.socketMasterMsg.send(pdu)
        id_nodo, accion, path, datos = self.socketMasterMsg.recv()
        print "copiar master"
        print path.split('/')
        print datos
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
            id_nodo, accion, path, datos = self.socketMasterMsg.recv()

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
        print "ingreso a cerrar socket"
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            print "SHUT_RDWR"
            self.socket_server.close()
            import sys
            sys.exit(1)
            print "close()"
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
            
            
class ThreadSlave(Thread):
    def __init__(self, sock_client_msg, host_master, port_master, id_nodo, recv_buffer, directorio, log):
        self.sockClientMsg = sock_client_msg
#        self.socketMasterMsg = sock_master_msg
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
        print 'accion: ', accion, 'datos: ', datos
        if accion == ACCION_REMOTO:        
            comando = datos
            while len(comando):
                usuario = 'usuario'                
                print "Inicio de sesion: "+usuario
#                sesion = 'Usuario: ' +usuario +" "+ str(self.conn_client.getpeername())+' ingreso: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
                p = subprocess.Popen(comando, cwd=self.raiz, stdout=subprocess.PIPE, shell=True) 
                directorioAntes = self.getDirectorios() #guardamos el estado del directorio antes de ejecutar el comando
                (salida, err) = p.communicate()
                directorioDespues = self.getDirectorios() #guardamos el estado del directorio despues de ejecutar el comando
                
                #Verificamos las modificaciones realizadas en el direcorio y las notificamos al nodo master
                modificar = {k:v for (k,v) in directorioAntes.items() if k in directorioDespues and v != directorioDespues.get(k, None) }
                agregar = {k:v for (k,v) in directorioDespues.items() if k not in directorioAntes}
                eliminar = {k:v for (k,v) in directorioAntes.items() if k not in directorioDespues}
                
                print "modificacion: ", modificar
                print "agregar: ", agregar
                print "eliminar: ", eliminar  
                
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
                    print pdu
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
                paths= self.getPaths()

                pdu = [self.id_nodo, ACCION_REMOTO, paths, str(salida)]
                self.sockClientMsg.send(pdu)
                print "usuario: "+usuario+ " - comando: "+comando
#                sesion += usuario +"@"+usuario+":~$ " + comando + "\n"+salida             
                id_nodo, accion, path, comando = self.sockClientMsg.recv()
        elif accion == AGREGAR_ARCHIVO:
            archivo = open(path,'w')
            archivo.write(datos)
            archivo.close()           
        elif accion == ELIMINAR_ARCHIVO:
            remove(path)
            print "Eliminación de archivo "+path
        elif accion == MODIFICAR_ARCHIVO:
            remove(path)
            archivo = open(path,'w')
            archivo.write(datos)
            archivo.close()            
            
    def getPaths(self):
        paths=''
        if not exists(self.raiz):
            mkdir(self.raiz)
        for ruta, subdirectorio, ficheros in walk(self.raiz):
           subdirectorio.sort()
           for nombreFichero in ficheros:
              rutaCompleta = join(ruta, nombreFichero)
              paths+=rutaCompleta+':'
        return paths[:-1]
        
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
