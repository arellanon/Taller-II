#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from sys import argv
from lib import tools

if __name__ == '__main__':
    query = argv[1]

    def buscar(buscador, url, query):
        urllib.FancyURLopener.version = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
        web = urllib.urlopen(url + urllib.urlencode({'q':query}) )
        open( buscador + '.html', 'w').write(web.read())

    buscadores={"google" : "http://www.google.com.ar/search?", "yahoo" : "http://ar.search.yahoo.com/search?", "ask": "http://ar.ask.com/web?" }
    for buscador, url in buscadores.iteritems() :
        tiempo = tools.cronometro(buscar)(buscador, url, query)
        print "El tiempo del buscador %s es: %s" % (buscador, tiempo)
