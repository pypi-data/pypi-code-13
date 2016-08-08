#!/usr/bin/env python
# -*- coding: utf8 -*-

from peche.logging import Level


class Handler(object):

    levels = [Level.Debug, Level.Info, Level.Warn, Level.Error,
              Level.Critical]

    def setup(self):
        pass

    def on_event(self, event):
        pass

    def flush(self):
        pass

    def close(self):
        self.flush()
