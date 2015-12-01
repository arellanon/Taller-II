#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ServerUTC import ServerUTC

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Servidor UTC.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()
    
    s = ServerUTC(args.host, args.port)
    s.iniciar_server()
