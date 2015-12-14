#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, time
import urllib
from ClientHTTP import ClientHTTP

FLAG = True

class LoadBalancer:
### Class server HTTP

    def __init__(self, host = '0.0.0.0', port = 8000, recv_buffer = 1024, listen = 5):
    ### Constructor
        self.host = host
        self.port = port
        self.recv_buffer = recv_buffer
        self.listen = listen

    def setNodo1(self, host = '0.0.0.0', port = 8001):
        self.nodo1_host = host
        self.nodo1_port = port
        
    def setNodo2(self, host = '0.0.0.0', port = 8002):
        self.nodo2_host = host
        self.nodo2_port = port
             
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
            s.socket.cerrar_server(socket.SHUT_RDWR)
        except Exception as e:
            print "ERROR: No se puede cerrar el socket.", e

    def header_http(self,  code):
    ### Determinar el code http
        header = ''
        if (code == 200):
            header = 'HTTP/1.1 200 OK\n'
        elif(code == 404):
            header = 'HTTP/1.1 404 Not Found\n'

        ### Escribimos header http
        current_date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: ' + current_date +'\n'
        header += 'Server: HTTP-Server-Nahuel\n'
        header += 'Connection: close\n\n'

        return header

    def esperando_conexiones(self):
        global FLAG
        while True:
            print "Esperando conexiones..."
            self.socket_server.listen(self.listen) # maxima cantidad de conexiones

            conn, addr = self.socket_server.accept()

            print "Conexion desde:", addr

            data = conn.recv(1024) #recibe datos desde el cliente
            string = bytes.decode(data) #decodificamos como string

            # Determinar peticion (HEAD y GET soportados)
            request_method = string.split(' ')[0]
            if (request_method == 'GET') | (request_method == 'HEAD'):
                nodo1 = ClientHTTP(self.nodo1_host, self.nodo1_port)
                nodo2 = ClientHTTP(self.nodo2_host, self.nodo2_port)
            # Recuperamos el archivo solicitado
                file_requested = string.split(' ')[1]
                if FLAG:
                    print "Nodo1: ", nodo1.getSocket(), file_requested
#                    print "file_requested:", file_requested
                    page = nodo1.get(file_requested)
                    response_content = page
                    FLAG = False
                else:
                    print "Nodo2: ", nodo2.getSocket(), file_requested
                    page = nodo2.get(file_requested)
                    response_content = page
                    FLAG = True
                response_headers = self.header_http( 200)

            # Cargamos contenido del archivo 
                server_response =  response_headers.encode() # Retornamos Header
                if (request_method == 'GET'):
                    server_response +=  response_content  # Solo para GET

                conn.send(server_response)
                print "Cerrar conexion con el cliente"
                conn.close()
            else:
                print "HTTP request method no soportado!!! (unicamente GET y HEAD)", request_method
