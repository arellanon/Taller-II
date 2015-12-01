#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.ServerNtp import ServerNtp
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor NTP.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()
    
    s = ServerNtp(args.host, args.port)
    s.iniciar_server()
