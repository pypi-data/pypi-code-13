#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ConstantPool(object):
    """
    An implementation of the JVM Constant Pool.
    """
    def __init__(self, cf, collapse=True):
        #: The ClassFile instance bound to this pool.
        self.cf = cf
        #: The 1-indexed table of Constants registered to this pool.
        self.index = {}
        #: Collapse duplicate constants into single table entries?
        self.collapse = collapse

    def __getitem__(self, idx):
        pass

    def __setitem__(self, idx, constant):
        pass
