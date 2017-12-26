#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, random
from os import system,remove, walk, mkdir
from os.path import exists, isdir, join, dirname, getmtime
import time
       
if __name__ == "__main__":
        raiz = "SLAVE2"
        paths={}
        if not exists(raiz):
           mkdir(raiz)
           print "no existe raiz"
        for ruta, subdirectorio, ficheros in walk(raiz):
            print ruta, subdirectorio, ficheros
            subdirectorio.sort()
            if len(ficheros) > 0:
                for nombreFichero in ficheros:
                   rutaCompleta = join(ruta, nombreFichero)
                   timeModification = time.ctime(getmtime(rutaCompleta))
    #              elemento = (rutaCompleta, timeModification)
    #              paths.append(elemento)
                   paths[rutaCompleta] = timeModification
            else :
                paths[ruta] = None
        print paths
        print subdirectorio
        #print walk(raiz)
        
        antes = {1:"manzana", 2:"banana", 3:"naranja", 4:"pera" }
        despues = {1:"brazo", 4:"pera", 5:"pierna", 6:"ojo"}        
        modificar = {k:v for (k,v) in antes.items() if k in despues and v != despues.get(k, None) } #interseccion
        agregar = {k:v for (k,v) in despues.items() if k not in antes} #interseccion
        eliminar = {k:v for (k,v) in antes.items() if k not in despues} #interseccion
        
        print antes
        print despues
        print "modificacion: ", modificar
        print "agregar: ", agregar
        print "eliminar: ", eliminar        
