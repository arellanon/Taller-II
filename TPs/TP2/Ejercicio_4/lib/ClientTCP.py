#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, struct, time

class ClientTCP():
    def __init__(self, host = '0.0.0.0', port = 80, recv_buffer = 512):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def rtt(self, segundos) :
        enviado = 0
        recibido = 0
        perdido = 0
        tiempo_total = 0
        tiempo_finalizacion = time.time() + int(segundos)
        while time.time() < tiempo_finalizacion :
            enviado += 1
            llego, tiempo = self.ping()
            tiempo_total += tiempo
            if llego :
                recibido += 1
            else :
                perdido += 1  
        if recibido > 0 : 
            promedio = tiempo_total / recibido  
        else :
            promedio = 0
        #mostramos resultados
        print '**********************************************'
        print 'Estadisticas IP: ', self.host
        print 'Paquetes: enviados=%d, Recibido=%d, Perdido=%d' % ( enviado, recibido, perdido)        
        print 'Promedio=%.f ms' % promedio
        print '**********************************************'

    def ping(self):
        socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_client.settimeout(10)
        start_time = time.time()
        recibido = False
        tiempo = 0
        try:
            socket_client.connect((self.host, self.port))
            end_time = time.time()
            tiempo = (end_time - start_time) * 1000
            recibido = True
            socket_client.close()
            print 'from %s: time=%.f ms' % ( self.host, tiempo)
        except:
            print 'unable to connect, lost package!'
        return recibido, tiempo
