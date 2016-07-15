#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2016-07-12 15:39:15
# Filename      : __init__.py
# Description   : 
from __future__ import print_function, unicode_literals
import os
import vacuum.log

def scanning():
    for application_name, log_file in vacuum.log.ls():
        vacuum.log.analysis(application_name, log_file)

def backup():
    vacuum.log.sync2cdn()

