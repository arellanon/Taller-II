#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, sys
 
if __name__ == '__main__':
    
    if(len(sys.argv) < 3) :
        print 'Usar: python client_tcp_echo.py <ip> <puerto> <formato_fecha>'
        sys.exit()
    buff_size = 4096
    host = sys.argv[1]
    port = int(sys.argv[2])
    datos_env = sys.argv[3]
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.send(datos_env)
    print "enviado: ", datos_env
    datos_recv = s.recv(buff_size)
    print "recibido: ", datos_recv
    s.close()
