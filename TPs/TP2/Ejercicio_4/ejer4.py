#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, os
from sys import argv
from lib.ClientTCP import ClientTCP
from lib.ClientUDP import ClientUDP
import time, argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RTT.')
    parser.add_argument('--segundos', type=int, default='3', help='Setear segundos del RTT. (Por defecto 3).')
    parser.add_argument('--udp', help='Procesa la lista de IP IPsUDP.txt para el protocolo UDP.', action='store_true')
    parser.add_argument('--tcp', help='Procesa la lista de IP IPsTCP.txt para el protocolo TCP.', action='store_true')        
    args = parser.parse_args()
    
    if not args.udp and not args.tcp :
        print 'Debe seleccionar algun protocolo para ejecutar programa.'
    
    if args.udp :
        print "*** UDP ***"
        f = open('IPsUDP.txt', 'r+')
        string = f.read().strip()
        ips = string.split(';')
        for ip in ips :
            print 'Procesando ip: ', ip
            c = ClientUDP(ip, 53)
            c.rtt(args.segundos)

    if args.tcp :
        print "*** TCP ***"
        f = open('IPsTCP.txt', 'r+')
        string = f.read().strip()
        ips = string.split(';')
        for ip in ips :
            print 'Procesando ip: ', ip
            c = ClientTCP(ip, 80)
            print ip, ":", c.rtt(args.segundos)
