#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse, ConfigParser, sys
from lib.ClienteUDP import ClienteUDP

def main():
# Start the job threads
    s = ClienteUDP(args.host, args.port )
    s.iniciar_cliente()
    
#Método cifrar. Abre el archivo de usuarios y lo cifra. 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    parser.add_argument('--log',  default='log.txt', help='Archivo donde se almacenara el log. Por defecto log.txt')
    args = parser.parse_args()
    main()


