#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
from urlparse import urlparse

class UrlDownload:
### Descargar url

    def __init__(self, url, proxy = '', port = 80, recv_buffer = 4096):
    ### Constructor
        self.url = url
        self.port = port
        self.recv_buffer = recv_buffer
        
        # seteamos el archivo a descargar
        u = urlparse(url)
        if u.path != "/" :
            self.path, self.filename = os.path.split(u.path)
        else :
            self.filename = "index.html"
            
        # seteamos el host donde nos conectaremos
        if proxy != '' :
            self.host = proxy
        else :
            self.host = u.netloc

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
          #  self.client_socket.settimeout(2)
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar()
            import sys
            sys.exit(1)
                    
        ### Generamos Header HTTP para solicitar recurso
        http_head =  'GET ' + self.url + ' HTTP/1.1\r\n'
        http_head += 'Host: ' + self.host +'\r\n'
        http_head += 'Accept: */*\r\n'
        http_head += 'User-Agent: Mozilla/5.0 (X11;Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.245485 Safari/537.36\r\n\r\n'
        self.client_socket.send(http_head)

        print "Descargando: ", self.filename
        ### Recuperamos el primer paquete http
        datos=self.client_socket.recv(self.recv_buffer)

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
        file = open(self.filename,"wb")
        #Datos sin Header HTTP
        datos_reales = datos[pos_header_end+len('\r\n\r\n'):]

        count = 1
        file.write(datos_reales)
        tot_len = float(len(datos_reales))
        print "N° ", count, ": ", len(datos_reales),"bytes - ",  tot_len / cl * 100, "%"

        while datos:
            count += 1
            datos = self.client_socket.recv(self.recv_buffer)
            tot_len += len(datos)
            print "N° ", count, ": ", len(datos),"bytes - ", tot_len / cl * 100, "%"
            file.write(datos)
            
        file.close()
        print "Tamaño total: ", tot_len, " bytes"
        self.client_socket.close()
