#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser

class ConfigHash:
    def __init__(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.SEP1 = parser.get('CONFIG', 'SEP1')
        self.CLAVE_PUBLICA = parser.get('CONFIG', 'CLAVE_PUBLICA')
        self.SEMILLA_TAMANO = int( parser.get('CONFIG', 'SEMILLA_TAMANO') ) # Tamaño de numero aleatorio en bytes
        self.NUM_ITERACIONES = int( parser.get('CONFIG', 'NUM_ITERACIONES') )     # Numero de interaciones en la generacion de la clave
        self.AES_MULTIPLO = int( parser.get('CONFIG', 'AES_MULTIPLO') ) # Tamaño multiplo requerido por AES
        self.ARCHIVO_USUARIOS_CIFRADO = parser.get('CONFIG', 'ARCHIVO_USUARIOS_CIFRADO')
        self.ARCHIVO_USUARIOS =  parser.get('CONFIG', 'ARCHIVO_USUARIOS') 
