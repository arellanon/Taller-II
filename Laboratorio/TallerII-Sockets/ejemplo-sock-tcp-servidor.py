#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import socket
from sys import argv

buff_size = 4096
host, port = "192.168.110.107", 8000
backlog = 5

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(backlog)

while True:
	client_sock, client_addr = s.accept()
	print "Desde:",client_sock.getpeername()
	data=client_sock.recv(buff_size)
	client_sock.send(data)
	while len(data):
		#Siquisieraenviarunarespuesta
		#client_sock.sendall(’Algo’)
		print data
		data = client_sock.recv(buff_size)
		client_sock.send(data)
	print "Conexión cerrada por:",client_sock.getpeername()
	client_sock.close()

s.close()

def main():
	
	return 0

if __name__ == '__main__':
	main()

