#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket 
from sys import argv
import sys
from datetime import datetime
from threading import Thread
from os import system
from os.path import exists
import subprocess
from datetime import datetime
from Msg import Msg
import os

DIRECTORIO='SERVIDOR' #Directorio a sincronizar

class AcceptClient(Thread):
    def __init__(self, conn_client, recv_buffer, directorio, log):
        self.conn_client = conn_client
        self.user = "usuario"
        self.recv_buffer = recv_buffer
        self.directorio = directorio
        self.log = log
        Thread.__init__(self)

    def run(self):
        accion, datos = Msg(self.conn_client).recv()
        print accion
        self.iniciarSesion(self.user, datos) # Permite el acceso al cliente. Inicia la maquina remota

    def iniciarSesion(self, usuario, comando):
        print "Inicio de sesion: "+usuario
        sesion = 'Usuario: ' +usuario +" "+ str(self.conn_client.getpeername())+' ingreso: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
        ejecutando = True   
        try:
            while ejecutando==True:
                if len(comando):
                    #Ejecutar comando
                    p = subprocess.Popen(comando, cwd=self.directorio, stdout=subprocess.PIPE, shell=True) 
                    (salida, err) = p.communicate()
                    if salida =="": 
                        error = "Comando Inexistente "
                        Msg(self.conn_client).send(1, error)                      
                    else:
                        Msg(self.conn_client).send(1, str(salida))                                          
                    print "usuario: "+usuario+ " - comando: "+comando
                    sesion += usuario +"@"+usuario+":~$ " + comando + "\n"+salida 
                else:
                    ejecutando=False
                    print "Fin de sesion: "+usuario
                    sesion += "Usuario " +usuario +" "+ str(self.conn_client.getpeername())+' salio del sistema el: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
                    self.escribirLog(sesion)
                    self.conn_client.close()
                accion, comando = Msg(self.conn_client).recv() 
        except:     
            sesion += "Usuario " +usuario +" "+ str(self.conn_client.getpeername())+' salio del sistema el: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
            self.escribirLog(sesion)  
            self.conn_client.close()

    def escribirLog(self, sesion):
        log = open(self.log, 'a')
        log.write(sesion +'\n')
        log.close()
