#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
from urlparse import urlparse

class ClientHTTP:
### Descargar url

    def __init__(self, host = '', port = 80, proxy = '', recv_buffer = 4096):
    ### Constructor
        if proxy != '' :
            self.host = proxy
        else :
            self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def getHost(self):
        return self.host
    
    def getPort(self):
        return str(self.port)
    
    def getSocket(self):
        return self.host+":"+str(self.port)

    def cerrar(self):
    ### Cerrar conexion
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

    def get(self, url):
        self.url = url
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
          #  self.client_socket.settimeout(2)
            print self.host,":", self.port
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

        print "Descargando..."
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
        file = open("log.txt","a")
        file.write(datos[:pos_header_end])
        file.close()

        ### Generamos archivo de descarga
        datos_reales = datos[pos_header_end+len('\r\n\r\n'):]

        count = 1
        resultado = datos_reales
        tot_len = float(len(datos_reales))
        if tot_len > cl : cl = tot_len
        print "N° ", count, ": ", len(datos_reales),"bytes - ",  tot_len / cl * 100, "%"

        while datos:
            count += 1
            datos = self.client_socket.recv(self.recv_buffer)
            tot_len += len(datos)
            print "N° ", count, ": ", len(datos),"bytes - ",  tot_len / cl * 100, "%"
            #file.write(datos)
            resultado += datos
            
        #file.close()
        print "Tamaño total: ", tot_len, " bytes"
        self.client_socket.close()

        return resultado
