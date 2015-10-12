#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import time

class Server:
### Class server HTTP

    def __init__(self, port = 8000):
    ### Constructor
        self.host = ''
        self.port = port
        self.www_dir = 'www' # Directorio raiz

    def iniciar_server(self):
    ### Iniciar conexion
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket.bind((self.host, self.port))

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
        while True:
            print "Esperando conexiones..."
            self.socket.listen(5) # maxima cantidad de conexiones

            conn, addr = self.socket.accept()

            print "Conexion desde:", addr

            data = conn.recv(1024) #recibe datos desde el cliente
            string = bytes.decode(data) #decodificamos como string

            # Determinar peticion (HEAD y GET soportados)
            request_method = string.split(' ')[0]
            print "Method: ", request_method
            print "Request body: ", string
            if (request_method == 'GET') | (request_method == 'HEAD'):

            # Recuperamos el archivo solicitado
                file_requested = string.split(' ')[1]
            # Descartamos lo que viene despues del ?
                file_requested = file_requested.split('?')[0]

                if (file_requested == '/'):
                    file_requested = '/index.html' # si es vacio por defecto devolvemos index.html
                    
                file_requested = self.www_dir + file_requested
                #print ("[",file_requested,"]")

            # Cargamos contenido del archivo
                try:
                    file_handler = open(file_requested,'rb')
                    if (request_method == 'GET'):  #Solo para GET
                        response_content = file_handler.read()
                    file_handler.close()

                    response_headers = self.header_http( 200)

                except Exception as e: # Generamos ERROR 404
                    print "Error 404: File not found\n", e
                    # Header HTTP de archivo no encontrado!
                    response_headers = self.header_http( 404)
                    
                    #Pagina por defecto para el error404
                    file_error404 = self.www_dir + "/ERROR404.html"
                    try:
                        file_handler = open(file_error404,'rb')
                        if (request_method == 'GET'):  #Solo para GET
                            response_content = file_handler.read()
                        file_handler.close()
                    
                    #Si la pagina por defecto no existe
                    except Exception as e:
                        print "Error 404: File not found\n", e
                        #response_headers = self.header_http( 404)                        
                        if (request_method == 'GET'):
                            response_content = b"<html><body><h1>Error 404: File not found</h1></body></html>"

                server_response =  response_headers.encode() # Retornamos Header
                if (request_method == 'GET'):
                    server_response +=  response_content  # Solo para GET

                conn.send(server_response)
                print "Cerrar conexion con el cliente"
                conn.close()
            else:
                print "HTTP request method no soportado!!! (unicamente GET y HEAD)", request_method
