#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Socket import Socket
from enum import Enum
mode = Enum('mode', 'None Client Server')
state = Enum('state', 'Disconnected Listening Connecting ConnectFail Connected')

class Connection:
    def __init__(self, protocoloId = 0, timeout = 60):
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
    
    def Connect(self, address):
        self.ClearData()
        self.mode = mode.Client
        self.state = state.Connecting
        self.address = address
            
    def Mostrar(self):
        print self.protocoloId
        print self.timeout
        print self.mode
        print self.running

X = Connection()
X.Start(8000)
X.Mostrar()
