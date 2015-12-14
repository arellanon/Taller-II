#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math, os, socket, ast
from Msg import Msg

class NodoMaster():

    def __init__(self, host, port, mappers, reducer, outfilename):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.listen = 5
        self.reducer = reducer
        self.mappers = mappers
        self.outfilename = outfilename

    def iniciar(self, filename):
        try :
            print "Iniciando proceso..."
            partes = self.dividir_file(filename, len(self.mappers))
    #        print partes
            socket_reducer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print 'conectando reducer: ',tuple(self.reducer)
                socket_reducer.connect(tuple(self.reducer))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket.", tuple(self.reducer)
                socket_reducer.close()
                import sys
                sys.exit(1)
            #Informamos el nro de partes en que fue dividido el archivo
            Msg(socket_reducer).send(1, str( len(partes) ))
            socket_reducer.close()
            
            #Repartimos las partes en los mappers
            self.repartir_mappers(filename, partes)
            
            self.iniciar_server()
            print 'Fin!'
        except KeyboardInterrupt:
           print "\nProceso finalizado"

    def iniciar_server(self):
        print 'Esperando resultados del reducer.'
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        
        try:
            print "Corriendo servidor - %s:%s" % (self.host, self.port)
            self.socket_server.bind((self.host, self.port))
        except Exception as e:
            print "ERROR: Falla en la conexion de socket."
            self.socket_server.close()
            import sys
            sys.exit(1)
        self.esperando_conexiones()
        
    def esperando_conexiones(self):
        print "Esperando conexiones..."
        self.socket_server.listen(self.listen)
        client_socket, client_addr = self.socket_server.accept()
        
        id, resultado = Msg(client_socket).recv()
        resultado = ast.literal_eval(resultado)
        outfile = open(self.outfilename, 'w')
        for k, v in resultado.iteritems():
             outfile.write('%s:%d\n' % ( k.encode('UTF-8'), v) )
        outfile.close()
        print 'El resultado se encuentra informado en: ', self.outfilename
        client_socket.close()
        self.socket_server.close()

    def repartir_mappers(self, filename, partes):
        infile = open(filename, 'r')
        for i in range(len(self.mappers)):
            id, byte_inicio, byte_fin = partes[i]
            socket_mapper = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print 'conectando mapper:  ',tuple(self.mappers[i])
                socket_mapper.connect(tuple(self.mappers[i]))
            except Exception as e:
                print "ERROR: Falla en la conexion de socket.", tuple(self.mappers[i])
                socket_mapper.close()
                import sys
                sys.exit(1)
            infile.seek(byte_inicio)
            Msg(socket_mapper).send(id, infile.read(byte_fin - byte_inicio))
            socket_mapper.close()
        infile.close()

    def dividir_file(self, filename, nro_partes):
        print "Dividiendo archivo"
        partes = []        
        byte_inicio = 0
        tamano = os.path.getsize(filename)
        tamano_parte = math.ceil(tamano / nro_partes)
        infile = open(filename, 'r')
        for i in range(1, nro_partes):
            if i == nro_partes: #ultima parte
                infile.seek(0, 2)
                byte_fin = infile.tell()
            else:
                infile.seek(i * tamano_parte)
                while True:
                    ch = infile.read(1)
                    if ch.strip():
                        break
                byte_fin = infile.tell() - 1
            partes.append((i, byte_inicio, byte_fin))
            byte_inicio = byte_fin
        partes.append((nro_partes, byte_inicio, tamano))
        infile.close()
        return partes
