#!/usr/bin/env python
# -*- coding: utf8 -*-

import inspect
from peche.context import Context
from peche.logging import Logger
from peche.logging.handlers import Stdout
import sys


class Manager(object):
    __state = {}
    contexts = {}

    def __init__(self):
        self.__dict__ = self.__state

    def setup(self, name=None, root=None, logger=None):
        if name is None or root is None:
            stack = inspect.getframeinfo(sys._getframe(1), 0)

            path = stack.filename

            components = path.split('/')

            name = name or components[-2]
            root = root or '/'.join(components[0:-1])

        try:
            context = self.contexts[name]
            return context, context.logger
        except KeyError:
            pass

        context = Context(name, root)

        if logger is None:
            logger = Logger(context)
            logger.add_handler(Stdout)

        context.logger = logger

        self.contexts[name] = context

        return context, context.logger