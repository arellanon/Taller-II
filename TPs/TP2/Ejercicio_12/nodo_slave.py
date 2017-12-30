#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import socket
import argparse, ConfigParser, sys
from lib.NodoSlave import NodoSlave
#from os.path import exists
#from lib.Msg import Msg

#Método cifrar. Abre el archivo de usuarios y lo cifra. 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Nodo Slave.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()

    s = NodoSlave(args.host, args.port)
    s.iniciar_server()
