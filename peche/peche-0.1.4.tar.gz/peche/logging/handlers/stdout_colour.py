#!/usr/bin/env python
# -*- coding: utf8 -*-

from termcolor import cprint
from peche.logging.handlers import Stdout
from peche.logging import Level
from sys import stdout, stderr

class StdoutColourHandler(Stdout):

    level_to_colour = {
        Level.Debug: 'blue',
        Level.Info: 'green',
        Level.Warn: 'yellow',
        Level.Error: 'red',
        Level.Critical: 'magenta'
    }

    def on_event(self, event):
        file = stderr if event.level in self.stderr_levels else stdout

        cprint(self.format(self.template(event), event),
               self.level_to_colour[event.level],
               file=file)
