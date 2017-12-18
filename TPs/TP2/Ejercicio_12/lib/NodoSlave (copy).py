#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from Msg import Msg
from AcceptClient import AcceptClient
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join

SEP=':'
DIRECTORIO='SLAVE'

class NodoSlave:
### Class server Remote
    def __init__(self, host = '0.0.0.0', port = 8001, host_master='0.0.0.0', port_master=8000, nro_nodo = 0, log = "log.txt", recv_buffer = 1024, listen = 5):
        self.host = host
        self.port = port
        self.host_master = host_master
        self.port_master = port_master
        self.nro_nodo = nro_nodo
        self.directorio = DIRECTORIO+str(self.nro_nodo)
        self.recv_buffer = recv_buffer
        self.listen = listen
        self.log = log
        self.copiarMaster()

    def copiarMaster(self):
        socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketMaster.connect((self.host_master, self.port_master))
        Msg(socketMaster).send(2,'')
        accion, datos = Msg(socketMaster).recv()
        while datos != '':
            path=datos.split(SEP)[0]
            datosArchivo=datos.split(SEP)[1]
            subpath=path.split('/')
            subpath[0]= self.directorio #reemplazamos el directorio por el correspondiente del slave
            direct=subpath[0]
            while len(subpath)>1:
                if not exists(direct):
                    mkdir(direct)
                direct+='/'+subpath[1]
                subpath.remove(subpath[0])
            archivo = open(direct,'w')
            archivo.write(datosArchivo)
            archivo.close()
            accion, datos = Msg(socketMaster).recv()

    def iniciar_server(self):
    ### Iniciar conexion
        self.socket_server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#        print "Corriendo servidor - %s:%s" % (self.host, self.port)
#        self.socket_server.bind((self.host, self.port)) 
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
                AcceptClient(conn_client,self.recv_buffer, self.directorio, self.log).start()
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
           
    #Método crearPathsDirectorio. Devuelve un String con todos los paths del directorio.
    def crearPathsDirectorio(self):
        paths=''
        if not exists(self.directorio):
            mkdir(self.directorio)
        for ruta, subdirectorio, ficheros in walk(self.directorio):
           subdirectorio.sort()
           for nombreFichero in ficheros:
              rutaCompleta = join(ruta, nombreFichero)
              paths+=rutaCompleta+':'
        return paths[:-1]
