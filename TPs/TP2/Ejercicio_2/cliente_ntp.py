#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import sys
if __name__ == '__main__':    
    if(len(sys.argv) < 3) :
        print 'Usar: python cliente_ntp.py <ip> <puerto> <formato_fecha>'
        sys.exit()
    socket_cliente=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    addr=sys.argv[1]
    port=int(sys.argv[2])
    try:
        data=sys.argv[3]
    except:
        data = "%c"
    print data
    socket_cliente.sendto(data,(addr,port))
    data,addr=socket_cliente.recvfrom(1024)
    print data
