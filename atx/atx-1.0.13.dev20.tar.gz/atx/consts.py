#!/usr/bin/env python
# -*- coding: utf-8 -*-

SCREENSHOT_METHOD_UIAUTOMATOR = 'uiautomator'
SCREENSHOT_METHOD_MINICAP = 'minicap'
SCREENSHOT_METHOD_AUTO = 'auto'

IMAGE_MATCH_METHOD_TMPL = 'template'
IMAGE_MATCH_METHOD_SIFT = 'sift'

EVENT_UIAUTO_TOUCH = 1 << 0
EVENT_UIAUTO_CLICK = 1 << 0 # alias for touch
EVENT_UIAUTO_SWIPE = 1 << 2

EVENT_SCREENSHOT = 1 << 3
EVENT_CLICK = 1 << 4
EVENT_CLICK_IMAGE = 1 << 5

EVENT_ALL = EVENT_SCREENSHOT | EVENT_CLICK | EVENT_CLICK_IMAGE
# 1 - 2 - 3
# 4 - 5 - 6
# 7 - 8 - 9

NW = 1
N = 2
NE = 3
W = 4
E = 6
SW = 7
S = 8
SE = 9
