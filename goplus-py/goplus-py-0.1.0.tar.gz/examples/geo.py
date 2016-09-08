#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

device = things.Geo({{DID}})

while True:
    # get current coordinates from some function
    (lat, lon) =...  # your code here to request coordinates
    # lat, lon has to be float values

    resp = device.update(lat, lon)
    print("Result: " + resp)

    # sleep for 60 seconds
    time.sleep(60)
