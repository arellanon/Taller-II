#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import argparse, ConfigParser, sys
from lib.NodoCircular import NodoCircular

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ejecucion de nodo mapper.')
    parser.add_argument('id', type=int, help='ID del nodo.')
    args = parser.parse_args()

    print 'Nodo elegido: ', 'nodo'+ str(args.id)
    
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read('config.ini')

#   Recuperamos la información del archivo de configuracion config.ini
    lista_nodos = {}
    for nodo in config_parser.sections():
        id_nodo = int(nodo.replace('nodo',''))
        #armamos un diccionario con key id_nodo y valor tupla host,port
        lista_nodos[id_nodo] = ( config_parser.get(nodo, 'host'), config_parser.getint(nodo, 'port') )
    
    if( lista_nodos.has_key(args.id) ) :
        cfg_nodo = lista_nodos[args.id]
        print cfg_nodo
        nodoCircular = NodoCircular( args.id, cfg_nodo[0], cfg_nodo[1] )
        nodoCircular.conectando_nodos(lista_nodos)
        nodoCircular.anilloLogico()
    else :
        print 'El nodo'+ str(args.id) +' no existe en el archivo de configuracion config.ini'
    #cfg_nodo = { 'host' : config_parser.get(name_nodo, 'host'), 'port' : config_parser.getint(name_nodo, 'port') }
    
    #print cfg_nodo['host'], ':', cfg_nodo['port']
    
    


   # mapper = NodoMapper(args.host, args.port, reducer)
   # mapper.iniciar_server()
