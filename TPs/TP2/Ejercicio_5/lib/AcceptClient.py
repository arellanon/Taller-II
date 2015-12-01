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
from Hash import Hash
from ConfigHash import ConfigHash

TAG2=':'

class AcceptClient(Thread):
   def __init__(self, conn_client, recv_buffer, log):
          self.conn_client = conn_client
          self.recv_buffer = recv_buffer
          self.log = log
          Thread.__init__(self)

   def run(self):
      self.configCifrador = ConfigHash()
      datosParaCifrar = self.configCifrador.CLAVE_PUBLICA+TAG2+str(self.configCifrador.SEMILLA)+TAG2+str(self.configCifrador.ITERACIONES)+TAG2+str(self.configCifrador.AES) 
      self.conn_client.sendall(datosParaCifrar)
      flag=False
      while not flag:
        datosCifrado = self.conn_client.recv(self.recv_buffer)
        if datosCifrado: 
           usuario, acceso = self.autenticarSesion(datosCifrado)
           self.conn_client.sendall(str(acceso))
           if acceso == 1:
              print "Acceso permitido: " + usuario
              self.iniciarSesion(usuario) # Permite el acceso al cliente. Inicia la maquina remota
              flag=True
           else:
              print "Acceso denegado"
        else:
          self.conn_client.close()
          flag=True

   def iniciarSesion(self, usuario):
       print "Inicio de sesion: "+usuario
       sesion = 'Usuario: ' +usuario +" "+ str(self.conn_client.getpeername())+' ingreso: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
       ejecutando = True   
       try:
         while ejecutando==True:
            comando = self.conn_client.recv(self.recv_buffer)
            if len(comando):
                #Ejecutar comando
                p = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True) 
                (salida, err) = p.communicate()
                if salida =="": 
                  error = "Comando Inexistente "
                  self.conn_client.sendall(error)
                else:
                  self.conn_client.sendall(str(salida))
                print "usuario: "+usuario+ " - comando: "+comando
                sesion += usuario +"@"+usuario+":~$ " + comando + "\n"+salida 
            else:
              ejecutando=False
              print "Fin de sesion: "+usuario
              sesion += "Usuario " +usuario +" "+ str(self.conn_client.getpeername())+' salio del sistema el: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
              self.escribirLog(sesion)
              self.conn_client.close()                  
       except:     
           sesion += "Usuario " +usuario +" "+ str(self.conn_client.getpeername())+' salio del sistema el: '+ datetime.now().strftime('%d %b %y %H:%M:%S').upper()+"\n" 
           self.escribirLog(sesion)  
           self.conn_client.close()
       
   def autenticarSesion(self, datosCifrado):
        datos = Hash().descifrar(datosCifrado, self.configCifrador.CLAVE_PUBLICA, self.configCifrador.SEMILLA, self.configCifrador.ITERACIONES)
        usuario = datos.split(TAG2)[0]
        clave = datos.split(TAG2)[1]
        if exists (self.configCifrador.ARCHIVO_USUARIOS_CIFRADO):
           archivoCifrado = open(self.configCifrador.ARCHIVO_USUARIOS_CIFRADO,"r")
        else:
           print "No existe archivo de cifrado."
           sys.exit(1)
        listaUsuarios = archivoCifrado.read().split(self.configCifrador.SEP1)
        acceso=0
        for user in listaUsuarios:
            if len(user):      
              datos = Hash().descifrar(user, self.configCifrador.CLAVE_PUBLICA, self.configCifrador.SEMILLA, self.configCifrador.ITERACIONES)
              usuarioArchivo = datos.split(TAG2)[0]
              claveArchivo = datos.split(TAG2)[1]
              if usuarioArchivo == usuario and claveArchivo == clave:
                   acceso=1
                   break
        archivoCifrado.close()
        return usuario, acceso
 
   def escribirLog(self, sesion):
        log = open(self.log, 'a')
        log.write(sesion +'\n')
        log.close()
