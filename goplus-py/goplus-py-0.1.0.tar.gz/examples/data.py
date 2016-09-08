#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Data({{DID}})

while True:
    # get data from some function
    data =...  # your code here to get data that you want to save on platform
    # data has to be int or float

    # send data to GO+ platform
    resp = device.update(data)
    print("Result: " + resp)

    # sleep for 60 seconds
    time.sleep(60)
