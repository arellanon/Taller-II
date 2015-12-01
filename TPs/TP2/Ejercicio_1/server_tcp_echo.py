#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse

if __name__ == '__main__':
    buff_size = 4096
    backlog = 5
    
    parser = argparse.ArgumentParser(description='Servidor Echo TCP.')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde brinda servicio el programa.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde brinda servicio el programa.')
    args = parser.parse_args()
    
    print "Corriend servidor %s:%s " % (args.host, args.port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((args.host, args.port))
    s.listen(backlog)
    while True:
	    client_sock, client_addr = s.accept()
	    print "Desde:",client_sock.getpeername()
	    data=client_sock.recv(buff_size)
	    client_sock.send(data)
    client_sock.close()
    s.close()
