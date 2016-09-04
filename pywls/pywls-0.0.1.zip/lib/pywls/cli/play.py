# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from pywls.cli import CLI


class PlayCLI(CLI):

    def __init__(self, args, callback=None):
        self.args = args
        self.options = None
        self.parser = None
        self.action = None
        self.callback = callback
