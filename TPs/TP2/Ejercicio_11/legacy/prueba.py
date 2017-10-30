#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys
from lib.MiClase import MiClase
import argparse

if __name__ == '__main__':    
    print "hola mundo"
    x = MiClase()
    print x.f()
"""
    parser = argparse.ArgumentParser(description='Cliente Echo UDP.')
    parser.add_argument('--data', help='Mensaje a enviar.', required=True)
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde se conecta el cliente.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde se conecta el cliente.')
    args = parser.parse_args()
    
    socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print "enviado: ", args.data
    Msg(socket_cliente).send(1, args.data,(args.host, args.port) )
    Msg(socket_cliente).recv()
#    socket_cliente.sendto(args.data,(args.host, args.port))
#    data, addr = socket_cliente.recvfrom(1024)
#    print "recibido: ", data
"""
