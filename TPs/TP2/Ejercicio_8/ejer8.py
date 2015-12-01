#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.LoadBalancer import LoadBalancer
from ConfigParser import SafeConfigParser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load Balancer. Archivo de configuracion config.ini')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()

    parser = SafeConfigParser()
    parser.read('config.ini')

    s = LoadBalancer(args.host, args.port)
    s.setNodo1( parser.get('nodo1', 'host'), int( parser.get('nodo1', 'port') ))
    s.setNodo2( parser.get('nodo2', 'host'), int( parser.get('nodo2', 'port') ))
    s.iniciar_server()
