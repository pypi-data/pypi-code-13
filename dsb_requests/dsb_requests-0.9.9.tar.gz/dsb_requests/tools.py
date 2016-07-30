#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-03-17 20:00:48
# Filename      : tools.py
# Description   : 
from __future__ import print_function, unicode_literals
import threading
from functools import wraps
import logging
import os

def utf8(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')

    else:
        return s

def get_log():
    log = logging.getLogger('dsb_requests')
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s %(asctime)s pid: %(process)s thread: %(threadName)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log

log = get_log()

def debug(msg):
    print(msg)
    if 'DEBUG_DSB' not in os.environ:
        return

    log.debug(utf8(msg))

def is_string(s):
    return isinstance(s, (str, unicode))

def is_list_or_tuple(data):
    return isinstance(data, (tuple, list))

def to_list(data):
    return data if is_list_or_tuple(data) else [data]

def async(func):
    @wraps(func)
    def innerwrap(*args, **kwargs):
        t = threading.Thread(target = func, args = args, kwargs = kwargs)
        t.setDaemon(True)
        t.start()

    return innerwrap

