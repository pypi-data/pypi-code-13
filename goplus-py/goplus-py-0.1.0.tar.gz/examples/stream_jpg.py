#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Stream({{DID}})

while True:
    # get image as a binary data from some function
    filename =...  # your code here to make image with webcam and save it to file

    # send data to GO+ platform
    resp = device.update_from_jpeg(filename)
    print("Result: " + resp)

    # sleep for 60 seconds
    time.sleep(60)
