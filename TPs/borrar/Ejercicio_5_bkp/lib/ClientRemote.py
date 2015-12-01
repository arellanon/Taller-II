#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from os import system
from Hash import Hash
from getpass import getpass

TAG=":"

class ClientRemote:
    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def sesion(self, user):
        try:
             while True:
                comando = raw_input (user +"@"+user+":~ $ ")
                if len(comando):
                  self.client_socket.send(comando)
                  out = self.client_socket.recv(self.recv_buffer)
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
        datosParaCifrar = self.client_socket.recv(self.recv_buffer)
        clavePublica= datosParaCifrar.split(TAG)[0]
        semilla_tamano= int(datosParaCifrar.split(TAG)[1])
        num_iteraciones= int(datosParaCifrar.split(TAG)[2])
        aes_multiplo= int(datosParaCifrar.split(TAG)[3])
        flag=False
        while not flag:
            user = raw_input ("user: ")
            password = getpass("password: ")
            datos = user +TAG +password
            datosCifrado = Hash().cifrar(datos, clavePublica, semilla_tamano, num_iteraciones,aes_multiplo)
            self.client_socket.send(datosCifrado) 
            acceso = self.client_socket.recv(self.recv_buffer)
            if int(acceso) ==1:
                system ("clear")
                print "Presione Ctl + C para salir."
                flag=True
                self.sesion(user) 
            else:
                print "Acceso denegado!"
        self.cerrar()

    def cerrar(self):
        ### Cerrar conexion
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except Exception as e:
                print "ERROR: No se puede cerrar el socket.", e
