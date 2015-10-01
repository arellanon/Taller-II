#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from sys import argv

buff_size = 4096
host, port = "192.168.110.107", 8000
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#http_head =  'GET http://www.unlu.edu.ar HTTP/1.1\r\n'
#http_head += 'Host: www.unlu.edu.ar\r\n'
#http_head += 'Accept: text/html\r\n'
#http_head += 'User-Agent: Mozilla/5.0 (X11;Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.245485 Safari/537.36\r\n\r\n'

http_head = "hola mundo"
s.send(http_head)
        
datos=s.recv(buff_size)
print datos
"""
http = ""
while datos:
    http += datos
    datos = s.recv(buff_size)
print http
"""
s.close()
