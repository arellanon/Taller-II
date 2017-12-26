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

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
ACCION_ELIMINAR_ARCHIVO = 3


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
            self.socket_server.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

class ThreadMaster(Thread):
    def __init__(self, conn_client, lista_nodos):
        self.conn_client = conn_client
        self.lista_nodos = lista_nodos
        self.raiz = DIRECTORIO
        self.id_master = 0
        Thread.__init__(self)

    def run(self):
        id_nodo, accion, path, datos = Msg(self.conn_client).recv()
        if  accion == ACCION_REGISTRAR:
            nodo = datos.split(':')
            id_nodo = len(self.lista_nodos) + 1 
            nodo.append(id_nodo)
            self.lista_nodos.append(nodo)
            print self.lista_nodos
            Msg(self.conn_client).send(self.id_master, 0, '', str(id_nodo) )
        elif accion == ACCION_REMOTO:
            nodo1 = self.lista_nodos[ random.randrange(0, len( self.lista_nodos ) ) ]
            socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_slave.connect((nodo1[0],int(nodo1[1])))
            while len(datos) and accion == 1:
                Msg(socket_slave).send(self.id_master, accion, '', datos) #reenviamos la instruccion del cliente a un nodo slave
                id_nodo_aux, accion_aux, path, datos_aux = Msg(socket_slave).recv()    #recivimos la respuesta del nodo slave
                print 'accion: ', accion, ' datos: ', datos
                print path
                Msg(self.conn_client).send(id_nodo_aux, accion_aux, '', datos_aux) #enviamos la respuesta al cliente
#                id_nodo, accion, path, datos = Msg(socket_slave).recv()  #recivimos los paths de sincronizacion
                self.sincronizar(path, id_nodo_aux)
                id_nodo, accion, path, datos = Msg(self.conn_client).recv()    #recivimos proxima instruccion
        elif accion == ACCION_COPIAR:
            pathsMaster = self.getPaths()
            for path in pathsMaster:
                archivo=open(path,'r')
                datosArchivo = archivo.read()
                archivo.close()
                time.sleep(0.01)
                Msg(self.conn_client).send(self.id_master, accion, path, datosArchivo)
            Msg(self.conn_client).send(self.id_master, accion, '', '')
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
        
    def sincronizar(self, paths, id_nodo):
        print "sincronizar"
        #reemplazar raiz
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
                self.eliminarArchivo(pathMaster, id_nodo)
#                print 'eliminar ', pathMaster
        for pathNodoSlave in pathsNodoSlave:
             #Los path restantes de la lista de pathNodoSlave son archivos agregados 
            print 'agregar ', pathNodoSlave

#Método eliminarArchivo. Se encarga de eliminar los archivos de los demás equipos. Toma como argumento el path del archivo y la IP, PUERTO del equipo del archivo eliminado. 
    def eliminarArchivo(self, pathServidor, id_nodo):
        print "ingresamos en eliminar ", id_nodo
        nodos=[]
        for e in self.lista_nodos:
            if e[2] != id_nodo :
                nodos.append(e)    
#        equipos=self.obtenerEquiposRestantes(host,puerto)
        print nodos
        remove(pathServidor) #Elimina el archivo del directorio del Servidor Central
        for nodo in nodos:
            socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_slave.connect((nodo[0],int(nodo[1])))
            Msg(socket_slave).send(self.id_master, 3, pathServidor, '' )
            socket_slave.close()
"""
#Método agregarArchivo. Se encarga de agregar los archivos a los demas equipos. Toma como argumento el path del archivo y la IP, PUERTO del equipo del archivo agregado. 
    def agregarArchivo(self, pathServidor, id_nodo):
        print "ingresamos en eliminar ",id_nodo
        nodos=[]
        for e in self.lista_nodos:
            if e[2] != id_nodo :
                nodos.append(e)
            else :
                nodo_origen = e
        
        socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_slave.connect((nodo_origen[0],int(nodo_origen[1])))
        Msg(socket_slave).send(self.id_master, 4, pathServidor, '' )
        
        
         pdu = socketServidorEquipoCopiarArchivo.recv(self.buff_size)
         tipo, datosArchivo = desencapsularPDU(pdu)
         datos= pathEquipo+SEP+datosArchivo
         pdu = encapsularPDU(TIPO_AGREGAR_ARCHIVO,datos)
         archivoNuevo=open(pathEquipo,'w') 
         archivoNuevo.write(datosArchivo) #Copia el archivo al directorio del Servidor Central
         archivoNuevo.close()
         for equipo in equipos:
            socketServidorEquipoAgregarArchivo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
              socketServidorEquipoAgregarArchivo.connect((equipo[0],int(equipo[1])))
              socketServidorEquipoAgregarArchivo.sendall(pdu) #Envía el path y la copia del archivo a agregar a los demás equipos.
              print "Agregación de archivo "+pathEquipo+" enviada al equipo "+equipo[0]+ ":"+equipo[1]
              self.log("Agregación de archivo "+pathEquipo+" enviada al equipo "+equipo[0]+ ":"+equipo[1]+'\n')    
            except KeyboardInterrupt:
               print "\nSe ha caido la conexion con el Servidor!"
            except:
               print "\nNo se ha podido conectar al Servidor " + host + " puerto " +str(puerto) +". El Servidor se ha caido o no existe. "     
            socketServidorEquipoAgregarArchivo.close()  
       except KeyboardInterrupt:
            print "\nSe ha caido la conexion con el Servidor!"
       except:
            print "\nNo se ha podido conectar al Servidor " + host + " puerto " +str(puerto) +". El Servidor se ha caido o no existe. "
       socketServidorEquipoCopiarArchivo.close() 
"""
