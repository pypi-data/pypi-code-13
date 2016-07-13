#!/usr/bin/env python
# -*- coding: utf8 -*-

from peche.logging.handlers import Stdout


class TextFileHandler(Stdout):

    file_handle = None

    def __init__(self, path=None, name='peche', file_handle=None):
        super().__init__()

        self.path = file_handle.name if file_handle else path or '/var/log/{name}.log'.format(name=name)
        self.file_handle = file_handle

    def setup(self):
        if self.file_handle is None:
            try:
                self.file_handle = self.open_handle()
            except IOError:
                raise

    def open_file_handle(self):
        self.file_handle = open(self.path, 'a')

    def format(self, template, event):
        return '{}\n'.format(super().format(template, event))

    def flush(self):
        self.handle.flush()

    def close(self):
        super().close()
        self.file_handle.close()

    def on_event(self, event):
        formatted = self.format(self.template(event), event)

        try:
            self.handle.write(formatted)
        except ValueError:
            self.open_file_handle()
            self.file_handle.write(formatted)
