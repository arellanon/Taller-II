#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ServerProxyHttp import ServerProxyHttp

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Server Proxy HTTP .')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()
    
    s = ServerProxyHttp(args.host, args.port)
    s.iniciar_server()
