#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, os
from sys import argv
from lib.ClientTCP import ClientTCP
from lib.ClientUDP import ClientUDP
import time, argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RTT.')
    parser.add_argument('--segundos', type=int, default='4', help='Setear segundos del RTT. (Por defecto 4).')
    args = parser.parse_args()

    print "UDP"
    f = open('IPsUDP.txt', 'r+')
    string = f.read().strip()
    ips = string.split(';')

    for ip in ips :
        print 'Procesando ip: ', ip
        c = ClientUDP(ip, 53)
        print ip, ":", c.rtt(args.segundos)

    print "TCP"
    f = open('IPsTCP.txt', 'r+')
    string = f.read().strip()
    ips = string.split(';')
    for ip in ips :
        print 'Procesando ip: ', ip
        c = ClientTCP(ip, 80)
        print ip, ":", c.rtt(args.segundos)
