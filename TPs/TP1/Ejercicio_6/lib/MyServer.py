#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler
import os
import urllib
import SimpleHTTPServer

FLAG = True
NUM = 0

#Creamos la clase MyBaseHTTPRequestHandler, heredamos de BaseHTTPRequestHandler
class MyHandler(BaseHTTPRequestHandler):
                             
    #GET
    def do_GET(self):
        rootdir = 'www/' #Directorio raiz del servidor
        #Si el path de consulta esta vacio, devolvemos la pagina index.html
        if self.path == "/":
            self.path = "/index.html"
            
        try:                
            #if self.path.endswith('.html'):
        
            f = open(rootdir + self.path)

            #se envia el codigo 200
            self.send_response(200)

            #armamos cabecera
            self.send_header('Content-type','text-html')
            self.end_headers()

            #se envia el archivo al cliente
            self.wfile.write(f.read())
            f.close()
            return
        except IOError:
            self.send_error(404, 'archivo no encontrado')
