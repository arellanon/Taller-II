#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, time, sys

class ServerUTC:
### Class server HTTP

    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 1024, listen = 5):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = listen

    def iniciar_server(self):
    ### Iniciar conexion
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket_server.bind((self.host, self.port))

        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.cerrar_server()
            import sys
            sys.exit(1)

        print "Presionar Ctrl+C para salir."
        self.esperando_conexiones()

    def cerrar_server(self):
    ### Cerrar conexion
        try:
            self.socket_server.shutdown(socket.SHUT_RDWR)
            self.socket_server.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

    def esperando_conexiones(self):
        try: 
            while True:
                self.socket_server.listen(self.listen)
                conn, addr = self.socket_server.accept()
                data = conn.recv(self.recv_buffer)
                msg_time = time.time()
                if data == 'cristian':
                    print 'conexion cliente: ', conn.getpeername()
                    time.sleep(0.900)
                    time_to_send = time.time()
                    conn.send(str(time_to_send)+';'+str(msg_time))
                    conn.close()
        except KeyboardInterrupt:
           print "\nServidor Apagado"
           self.cerrar_server()
