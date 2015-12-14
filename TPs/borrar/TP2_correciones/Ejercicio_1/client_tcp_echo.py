#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Cliente Echo TCP.')
    parser.add_argument('--data', help='Mensaje a enviar.', required=True)
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde se conecta el cliente.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde se conecta el cliente.')
    args = parser.parse_args()
        
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    s.send(args.data)
    print "enviado: ", args.data
    args.data = s.recv(1024)
    print "recibido: ", args.data
    s.close()
