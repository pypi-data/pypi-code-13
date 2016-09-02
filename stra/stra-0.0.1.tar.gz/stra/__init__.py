#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fst.py [args...] runs the command specified by args and prepend each output
line with [OUT] or [ERR], according to which stream it was written to.

The order of the output is not garanteed to be sequential accross different
streams.
"""

from __future__ import print_function

import array
import sys

from subprocess import PIPE, Popen

from fcntl import ioctl
from termios import FIONREAD
from time import sleep

from errno import ENOENT
from os import strerror

from os.path import basename


def usage(prog_path):
    print("Usage: %s prog [...]" % (basename(prog_path)))

try:
    # function that will write bytes to stdout
    write_bytes = sys.stdout.buffer.write
except AttributeError:
    write_bytes = sys.stdout.write


def write_output(out, name):
    lines = out.splitlines(True)
    for l in lines:
        write_bytes(name + l)
    sys.stdout.flush()


def main(*args):
    try:
        r = Popen(args, stdout=PIPE, stderr=PIPE)
    except OSError as e:
        print('Error opening %s: %s' % (args[0], strerror(e.errno)))
        return ENOENT

    while True:
        out = None
        for fd, name in [(r.stdout, b'[OUT] '),
                         (r.stderr, b'[ERR] ')]:
            buf = array.array('I', [0])
            ioctl(fd, FIONREAD, buf, True)
            readable_bytes = buf[0]

            if readable_bytes > 0:
                out = fd.read(readable_bytes)
                write_output(out, name)

        if not out and r.poll() is not None:
            return r.returncode

        sleep(0.01)


def entrypoint():
    if len(sys.argv) <= 1:
        usage(sys.argv[0])
        sys.exit()
    try:
        sys.exit(main(*sys.argv[1:]))
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    entrypoint()
