#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from lib.MyServer import MyHandler
import os
import threading
import time
from sys import argv
   
def run(HOST_NAME = '127.0.0.1', PORT_NUMBER = 8000):

    server_address = (HOST_NAME, PORT_NUMBER)
    httpd = HTTPServer(server_address, MyHandler)

    print time.asctime(), "Corriendo servidor - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Deteniendo servidor - %s:%s" % (HOST_NAME, PORT_NUMBER)    
    
  
if __name__ == '__main__':
    #Seteamos las configuraciones por defecto 127.0.0.1:8000
    HOST_NAME = '127.0.0.1'
    PORT_NUMBER = 8000
    #Si vienen 
    try:
        HOST_NAME = argv[1]
    except:
	    pass
    try:
        PORT_NUMBER = int(argv[2])
    except:
	    pass
    run(HOST_NAME, PORT_NUMBER)
