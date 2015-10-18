#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from datetime import datetime, timedelta
from pytz import timezone
import pytz

if __name__ == '__main__':
    utc = pytz.utc
    eastern = timezone('US/Eastern')
    amsterdam = timezone('Europe/Amsterdam')
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    loc_dt = eastern.localize(datetime(2002, 10, 27, 6, 0, 0))
    ams_dt = loc_dt.astimezone(amsterdam)
    print ams_dt.strftime(fmt)
