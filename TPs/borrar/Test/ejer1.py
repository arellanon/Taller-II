#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen, urlencode
from sys import argv

if __name__ == '__main__':
    file = open("resultado.html","w")
    query = argv[1]
    index = 'https://es.wikipedia.org/w/index.php?'
    param = {'search':query}
    url = index+urlencode(param)
    filehandle = urlopen(url)
    file.write(filehandle.read())
    file.close()
