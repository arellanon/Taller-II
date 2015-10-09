#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socket import AF_INET, SOCK_DGRAM
from datetime import datetime
import sys
import socket
import struct, time
def consultar():
    # Seteo de variables del servidor NTP
    host = "pool.ntp.org"
    port = 123
    buf = 1024
    address = (host,port)
    msg = '\x1b' + 47 * '\0'
    #
    #  Expresamos 1970-01-01 00:00:00 en segundo
    #
    #       1900-01-01
    #   -   1970-01-01
    #       ----------
    #            25567 (dias)
    #     
    #       25567 dias x 24 hs x 60 min x 60 seg = 2208988800 seg

    TIME1970 = 2208988800L # 1970-01-01 00:00:00
    # Conectar al servidor
    client = socket.socket(AF_INET,SOCK_DGRAM)
    client.sendto(msg, address)
    data, address = client.recvfrom(buf)

    # Recuperamos los segundos
    t = struct.unpack("!12I", data)[10]
    # Restamos los segundos 1970
    t -= TIME1970

    date = time.ctime(t)
    return date
