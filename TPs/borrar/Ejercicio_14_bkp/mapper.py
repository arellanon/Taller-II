#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse, ConfigParser, sys
from lib.NodoMapper import NodoMapper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecucion de nodo mapper.')
    parser.add_argument('host', help='IP del host donde brinda servicio.')
    parser.add_argument('port', type=int, help='Puerto donde brinda servicio.')    
    args = parser.parse_args(sys.argv[1:])

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read('config.ini')
    
    #recuperamos configuraciones
    #nodo mapper
    host = args.host
    port = args.port
        
    #nodo reducer
    reducer = [config_parser.get('reducer', 'host'), config_parser.getint('reducer', 'port')]

    mapper = NodoMapper(host, port, reducer)
    mapper.iniciar_server()
