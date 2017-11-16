#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

class mysocket:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock
		print "hola mundo"

	def connect(host, port):
	    self.sock.connect((host, port))

	def mysend(msg):
	    totalsent = 0
	    while totalsent < MSGLEN:
			sent = self.sock.send(msg[totalsent:])
			if sent == 0:
				raise RuntimeError
			totalsent = totalsent + sent

	def myreceive():
	    msg = ''
	    while len(msg) < MSGLEN:
			chunk = self.sock.recv(MSGLEN-len(msg))
			if chunk == '':
				raise RuntimeError
			msg = msg + chunk
	    return msg

X = mysocket()
