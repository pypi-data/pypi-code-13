#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import inspect
from peche.logging import Level
from peche.logging import Event
from peche.logging.handlers import Handler
import sys


class Logger(object):

    def __init__(self, ctx, level_=Level.Info, default_levels=None,
                 inspection=False):
        self.ctx = ctx
        self._handlers = {}
        self.level = level_
        self.default_levels = default_levels or [Level.Debug, Level.Info,
                                                 Level.Warn, Level.Error,
                                                 Level.Critical]
        self.inspection = inspection

    def add_handler(self, handler, levels=None):
        if inspect.isclass(handler):
            handler = handler()

        if isinstance(handler, Handler):
            handler.setup()

        if levels is None and isinstance(handler, Handler):
            levels = handler.levels
        elif levels is None:
            levels = self.default_levels

        for level_ in levels:
            try:
                self._handlers[level_].append(handler)
            except KeyError:
                self._handlers[level_] = [handler]

    def remove_handler(self, handler, levels=None):
        if levels is None and isinstance(handler, Handler):
            levels = handler.levels
        elif levels is None:
            levels = self.default_levels

        for level_ in levels:
            try:
                self._handlers[level_].remove(handler)
            except ValueError:
                pass

        if isinstance(handler, Handler):
            handler.close()

    def drop_handlers(self):
        self._handlers = {}

    def _log(self, level_, event, **kwargs):
        timestamp = datetime.datetime.utcnow()

        if level_.value < self.level.value:
            return

        if self.inspection:
            stack = inspect.getframeinfo(sys._getframe(2), 0)

            path = stack.filename
            line_no = stack.lineno
            function = stack.function

            path = path[len(self.ctx.root)+1:-3].replace('/', '.')
        else:
            path = None
            line_no = None
            function = None

        event = Event(
            timestamp=timestamp,
            level=level_,
            ctx=self.ctx,
            function=function,
            path=path if path != '' else None,
            line_no=line_no,
            message=event,
            tags=kwargs
        )

        for handler in self._handlers[level_]:
            if isinstance(handler, Handler):
                handler.on_event(event)
            else:
                handler(event)

    def debug(self, event=None, **kwargs):
        self._log(Level.Debug, event, **kwargs)

    def info(self, event=None, **kwargs):
        self._log(Level.Info, event, **kwargs)

    def warn(self, event=None, **kwargs):
        self._log(Level.Warn, event, **kwargs)

    def error(self, event=None, **kwargs):
        self._log(Level.Error, event, **kwargs)

    def critical(self, event=None, **kwargs):
        self._log(Level.Critical, event, **kwargs)
