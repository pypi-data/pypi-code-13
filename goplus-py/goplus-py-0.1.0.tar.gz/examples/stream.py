#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Stream({{DID}})

while True:
    # get image as a binary data from some function
    data =...  # your code here to get image data from webcam

    # send data to GO+ platform
    resp = device.update(data)
    print("Result: " + resp)

    # sleep for 60 seconds
    time.sleep(60)
