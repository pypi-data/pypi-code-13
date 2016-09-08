#!/usr/bin/env python
# -*- coding: utf-8 -*-

from goplus import *


def set_value(x):
    result =...  # your code here to set state to requered value
    # result is the actually set value, which can be different from required
    return result


def get_value():
    value =...  # your code here to return some state
    return 0


device = things.Level({{DID}}, {{user_id}}, set_value, get_value)
device.start_loop()