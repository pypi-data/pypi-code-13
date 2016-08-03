# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals


class Browser(object):
    def __init__(self, name, **kw):
        self._name = name
        self._kw = {}
        self._verbose = 0
        # self._vnc = kw.get('vnc')

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = int(val)


class NoSuchElementException(Exception):
    pass
