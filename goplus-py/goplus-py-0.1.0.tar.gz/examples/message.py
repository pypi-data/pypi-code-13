#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Message({{DID}})

while True:
    # get message from some function
    message =...  # your code here to get message that you want to save on platform
    # message has to be string

    # send data to GO+ platform
    resp = device.update(message)
    print("Result: " + resp)

    # sleep for 60 seconds
    time.sleep(60)
