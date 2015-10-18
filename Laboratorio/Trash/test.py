#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from sys import argv

buff_size = 4096

#query = argv[1]
#proxy = argv[2]
#port = argv[3]

#host, port = "proxyw.unlu.edu.ar", 8080
#port = int(port)
#print proxy
#print port


host = 'www.labredes.unlu.edu.ar'
port = 80
#host, port = proxy, port
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

#http_head =  'GET http://www.unlu.edu.ar HTTP/1.1\r\n'
http_head =  'GET http://www.labredes.unlu.edu.ar/sites/www.labredes.unlu.edu.ar/files/site/data/bdm/clase_3_db_multidimensionales.pdf HTTP/1.1\r\n'
http_head += 'Host: www.unlu.edu.ar\r\n'
#http_head =  'GET ' + query + ' HTTP/1.1\r\n'
#http_head += 'Host: www.unlu.edu.ar\r\n'
http_head += 'Accept: text/html\r\n'
http_head += 'User-Agent: Mozilla/5.0 (X11;Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.245485 Safari/537.36\r\n\r\n'

s.send(http_head)
datos=s.recv(buff_size)
poscl = datos.lower().find('\r\ncontent-length: ')
poseoh = datos.find('\r\n\r\n')
if poscl < poseoh and poscl >= 0 and poseoh >= 0:
    # found CL header
    poseocl = datos.find('\r\n',poscl+17)
    cl = int(datos[poscl+17:poseocl])
    realdata = datos[poseoh+4:]
print "poseocl: ", poseocl
print "cl: ", cl
print "poscl: ", poscl
print "poseoh: ", poseoh

#file = open("log.txt","w")
#file.write(http_head)
#file.close()

#file = open("resultado.html","w")
http = ""
i = 1
while datos:
    datos = s.recv(buff_size)
    print i, ": ", len(datos)
    i= i +1
#    print datos
#    file.write(datos)
#file.close()

s.close()
