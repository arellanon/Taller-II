#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, os, sys
from lib.ServerSsh import ServerSsh
import subprocess

if __name__ == '__main__':

#    if(len(sys.argv) < 2) :
#        print 'Usar: python test.py comando'
#        sys.exit()
#    comando = sys.argv[1]
#    os.system("cd /home/")
#    os.system(comando)
    
    
#    output = subprocess.check_output("ls", shell=True)
#    print output
    
#    s = ServerSsh()
#    s.iniciar_server()

    import subprocess

    os.environ['a'] = '/home'
    os.environ['b'] = '/'

    subprocess.call('cd $a', shell=True)
    subprocess.call('ls', shell=True)

    subprocess.call('cd $b', shell=True)
    subprocess.call('ls', shell=True)
