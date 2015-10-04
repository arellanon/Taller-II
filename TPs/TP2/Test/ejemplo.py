#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from datetime import datetime, timedelta
from pytz import timezone
import pytz

if __name__ == '__main__':
    print "Hola mundo!"
    utc = pytz.utc
    print utc.zone
