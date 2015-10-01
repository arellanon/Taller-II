#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#from lib.MyHandler import MyHandler
import os
import threading, datetime
import time
import urllib
#from urllib import urlopen, urlencode

def sensar():
    # cargamos los diccionarios con los archivos del directorio y su ultima modificacion
    print datetime.datetime.now()
    master={}
    for archivo in os.listdir("www/"):
        master[archivo] = os.path.getmtime("www/" + archivo)
    slave={}
    for archivo in os.listdir("www - copia/"):
        slave[archivo] = os.path.getmtime("www - copia/" + archivo)

#Verificamos diferencias para agregar y modificar
    print master
    print slave
    for filemaster, lastmod in master.items():
        if slave.has_key(filemaster) :
            if lastmod <> slave.get(filemaster) :
                print filemaster, " - modificar"
                os.remove("www - copia/" +filemaster)
                urllib.FancyURLopener.version = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
                file = open("www - copia/"+filemaster,"w")
                filehandle = urllib.urlopen("http://127.0.0.1:8000/"+filemaster)
                file.write(filehandle.read())
                file.close()
        else :
            print filemaster, " - agregar"
            urllib.FancyURLopener.version = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
            file = open("www - copia/"+filemaster,"w")
            filehandle = urllib.urlopen("http://127.0.0.1:8000/"+filemaster)
            file.write(filehandle.read())
            file.close()
            
#Verificamos diferencias para eliminar
    for fileslave, lastmod in slave.items():
        if not( master.has_key(fileslave) ) :
            print fileslave, " - eliminar"
            os.remove("www - copia/" +fileslave)

    threading.Timer(10, sensar).start()

if __name__ == '__main__':
    sensar()
