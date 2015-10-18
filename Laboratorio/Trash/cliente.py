#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from sys import argv

buff_size = 4096

query = argv[1]
proxy = argv[2]
port = argv[3]

#host, port = "proxyw.unlu.edu.ar", 8080
port = int(port)
print proxy
print port
host, port = proxy, port
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#http_head =  'GET http://www.unlu.edu.ar HTTP/1.1\r\n'
#http_head += 'Host: www.unlu.edu.ar\r\n'
http_head =  'GET ' + query + ' HTTP/1.1\r\n'
http_head += 'Host: www.unlu.edu.ar\r\n'
http_head += 'Accept: text/html\r\n'
http_head += 'User-Agent: Mozilla/5.0 (X11;Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.245485 Safari/537.36\r\n\r\n'

s.send(http_head)
datos=s.recv(buff_size)
print datos
file = open("log.txt","w")
file.write(http_head)
file.close()

file = open("resultado.html","w")
http = ""
while datos:
    datos = s.recv(buff_size)
    file.write(datos)
file.close()

s.close()
