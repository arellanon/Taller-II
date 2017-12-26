#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Connection import Connection

protocoloId = 0x99887766
timeout = 10.0
x = Connection(protocoloId, timeout)
x.Start(8000)
x.Listen()
