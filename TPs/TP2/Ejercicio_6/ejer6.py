#!/usr/bin/python
# -*- coding: utf-8 -*-
from lib.Server import Server

#signal.signal(signal.SIGINT, graceful_shutdown)
s = Server(8000)  # construct server object
s.iniciar_server() # aquire the socket
