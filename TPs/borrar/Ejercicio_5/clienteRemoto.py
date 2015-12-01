#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket 
from sys import argv
import sys
import argparse
from datetime import datetime
from threading import Thread
from os import system
from os.path import exists
from lib.cifrador import Cifrador
from getpass import getpass
import hashlib

buff_size=4096
TAG=":"

#Método iniciarMaquinaRemota. Toma como argumento el nombre de usuario y el Socket Cliente-Servidor. Envia los comandos al servidor, recibe los resultados y lo muestra en pantalla.
def iniciarMaquinaRemota(usuario,clienteSocket):
    ejecutando = True   
    try:
         while ejecutando:
            comando = raw_input (usuario +"@"+usuario+"-System-Product-Name:~$ ")
            if len(comando):
              clienteSocket.send(comando)
              salida = clienteSocket.recv(buff_size)
              print salida
    except:
       print "\nSalida de la Maquina remota.\n "

#Método Principal.
def main(args):
 system ("clear")
 print "-----Conexion al Servidor Remoto Unix-----"
 host_servidor = raw_input (" Escriba la IP del Servidor de maquina remota: ")
 puerto_servidor = raw_input (" Escriba el puerto del Servidor de maquina remota: ")
 clienteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 try:
    clienteSocket.connect((host_servidor,int(puerto_servidor)))
    system ("clear")
    print "     Conexion abierta con el servidor " + host_servidor +" puerto " +str(puerto_servidor)
    datosParaCifrar = clienteSocket.recv(buff_size) #Recibe los datos para cifrar. 
    clavePublica= datosParaCifrar.split(TAG)[0]
    semilla_tamano= int(datosParaCifrar.split(TAG)[1])
    num_iteraciones= int(datosParaCifrar.split(TAG)[2])
    aes_multiplo= int(datosParaCifrar.split(TAG)[3])
    print "     Para entrar al sistema remoto ingrese su usuario y contraseña "
    entradaMaquina=False
    while not entradaMaquina:
      usuario = raw_input ("--Usuario: ")
      contrasenia = getpass("--Contraseña: ")
      datos = usuario +TAG +contrasenia
      datosCifrado = Cifrador().cifrar(datos, clavePublica, semilla_tamano, num_iteraciones,aes_multiplo) #Cifra los datos de usuario y contrasena
      clienteSocket.send(datosCifrado) 
      autenticacion = clienteSocket.recv(buff_size) #Recibe el codigo de autenticacion. 1 Permite el acceso a la maquina remota.  0 Acceso denegado
      if int(autenticacion) ==1:
         print "\nAcceso permitido a la maquina remota!! Presione Ctl + C para salir. "
         entradaMaquina=True
         iniciarMaquinaRemota(usuario,clienteSocket) #Inicia la maquina remota
      else:
         print "Acceso denegado!. Usuario inexistente o contraseña invalida."     
 except KeyboardInterrupt:
      print "\nPrograma Terminado!"
 except:
      print "\nNo se ha podido conectar al servidor " + host_servidor + " puerto " +puerto_servidor
    
 clienteSocket.close()
  
if __name__ == "__main__":
   sys.exit(main(sys.argv))
