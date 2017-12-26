#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random
#from AcceptClient import AcceptClient
from threading import Thread
from Msgg import Msg
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname
import time

DIRECTORIO='SERVIDOR'

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
ACCION_ELIMINAR_ARCHIVO = 3
ENVIAR_ARCHIVO = 4
MODIFICAR_ARCHIVO=5
AGREGAR_ARCHIVO=6
ELIMINAR_ARCHIVO=7

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
                print "Comienza un Thread ",addr_client
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
        print pdu_original
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
#            print LISTA_NODOS
        elif accion == ACCION_REMOTO:
            keyRandom = LISTA_NODOS.keys()[ random.randrange(0, len( LISTA_NODOS.keys() ) ) ]  #seleccionamos un nodo al azar
            nodo = LISTA_NODOS[keyRandom]
            socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_slave.connect((nodo[0],int(nodo[1])))
            nodoSlaveMsg = Msg(socket_slave)
            while len(datos) and accion == 1:
                pdu_out = [self.id_master, accion, '', datos]
                nodoSlaveMsg.send(pdu_out) #reenviamos la instruccion del cliente a un nodo slave
#                id_nodo_aux, accion_aux, path, datos_aux 
                pdu_in = nodoSlaveMsg.recv()  #recivimos la respuesta del nodo slave
                self.sockClientMsg.send(pdu_in) #enviamos la respuesta al cliente
                #self.sincronizar(id_nodo_aux, path)
                id_nodo, accion, path, datos = self.sockClientMsg.recv()    #recivimos proxima instruccion
        elif accion == ACCION_COPIAR:
            pathsMaster = self.getPaths()
            print pathsMaster
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
            print "Eliminación de archivo "+path
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
        print "Fin del Thread"
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
    
    """

#Sincroniza el directorio raiz con el path informado por el nodo
    def sincronizar(self, id_nodo, paths):
        print "sincronizar"
        pathsNodoSlave=paths.split(':')
        for index in range(len(pathsNodoSlave)):
            pathsNodoSlave[index] = self.cambiarDirectorioRaiz(pathsNodoSlave[index], self.raiz)
        pathsMaster=self.getPaths()
        for pathMaster in pathsMaster:
            if pathMaster in pathsNodoSlave: #Si existe el pathMaster, no se realizaron cambios
                pathsNodoSlave.remove(pathMaster)
            else:                                       
                self.eliminarArchivo(id_nodo, pathMaster) #Si no existe existe el pathMaster, hay que eliminarlo
        for pathNodoSlave in pathsNodoSlave:
             #Los path restantes de la lista de pathNodoSlave son archivos agregados 
            print 'agregar ', pathNodoSlave
            self.agregarArchivo(id_nodo, pathNodoSlave)

#Elimina el archivo en el nodo master y en resto de los nodos slave
    def eliminarArchivo(self, id_nodo, pathArchivo):
        remove(pathArchivo) #Elimina el archivo del NodoMaster
        for key_nodo, address in LISTA_NODOS.items():
            if key_nodo != id_nodo:
                socket_slave= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_slave.connect(address)
                Msg(socket_slave).send(self.id_master, ACCION_ELIMINAR_ARCHIVO, pathArchivo, '' )
                socket_slave.close()
                
#Método agregarArchivo. Se encarga de agregar los archivos a los demas equipos. Toma como argumento el path del archivo y la IP, PUERTO del equipo del archivo agregado. 
    def agregarArchivo(self, id_nodo, pathArchivo):
        self.sockClientMsg.send(self.id_master, ENVIAR_ARCHIVO, pathArchivo, '')
        id_nodo, accion, path, datos = self.sockClientMsg.recv()
       #Pedir archivo
        archivoNuevo=open(pathArchivo,'w') 
        archivoNuevo.write(datos) #Copia el archivo al directorio del Servidor Central
        archivoNuevo.close()
        
       try:
         socketServidorEquipoCopiarArchivo.connect((host,int(puerto)))
         socketServidorEquipoCopiarArchivo.sendall(pdu) #Envía solicitud de copia de archivo al equipo.
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

