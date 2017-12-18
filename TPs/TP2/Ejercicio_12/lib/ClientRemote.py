#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from os import system
#from Hash import Hash
from getpass import getpass
from Msg import Msg

class ClientRemote:
    def __init__(self, host = '0.0.0.0', port = 8000, user = 'usuario', recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.user = user

    def sesion(self, user):
        try:
             while True:
                comando = raw_input (user +"@"+user+":~ $ ")
                if len(comando):
                  Msg(self.client_socket).send(1, comando)
#                  out = self.client_socket.recv(self.recv_buffer)
                  accion, out = Msg(self.client_socket).recv()
                  print out
        except:
           print "\nchau!.\n "

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
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
