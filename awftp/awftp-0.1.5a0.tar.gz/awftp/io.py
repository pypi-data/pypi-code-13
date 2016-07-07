from sys import __stdout__
from io import IOBase
from os import stat
from click import progressbar

from time import sleep

class R(IOBase):

    def __init__(self):
        super().__init__()
        self.isclosed = True
        self.atend = True

    def open(self, filename):
        size = stat(filename).st_size
        self.got = 0
        self.bar = progressbar(length=size, label='test', file=__stdout__)
        self.hdl = open(filename, 'rb')
        self.isclosed = False
        self.atend = False

    def close(self):
        self.hdl.close()
        self.isclosed = False
        self.bar.render_finish()

    def read(self):
        if self.atend or self.isclosed:
            return
        d = self.hdl.read(4096)
        if not len(d):
            self.atend = True
        self.got += len(d)
        self.bar.update(self.got)
        sleep(.1)
        return(d)
