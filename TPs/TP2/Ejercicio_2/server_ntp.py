#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.ServerNtp import ServerNtp
import socket
import datetime

if __name__ == '__main__':
    s = ServerNtp()
    s.iniciar_server()
