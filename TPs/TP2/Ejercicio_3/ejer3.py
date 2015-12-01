#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
from urlparse import urlparse
from lib.ClientHTTP import ClientHTTP

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga url.')
    parser.add_argument('--url', help='Url del recurso a descargar.', required=True)
    parser.add_argument('--proxy', default='', help='Setear proxy para realizar la conexion.')
    parser.add_argument('--port', type=int, default='80', help='Puerto donde se conecta el cliente.')
    args = parser.parse_args()

    # seteamos el archivo a descargar
    u = urlparse(args.url)
    if u.path != "/" :
        path, filename = os.path.split(u.path)
    else :
        filename = "index.html"
    host = u.netloc

    s = ClientHTTP(host, args.port, args.proxy)
    result = s.get(args.url)
    
    file = open(filename, "wb")
    file.write(result)
    file.close()
