#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Alert({{DID}})

while True:
    # get alert from some function
    alert =...  # your code here to check status and return True (alert) or False (everythig is ok)
    if alert:
        # send data to GO+ platform
        resp = device.update()
        print("Result: " + resp)
    # sleep for 5 seconds
    time.sleep(5)
