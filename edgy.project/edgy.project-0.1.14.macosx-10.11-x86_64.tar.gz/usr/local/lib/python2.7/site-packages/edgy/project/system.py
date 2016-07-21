# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

import contextlib
import os

from edgy.event import Event


class ShellEvent(Event):
    def __init__(self, command):
        super(ShellEvent, self).__init__()

class ShellWrapper(object):
    def __call__(self, *args, **kwargs):
        os.system(*args, **kwargs)

@contextlib.contextmanager
def Shell(dispatcher):
    event = ShellEvent()

    event = dispatcher.dispatch('edgy.project.on_command', event)
    yield f
    event.file = None



