#!/usr/bin/env python
# -*- coding: utf-8 -*-
class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
