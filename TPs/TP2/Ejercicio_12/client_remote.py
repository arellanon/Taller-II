#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ClientRemote import ClientRemote

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente Remoto.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde conecta el cliente remoto.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde conecta el cliente remoto.')
    args = parser.parse_args()

    s = ClientRemote(args.host, args.port)
    s.iniciar()
