#!/usr/bin/env python
# -*- coding: utf8 -*-

import inspect
from peche.configuration import Configuration
import sys


class Context(object):
    root = None
    name = None
    logger = None
    meta = {}
    config_root = None

    def __init__(self, name, root, config_root='/etc'):
        self.name = name
        self.root = root
        self.config_root = '{root}/{name}'.format(root=config_root,
                                                  name=name)

    def get_config(self):
        stack = inspect.getframeinfo(sys._getframe(1), 0)

        path = stack.filename[:-3]
        path = path[path.find(self.name):]
        path += '.{}'.format(stack.function)

        return Configuration(self, path)