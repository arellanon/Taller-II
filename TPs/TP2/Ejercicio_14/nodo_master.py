#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse, ConfigParser, sys
from lib.NodoMaster import NodoMaster

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecucion de nodo master - Es necesario que se encuentren activo los nodos mappers y nodo reducer - archivo de configuracion: config.ini')
    parser.add_argument('in_file', help='archivo de entrada a procesar.')
    parser.add_argument('out_file', help='archivo donde devolver el resultado del proceso.')
    args = parser.parse_args(sys.argv[1:])

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read('config.ini')
    
    #recuperamos configuraciones
    #nodo master
    host = config_parser.get('master', 'host')
    port = config_parser.getint('master', 'port')
    
    #nodo reducer
    reducer = [config_parser.get('reducer', 'host'),  config_parser.getint('reducer', 'port')]
    
    #nodos mappers
    mappers = config_parser.get('mappers', 'mappers').split(',')
    mappers = map(lambda m: m.strip().split(':'), mappers)
    mappers = map(lambda m: (m[0], int(m[1])), mappers)
    
    master = NodoMaster( host, port, mappers, reducer, args.out_file)
    master.iniciar(args.in_file)
