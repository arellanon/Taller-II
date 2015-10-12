#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
from sys import argv

from urlparse import urlparse

buff_size = 4096

### url a descargar ###
url= argv[1]
u = urlparse(url)

print u.path
if u.path != "/" :
    path, filename = os.path.split(u.path)
else :
    filename = "index.html"    
print "Descargando: ", filename

### seteamos las variables de conexion dependiendo de la configuracion del proxy###
try:
    host = argv[2]
except:
#   host de la url
    host = u.netloc
try:
    port = int(argv[3])
except:
#   puerto por defecto servidor http
    port = 80

### Creamos conexion
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

### Generamos Header HTTP para solicitar recurso
http_head =  'GET ' + url + ' HTTP/1.1\r\n'
http_head += 'Host: ' + host +'\r\n'
http_head += 'Accept: */*\r\n'
http_head += 'User-Agent: Mozilla/5.0 (X11;Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.245485 Safari/537.36\r\n\r\n'
s.send(http_head)

### Recuperamos el primer paquete http
datos=s.recv(buff_size)

### Final de Header HTTP
pos_header_end = datos.find('\r\n\r\n')

### Recuperamos Content-Length
# cl = Content-Length  
cl = 1
pos_cl = datos.lower().find('\r\ncontent-length: ')
if pos_cl < pos_header_end and pos_cl >= 0 and pos_header_end >= 0:
    # Encontrar Content-Length 
    pos_cl_inicio = pos_cl + len('\r\ncontent-length: ')
    pos_cl_final = datos.find('\r\n', pos_cl_inicio)
    cl = int(datos[pos_cl_inicio:pos_cl_final])
print "Content-length: ", cl

### Guardamos Header HTTP recibido
file = open("log.txt","w")
file.write(datos[:pos_header_end])
file.close()

### Generamos archivo de descarga
file = open(filename,"wb")
#Datos sin Header HTTP
datos_reales = datos[pos_header_end+len('\r\n\r\n'):]

count = 1
file.write(datos_reales)
tot_len = float(len(datos_reales))
print "N° ", count, ": ", len(datos_reales),"bytes - ",  tot_len / cl * 100, "%"

while datos:
    count += 1
    datos = s.recv(buff_size)
    tot_len += len(datos)
    print "N° ", count, ": ", len(datos),"bytes - ", tot_len / cl * 100, "%"
    file.write(datos)
    
file.close()
print "Tamaño total: ", tot_len, " bytes"
s.close()
