#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Socket import Socket
from enum import Enum

class Connection:
    mode = Enum('mode', 'None Client Server')
    state = Enum('state', 'Disconnected Listening Connecting ConnectFail Connected')

    def __init__(self, protocoloId, timeout):
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
        
x = Socket(8000)
print x.Open()
x.Send("hola mundo", '127.0.0.1', 8000)
x.Receive()
x.Close()
