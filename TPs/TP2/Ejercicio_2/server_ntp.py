#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib import server_ntp
import socket
import datetime

if __name__ == '__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(('',8000))
    while True:
        data,addr=s.recvfrom(1024)
        print('Address:',addr,'Data:',data)
        fecha = str( server_ntp.consultar() )
        today = datetime.datetime.now().strftime(data)
#        print today
        s.sendto(str(today) ,addr)
