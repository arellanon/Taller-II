#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import socket
from sys import argv

 
buff_size = 4096
host,port = "10.0.0.1", 8080
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

request_http = """GET http://www.unlu.edu.ar/ HTTP/1.0\r\nHost: www.unlu.edu.ar\r\n\r\n"""

s.send(request_http)



datos = s.recv(buff_size)
http = ''
while datos:
	http += datos
	datos = s.recv(buff_size)
	
print http
s.close()


def main():
	
	return 0

if __name__ == '__main__':
	main()

