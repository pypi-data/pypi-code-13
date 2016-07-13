#!/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import inspect
from peche.logging import level
from peche.logging import Event
from peche.logging.handlers import Handler

class Logger(object):

    level = level.Info
    default_levels = [level.Info, level.Warn, level.Error, level.Critical]

    def __init__(self, ctx):
        self.ctx = ctx
        self._handlers = {}

    def add_handler(self, handler, levels=None):
        if inspect.isclass(handler):
            handler = handler()

        if levels is None:
            if isinstance(handler, Handler):
                levels = handler.levels
            else:
                levels = self.default_levels

        for level_ in handler.levels:
            try:
                self._handlers[level_].append(handler)
            except KeyError:
                self._handlers[level_] = [handler]

    def remove_handler(self, handler, levels=None):
        if levels is None:
            if isinstance(handler, Handler):
                levels = handler.levels
            else:
                levels = self.default_levels

        for level_ in levels:
            if handler in self._handlers[level_]:
                self._handlers[level_].remove(handler)

    def _log(self, level_, event, **kwargs):
        timestamp = datetime.datetime.utcnow()

        if level_.value < self.level.value:
            return

        stack = inspect.stack()[2]

        path = stack[1]
        line_no = stack[2]
        function = stack[3]

        path = path[len(self.ctx.root)+1:-3].replace('/', '.')

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
        self._log(level.Debug, event, **kwargs)

    def info(self, event=None, **kwargs):
        self._log(level.Info, event, **kwargs)

    def warn(self, event=None, **kwargs):
        self._log(level.Warn, event, **kwargs)

    def error(self, event=None, **kwargs):
        self._log(level.Error, event, **kwargs)

    def critical(self, event=None, **kwargs):
        self._log(level.Critical, event, **kwargs)
