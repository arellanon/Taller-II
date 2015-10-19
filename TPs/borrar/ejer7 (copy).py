#!/usr/bin/python
# -*- coding: utf-8 -*-
#import socket, thread, select
#from lib.ConnectionHandler import ConnectionHandler
from lib.ServerProxy import ServerProxy

def start_server(host='localhost', port=8080, timeout=60, handler=ConnectionHandler):

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    print "Serving on %s:%d."%(host, port)#debug
    soc.listen(0)
    while 1:
#        thread.start_new_thread(handler, soc.accept()+(timeout,))
        thread.start_new_thread(handler, soc.accept()+(timeout,))

s = ServerProxy()
s.iniciar_server()

if __name__ == '__main__':
    start_server()
