#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import datetime
from sys import argv

xml = argv[1]
#xml ="http://www.telam.com.ar/rss2/politica.xml"
rss = BeautifulSoup(urlopen(xml))

count = 0
markup = '''
 <html>
  <head>
   <meta content="text/html; charset=utf-8" http-equiv="Content-type" />
  </head> 
  <body> '''

for item in rss.findAll('item'):
    count= count + 1
    print "Procesando noticia: " + str(count)
    f_title = item.find('title').getText()
    f_fecha = item.find('pubdate').string.strip()
    f_description = item.find('description').getText()
    f_link = item.find('link')

    f_enclosure_url = ""
    try:
        f_enclosure_url = item.find('enclosure')['url'].encode("UTF-8")
        file_enclosure = open(str(count)+".jpg","w")    
        file_enclosure.write( urlopen( f_enclosure_url ).read() )
        file_enclosure.close()
    except TypeError:
        pass
        
    markup = markup + '<h1>'+ f_title + ' +</h1>'
    markup = markup + '<h4>'+ f_fecha + ' +</h4>'
    markup = markup + '<p>' + f_description + '</p>'
    if f_enclosure_url :
        markup = markup + '<img src="'+ f_enclosure_url +'" width=350 height=320>'

markup = markup + '''
  </body>
 </html>
'''

resultado = open("resultado.html","w")
html = BeautifulSoup(markup)
resultado.write(html.prettify())
resultado.close()
