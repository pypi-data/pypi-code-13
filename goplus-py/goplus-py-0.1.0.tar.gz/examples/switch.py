#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *


def on():
    print("ON")
    # Your code here to execute on receiving command "ON"
    result =...
    # result has to be True or False
    return result


def off():
    print("OFF")
    # Your code here to execute on receiving command "OFF"
    result =...
    # result has to be True or False
    return result


device = things.Switch({{DID}}, {{user_id}}, on, off)
device.start_loop()