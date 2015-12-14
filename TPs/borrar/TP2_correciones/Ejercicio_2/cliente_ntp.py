#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse
import sys
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cliente NTP.')
    parser.add_argument('--format', default="%c", help='Formato de fecha solicitado.')
    parser.add_argument('--host', default='127.0.0.1', help='IP del host donde conecta el cliente ntp.')
    parser.add_argument('--port', type=int, default='8000', help='Puerto donde conecta el cliente ntp.')
    args = parser.parse_args()

#    if(len(sys.argv) < 3) :
#        print 'Usar: python cliente_ntp.py <ip> <puerto> <formato_fecha>'
#        sys.exit()

    socket_cliente=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#    addr=sys.argv[1]
#    port=int(sys.argv[2])
#    try:
#        data=sys.argv[3]
#    except:
#        data = "%c"
#    print data
    data = args.format
    print data    
    socket_cliente.sendto(data,(args.host, args.port))
    data,addr=socket_cliente.recvfrom(1024)
    print data
