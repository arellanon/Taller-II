#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, os, sys, subprocess

proc = subprocess.Popen('echo $HOME', shell=True)
#p1 = subprocess.Popen( 'ls', stdout=subprocess.PIPE)
#p2 = subprocess.Popen( 'ls', stdin=p1.stdout, stdout=subprocess.PIPE)
#output = p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits
#output = p2.communicate()[0]
#print output
