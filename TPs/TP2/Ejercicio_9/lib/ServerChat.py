#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select

class ServerChat:
### Class server Chat

    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 1024):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = 10
        # Lista de socket
        self.CONNECTION_LIST = []
        
    def iniciar_server(self):
    ### Iniciar conexion
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))

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
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

    def enviar_msg(self, client_socket, msg):      
        for socket in self.CONNECTION_LIST:
        #No envíar mensarje al server_socket y al sock que envia el mensaje
            if socket != self.server_socket and socket != client_socket :
                try :
                    socket.send(msg)
                except :
                    socket.close()
                    self.CONNECTION_LIST.remove(socket)

    def esperando_conexiones(self):
    
        self.server_socket.listen(self.listen)
        # Añadimos socket server a la lista
        self.CONNECTION_LIST.append(self.server_socket)
        while True:
        # Obtener la lista sockets que están listos para ser leídos a través de selección
            read_sockets,write_sockets,error_sockets = select.select(self.CONNECTION_LIST,[],[])

            for socket in read_sockets:
                # Nueva conexion
                if socket == self.server_socket:
                    # Hay una nueva conexión recibida
                    client_socket, addr = self.server_socket.accept()
                    self.CONNECTION_LIST.append(client_socket)
                    print "Cliente (%s, %s) conectado" % addr
                    self.enviar_msg(client_socket, "Ingreso: [%s:%s].\n" % addr)
                # Mensaje desde algun cliente chat
                else:
                    # Datos del cliente
                    try:
                        data = socket.recv(self.recv_buffer)
                        if data:
                            self.enviar_msg(socket, "\r" + '<' + str(socket.getpeername()) + '> ' + data)
                    except:
                        self.enviar_msg(socket, "Cliente (%s, %s) desconectado." % addr)
                        print "Cliente (%s, %s) desconectado." % addr
                        socket.close()
                        self.CONNECTION_LIST.remove(socket)
                        continue
        self.server_socket.close()
