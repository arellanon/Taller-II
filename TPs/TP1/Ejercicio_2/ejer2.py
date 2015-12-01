#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, cgi
import urllib
from sys import argv
				
def descargar(sugerencia):
    index = 'https://es.wikipedia.org/w/index.php?'    
    parameter = {'search':sugerencia}
    url = index+urllib.urlencode(parameter)
    print "Descargando: ...", sugerencia
    file_descarga = open("Resultado/"+sugerencia+".html","w")
    page = urllib.urlopen(url)
    file_descarga.write(page.read())
    file_descarga.close()
    
if __name__ == '__main__':
    query = argv[1]
    index = 'https://es.wikipedia.org/w/index.php?'    
    parameter = {'search':query}
    url = index+urllib.urlencode(parameter)
    page = urllib.urlopen(url)
#   Descargarmos la pagina con los resultados
    file_descarga = open("Resultado/resultado.html","w")
    file_descarga.write(page.read())
    file_descarga.close()

#   Buscamos las sugerencias para descargar
    page = urllib.urlopen(url)
    for line in page.readlines() :
        encontrado = re.findall('<li>misspelling of ',str(line))
        if encontrado:
            resultado = re.search('/wiki/(.+)" title', str(line))
            if resultado:
                print "enviando a descargar: ",urllib.unquote(resultado.group(1))
                descargar(urllib.unquote(resultado.group(1))) 
                resultado = ''
        else:
            resultado = re.search('href="/wiki/(.+)"(.+)title="', str(line), )
            if resultado:
                print str(line)
#                print resultado.group(3)
                link_recuperado = str(resultado.group(1))
                error_link = re.search(':',link_recuperado)
                if not error_link:
                    print "enviando a descargar: ", urllib.unquote(resultado.group(1))
                    descargar(urllib.unquote(resultado.group(1)))
