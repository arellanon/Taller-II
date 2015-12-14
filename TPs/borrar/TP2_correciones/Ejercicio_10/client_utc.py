#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ClientUTC import ClientUTC

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente UTC.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde conecta el cliente UTC.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde conecta el cliente UTC.')
    args = parser.parse_args()

    s = ClientUTC(args.host, args.port)
    s.iniciar()
