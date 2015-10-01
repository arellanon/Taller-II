#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from lib.MyServer import MyHandler, MyBalancer
import os
import time

""" Rutina balanceador """   
def run_balancer(HOST_NAME, PORT_NUMBER):

    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = HTTPServer(server_address, MyBalancer)
    print time.asctime(), "Corriendo balanceador - %s:%s\n" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Deteniendo balanceador - %s:%s" % (HOST_NAME, PORT_NUMBER)    
   
if __name__ == '__main__':
    try:
        run_balancer('127.0.0.1', 8000)
    except KeyboardInterrupt:
        print "Presion <Ctr-C>"
