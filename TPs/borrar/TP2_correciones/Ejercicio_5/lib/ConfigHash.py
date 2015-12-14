#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import SafeConfigParser

class ConfigHash:
    def __init__(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.SEP1 = parser.get('CONFIG', 'SEP1')
        self.CLAVE_PUBLICA = parser.get('CONFIG', 'CLAVE_PUBLICA')
        self.SEMILLA = int( parser.get('CONFIG', 'SEMILLA') )
        self.ITERACIONES = int( parser.get('CONFIG', 'ITERACIONES') )
        self.AES = int( parser.get('CONFIG', 'AES') )
        self.ARCHIVO_USUARIOS_CIFRADO = parser.get('CONFIG', 'ARCHIVO_USUARIOS_CIFRADO')
        self.ARCHIVO_USUARIOS =  parser.get('CONFIG', 'ARCHIVO_USUARIOS')
