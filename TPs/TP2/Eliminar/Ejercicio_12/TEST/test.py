#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from subprocess import Popen, PIPE
#comando = "ls "

p1 = Popen(["cd cosa"], stdout=PIPE, cwd= '1/')
p2 = Popen(["ls"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]

print output
"""

print os.path.dirname(os.path.realpath(__file__))
comando = raw_input("comando: ")
#lista = [, 'ls']
#print lista
proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd= '1/', shell=True) 
#(salida, err) = p.communicate()


error_econtrado = proceso.stderr.read()
proceso.stderr.close()


entrada = proceso.stdout
listado = proceso.stdout.read()
proceso.stdout.close()

print listado
print proceso.STARTUPINFO
#print os.path.abspath(proceso.stdout.name())

comando = raw_input("comando: ")
proceso2 = subprocess.Popen(comando, stdin=proceso, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd= '1/', shell=True) 

#entrada = proceso.stdin.read()
#proceso.stdin.close()
listado = proceso.stdout.read()
proceso.stdout.close()

print listado



if error_econtrado:
    print error_econtrado
else:
    print listado
#print salida
#print err
"""

