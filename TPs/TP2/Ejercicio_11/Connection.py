#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Socket import Socket
from enum import Enum
mode = Enum('mode', 'None Client Server')
state = Enum('state', 'Disconnected Listening Connecting ConnectFail Connected')

class Connection:
<<<<<<< HEAD
    def __init__(self, protocoloId = 0, timeout = 60):
=======
    def __init__(self, protocoloId, timeout):	
>>>>>>> 6dc25e75885e69cee320918968c878618243660e
        self.protocoloId = protocoloId
        self.timeout = timeout
        self.mode = mode.None
        self.running = False
    
    def ClearData(self):
        self.state = state.Disconnected;
        self.timeoutAccumulator = 0.0;
    
    def Start(self, port):
        self.socket = Socket(port)
        self.running = True
    
    def Stop(self):
        self.ClearData()
        self.socket.Close()
        self.running = False

    def Listen(self):
        self.ClearData()
        self.mode = mode.Server
        self.state = state.Listening
<<<<<<< HEAD
    
=======
	print self.mode
        
>>>>>>> 6dc25e75885e69cee320918968c878618243660e
    def Connect(self, address):
        self.ClearData()
        self.mode = mode.Client
        self.state = state.Connecting
        self.address = address
<<<<<<< HEAD
            
    def Mostrar(self):
        print self.protocoloId
        print self.timeout
        print self.mode
        print self.running

X = Connection()
X.Start(8000)
X.Mostrar()
=======
        
"""
x = Socket(8000)
print x.Open()
x.Send("hola mundo", '127.0.0.1', 8000)
x.Receive()
x.Close()
"""

>>>>>>> 6dc25e75885e69cee320918968c878618243660e
