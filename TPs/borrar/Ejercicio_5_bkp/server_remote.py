#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from lib.ServerRemote import ServerRemote
from lib.ConfigHash import ConfigHash
from lib.Hash import Hash
from os.path import exists

#Método cifrar. Abre el archivo de usuarios y lo cifra. 
def encriptar():
    config = ConfigHash()
    if exists (config.ARCHIVO_USUARIOS):
        archivo = open (config.ARCHIVO_USUARIOS,"r")
        archivoCifrado = open(config.ARCHIVO_USUARIOS_CIFRADO,"w")
        listaUsuarios = archivo.readlines()
        for user in listaUsuarios:
            usuarioCifrado = Hash().cifrar(user[:-1], config.CLAVE_PUBLICA, config.SEMILLA_TAMANO, config.NUM_ITERACIONES, config.AES_MULTIPLO) 
            archivoCifrado.write(usuarioCifrado +config.SEP1)
        archivo.close()
        archivoCifrado.close()
        print "Archivo cifrado"
    else:
        print "No existe el archivo "+config.ARCHIVO_USUARIOS
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    parser.add_argument('--log',  default='log.txt', help='Archivo donde se almacenara el log. Por defecto log.txt')
    parser.add_argument('--gen_user', help='Generar cifrado de usuarios del archivo user.txt ( usuario:clave )', action='store_true')
    args = parser.parse_args()
    
    if not args.gen_user :
        s = ServerRemote(args.host, args.port, args.log)
        s.iniciar_server()
    else :
#        print "Generar usuarios"
        encriptar()
