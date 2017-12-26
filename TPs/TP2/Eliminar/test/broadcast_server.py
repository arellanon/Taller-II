#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_socket.bind(('',8000))

    print 'start service ...'

    while True :
        message , address = my_socket.recvfrom(8192)
        print 'message (%s) from : %s' % ( str(message), address[0])
#        print 'message from :'+ str(address[0]) , message)

if __name__ == "__main__" :
    main()
