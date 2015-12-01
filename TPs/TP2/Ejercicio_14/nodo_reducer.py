#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import ConfigParser
import logging
import sys

from lib.NodoReducer import NodoReducer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecucion de nodo reducer. No necesita parametros se toman del archivo config.ini')
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read('config.ini')

    #recuperamos configuraciones
    #nodo reducer
    host = config_parser.get('reducer', 'host')
    port = config_parser.getint('reducer', 'port')
    
    #nodo master
    master = [config_parser.get('master', 'host'),  config_parser.getint('master', 'port')]
    
    reducer = NodoReducer(host, port, master)
    reducer.iniciar_server()
