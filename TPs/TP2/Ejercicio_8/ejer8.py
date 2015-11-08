#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ServerHttp import ServerHttp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load Balancer.')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()
    
    s = ServerHttp(args.host, args.port)
    s.iniciar_server()
