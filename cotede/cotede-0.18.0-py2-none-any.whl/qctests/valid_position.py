#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""

"""

import numpy as np
from numpy import ma


class Valid_Position(object):
    def __init__(self, data, varname, cfg):
        self.data = data
        self.varname = varname
        self.cfg = cfg

        self.set_features()

    def keys(self):
        return self.features.keys() + \
            ["flag_%s" % f for f in self.flags.keys()]

    def set_features(self):
        self.features = {}

    def test(self):
        self.flags = {}

        try:
            flag_good = self.cfg['flag_good']
            flag_bad = self.cfg['flag_bad']
        except:
            print("Deprecated cfg format. It should contain flag_good & flag_bad.")
            flag_good = 1
            flag_bad = 4

        if ('LATITUDE' in self.data) and ('LONGITUDE' in self.data):
            self.flags['valid_position'] = flag_good
            return

        if ('LATITUDE' in self.attributes) and \
                ('LONGITUDE' in self.attributes):
                    self.flags['valid_position'] = flag_good
                    return

        self.flags['valid_position'] = flag_bad        
