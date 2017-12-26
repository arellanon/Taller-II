#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, ConfigParser, sys
from lib.ServidorUDP import ServidorUDP

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server - Realiability, Ordering and Congestion Avoidance over UDP.')
    parser.add_argument('--host', default='0.0.0.0', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()

    s = ServidorUDP(args.host, args.port)
    s.iniciar_server()
