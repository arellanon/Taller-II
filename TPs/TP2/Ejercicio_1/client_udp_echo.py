#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys

if __name__ == '__main__':    
    if(len(sys.argv) < 3) :
        print 'Usar: python client_udp_echo.py <ip> <puerto> <formato_fecha>'
        sys.exit()
    socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    addr=sys.argv[1]
    port=int(sys.argv[2])
    data=sys.argv[3]
    print "enviado: ", data    
    socket_cliente.sendto(data,(addr,port))
    data,addr=socket_cliente.recvfrom(1024)
    print "recibido: ", data
