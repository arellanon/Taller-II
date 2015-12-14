#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib.ClientChat import ClientChat

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente Chat.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde conecta el cliente chat.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde conecta el cliente chat.')
    args = parser.parse_args()

    s = ClientChat(args.host, args.port)
    s.iniciar()
