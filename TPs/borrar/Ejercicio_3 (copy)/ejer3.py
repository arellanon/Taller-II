#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from lib.UrlDownload import UrlDownload

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga url.')
    parser.add_argument('--url', help='Url del recurso a descargar.', required=True)
    parser.add_argument('--proxy', default='', help='Setear proxy para realizar la conexion.')
    parser.add_argument('--port', type=int, default='80', help='Puerto donde se conecta el cliente.')
    args = parser.parse_args()

    s = UrlDownload(args.url, args.proxy, args.port)
    s.iniciar()
