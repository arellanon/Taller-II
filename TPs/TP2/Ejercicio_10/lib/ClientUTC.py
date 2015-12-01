#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, time, sys
import datetime

class ClientUTC:
### Cliente
    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 4096):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer

    def iniciar(self):
    ### Iniciar conexion
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            try:
                self.client_socket.connect((self.host, self.port))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket."
                self.cerrar()
                import sys
                sys.exit(1) 
            raw_input('Presione Enter para continuar...')
            start_time = time.time()
            request = 'cristian'
            self.client_socket.send(request)
            data = self.client_socket.recv(self.recv_buffer)
            end_time = time.time()
            #recuperamos los tiempos del servidor
            times = data.strip().split(';')
            delay_time = ((end_time - start_time) - (float(times[0]) - float(times[1])))/2
            time_to_server = float(times[0]) + delay_time
            time_request = datetime.datetime.utcfromtimestamp(time_to_server)
            print 'Delay: ', delay_time
            print 'Hora en UTC ' + (datetime.datetime.strftime(time_request,'%H:%M:%S'))
        except KeyboardInterrupt:
            print "\nChau!"
            self.cerrar()
            
    def cerrar(self):
    ### Cerrar conexion
        try:
            self.client_socket.shutdown(socket.SHUT_RDWR)
            self.client_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e
