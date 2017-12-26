#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, ConfigParser, sys
from lib.NodoMaster import NodoMaster
#from lib.ConfigHash import ConfigHash
#from lib.Hash import Hash
from os.path import exists

#Método cifrar. Abre el archivo de usuarios y lo cifra. 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    parser.add_argument('--log',  default='log.txt', help='Archivo donde se almacenara el log. Por defecto log.txt')
    args = parser.parse_args()

    s = NodoMaster(args.host, args.port)
    s.iniciar_server()
