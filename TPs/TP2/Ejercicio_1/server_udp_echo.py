#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

if __name__ == '__main__':
    buff_size = 4096
    host, port = "127.0.0.1", 8000

    print "Corriendo servidor %s:%s " % (host, port)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    while True:
	    data,addr=s.recvfrom(buff_size)
  	    print "Desde:", addr
	    s.sendto(data,addr)
