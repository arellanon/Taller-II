#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse, ConfigParser, sys
from lib.NodoCircular import NodoCircular

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecucion nodo circular.')
    parser.add_argument('--id', type=int, help='ID del nodo.')
    parser.add_argument('--id_dst', type=int, help='ID del nodo destino.')
    args = parser.parse_args()
   
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read('config.ini')

#   Recuperamos la información del archivo de configuracion config.ini
    lista_nodos = {}
    for nodo in config_parser.sections():
        id_nodo = int(nodo.replace('nodo',''))
        #armamos un diccionario con key id_nodo y valor tupla host,port
        lista_nodos[id_nodo] = ( config_parser.get(nodo, 'host'), config_parser.getint(nodo, 'port') )
    
    if( lista_nodos.has_key(args.id) and lista_nodos.has_key(args.id_dst) ) :
        cfg_nodo = lista_nodos[args.id]
        cfg_nodo_dst = lista_nodos[args.id_dst]
        nodoCircular = NodoCircular(args.id, cfg_nodo[0], cfg_nodo[1], cfg_nodo_dst[0], cfg_nodo_dst[1])
        try:
            nodoCircular.conectarNodos()
            nodoCircular.ejecutarAnillo()
        except KeyboardInterrupt:
            print "\nNodo Finalizado."
    else :
        print 'El NODO ID '+ str(args.id) +' o el NODO ID_DST '+str(args.id_dst)+' no existe en el archivo de configuracion config.ini'
