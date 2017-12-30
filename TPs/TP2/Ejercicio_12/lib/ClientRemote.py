#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from os import system
from getpass import getpass
from Msg import Msg

ACCION_REGISTRAR = 0
ACCION_REMOTO = 1
ACCION_COPIAR = 2
AGREGAR_ARCHIVO=3
ELIMINAR_ARCHIVO=4
MODIFICAR_ARCHIVO=5

class ClientRemote:
    def __init__(self, host = '0.0.0.0', port = 8000, user = 'usuario', recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.user = user
        self.id_cliente = 0

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            self.sockClientMsg = Msg(self.client_socket)
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar()
            import sys
            sys.exit(1)
            
        system ("clear")
        system ("clear")
        print "Presione Ctl + C para salir."
        flag=True
        self.sesion(self.user)
        self.cerrar()

    def cerrar(self):
        ### Cerrar conexion
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except Exception as e:
                print "ERROR: No se puede cerrar el socket.", e

    def sesion(self, user):
        try:
            while True:
                comando = raw_input (user +"@"+user+":~ $ ")
                if len(comando):
                    pdu = [self.id_cliente, ACCION_REMOTO, '', comando]
                    self.sockClientMsg.send(pdu)
                    id_nodo, accion, path, out = self.sockClientMsg.recv()
                    print out
        except:
            #Enviamos un mensaje vacio para terminar la conexion con el servidor
            pdu = [self.id_cliente, ACCION_REMOTO, '', '']
            self.sockClientMsg.send(pdu)
            print "\nchau!.\n "
