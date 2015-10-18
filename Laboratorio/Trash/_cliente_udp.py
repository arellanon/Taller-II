#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from sys import argv

buff_size = 4096
host, port = "127.0.0.1", 65430
s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto('hola mundo', (host, port ) )
s.close()
