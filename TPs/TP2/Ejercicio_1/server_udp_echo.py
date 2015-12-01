#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse

if __name__ == '__main__':
    buff_size = 4096

    parser = argparse.ArgumentParser(description='Servidor Echo UDP.')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()

    print "Corriendo servidor %s:%s " % (args.host, args.port)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((args.host, args.port))
    while True:
	    data,addr=s.recvfrom(buff_size)
  	    print "Desde:", addr
	    s.sendto(data,addr)
