#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from sys import argv

buff_size = 4096
host, port = "127.0.0.1", 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = setsockopt(socket.SOL_SOCKET, socket.SO_ROUSEADDR, 1)
s.bind()
s.liste(backlog)

while True:
    client_sock, clien_addr = s.accept()
    print "Desde ",client_sock.getpeername()
    data = client_sock.recv(buff_size)
    while len(data):
        data = client_sock.recv(buff_size)
        print "Conexion cerrado por: ", client_sock.getpeername()
    client_sock.close()
s.close()
