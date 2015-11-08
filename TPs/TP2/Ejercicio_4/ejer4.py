#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket, os
from sys import argv
from lib.ClientTCP import ClientTCP

if __name__ == '__main__':
    c = ClientTCP('190.104.80.1', 80)
    print c.ping()
