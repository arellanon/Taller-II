#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse, ConfigParser, sys
from lib.NodoSlave import NodoSlave
#from lib.ConfigHash import ConfigHash
#from lib.Hash import Hash
from os.path import exists
from lib.Msg import Msg


SEPARADOR = ':'
#Método cifrar. Abre el archivo de usuarios y lo cifra. 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    parser.add_argument('--log',  default='log.txt', help='Archivo donde se almacenara el log. Por defecto log.txt')
    args = parser.parse_args()

    socketMaster= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_master = raw_input("Ingrese la IP del Master: ")
    port_master = raw_input("Ingrese el puerto del Master: ")
    
    datos=str(args.host)+SEPARADOR+str(args.port)

    try:
        socketMaster.connect((host_master,int(port_master)))
        Msg(socketMaster).send(0,datos)
        accion, data = Msg(socketMaster).recv()
        nro_nodo = int(data)
    except:
        print  "No se pudo conectar con el Nodo Master"
        socketMaster.close()

    print "conectado"
    s = NodoSlave(args.host, args.port, host_master, int(port_master), nro_nodo)
    s.iniciar_server()
