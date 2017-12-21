#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, ConfigParser, sys
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join
from lib.Nodo import Nodo

def main():
#    print getPaths(args.folder)
    s = Nodo(args.host, args.port, args.folder)
    s.iniciar_server()

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    parser.add_argument('--folder',  default='Folder', help='Directorio raiz de documentos')
    args = parser.parse_args()
    main()
