#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse
import ConfigParser
import logging
import sys

from lib.NodoReducer import NodoReducer

if __name__ == "__main__":
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    LOG_CONSOLE_FORMAT = '%(levelname)-8s %(message)s'

    # parseo de argumentos con ArgumentParser
    parser = argparse.ArgumentParser(
        description='Permite ejecutar un nodo reducer.')
    parser.add_argument(
        '--log', help='nombre del archivo en el que volcar los logs')
    parser.add_argument(
        '--verbose', '-v',
        help='flag que activa la salida de los logs por pantalla',
        action='store_true')
    parser.add_argument('config_file', help='archivo de configuración')
    args = parser.parse_args(sys.argv[1:])

    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(args.config_file)

    # configuro el logging
    if config_parser.get('logging', 'log_enabled'):
        logging.basicConfig(
            format=LOG_FORMAT, level=logging.DEBUG,
            filename=config_parser.get('logging', 'log_file'),
            datefmt='%d-%m %H:%M', filemode='w')
        # si verbose está activo, mostrar la información por pantalla
        if args.verbose:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter(LOG_CONSOLE_FORMAT)
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
    else:
        if args.verbose:
            level = logging.DEBUG
        else:
            level = logging.WARNING
        logging.basicConfig(
            format=LOG_FORMAT, datefmt='%d-%m %H:%M', level=level)

    # correr nodo
    reducer = NodoReducer(
        config_parser.get('connection', 'host'),
        config_parser.getint('connection', 'port'),
        (config_parser.get('master', 'host'),
         config_parser.getint('master', 'port')))
    reducer.start()
    reducer.stop()
