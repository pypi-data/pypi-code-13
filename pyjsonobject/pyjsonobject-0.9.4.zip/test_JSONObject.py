#!/usr/bin/python
# -*- coding: utf-8 -*-
from unittest import TestCase

import datetime

from JSONObject import JSONObject

__author__ = 'Marco Bartel'


class TestJSONObject(TestCase):
    def test_toJSON(self):
        class example(JSONObject):
            def __init__(self):
                self.a = "aString"
                self.b = 21
                self.c = JSONObject()
                self.c.b = "bString"
                self.c.v = 120
                self.d = unicode
                self.e = datetime.datetime.now()

        e = example()
        print e.toJSON()


