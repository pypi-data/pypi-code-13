# -*- coding: utf-8 -*-
"""


"""

from __future__ import absolute_import

import logging

import numpy as np
import quantities as pq
import h5py

from neo.core import objectlist, Block
from neo.io.baseio import BaseIO

logger = logging.getLogger('Neo')


class NeoHdf5IO(BaseIO):
    supported_objects = objectlist
    readable_objects = objectlist
    name = 'NeoHdf5 IO'
    extensions = ['h5']
    mode = 'file'
    is_readable = True
    is_writable = False

    def __init__(self, filename):
        BaseIO.__init__(self, filename=filename)
        self._data = h5py.File(filename, 'r')

    def read_all_blocks(self, lazy=False, cascade=True, **kargs):
        """
        Loads all blocks in the file that are attached to the root (which
        happens when they are saved with save() or write_block()).
        """
        if cascade is not True:
            raise ValueError("cascade = {} is not supported".format(cascade))
        if lazy is True:
            raise ValueError("lazy loading is not supported")

        blocks = []
        for name, node in self._data.iteritems():
            if "Block" in name:


        return blocks

    def read_block(self, path='/', cascade=True, lazy=False):

        return block
