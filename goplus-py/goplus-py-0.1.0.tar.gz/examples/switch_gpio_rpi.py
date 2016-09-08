#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *

pin_number =...  # set number of GPIO pin that you want to use
pin = gpio.GPIO("rpi", pin_number, 'output')

device = things.Switch({{DID}}, {{user_id}}, pin.on, pin.off)
device.start_loop()