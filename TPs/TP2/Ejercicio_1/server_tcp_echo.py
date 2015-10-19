#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

if __name__ == '__main__':
    buff_size = 4096
    host, port = "127.0.0.1", 8000
    backlog = 5
    
    print "Corriend servidor %s:%s " % (host, port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen(backlog)
    while True:
	    client_sock, client_addr = s.accept()
	    print "Desde:",client_sock.getpeername()
	    data=client_sock.recv(buff_size)
	    client_sock.send(data)
    client_sock.close()
    s.close()
