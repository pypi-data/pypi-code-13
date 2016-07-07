# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click
import re
import sys

PY2 = sys.version_info[0] == 2

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

if PY2:
    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda s: unicode(s).encode('utf-8')
        return cls
else:
    def implements_to_string(cls):
        return cls


def implements_comparable(cls):
    cls.__ne__ = lambda s, o: not s == o
    cls.__gt__ = lambda s, o: not s < o and not s == o
    cls.__ge__ = lambda s, o: not s < o
    return cls


_version_re = re.compile(
    '^'
    '(\d+)\.(\d+)\.(\d+)'  # minor, major, patch
    '(?:\.dev([0-9]+))?'  # dev
    '$')


@implements_comparable
@implements_to_string
class Version(object):
    def __init__(self, version):
        if not Version.check(version):
            raise ValueError('Invalid version.')
        (self.major, self.minor, self.patch, self.dev) = \
            map(lambda v: int(v) if v is not None else None,
                _version_re.search(version).groups())

    def __str__(self):
        res = '{s.major:d}.{s.minor:d}.{s.patch:d}'.format(s=self)

        if self.dev:
            res += '.dev{s.dev:d}'.format(s=self)

        return res

    def as_list(self):
        return list(
            filter(None, [self.major, self.minor, self.patch, self.dev]))

    def increase(self, which='patch'):
        if which == 'major':
            self.major += 1
            self.minor = 0
            self.patch = 0
            self.dev = None
        elif which == 'minor':
            self.minor += 1
            self.patch = 0
            self.dev = None
        elif which == 'patch':
            self.patch += 1
            self.dev = None
        elif which == 'dev':
            if self.dev is not None:
                self.dev += 1
            else:
                self.dev = 1
        else:
            raise ValueError('Unknown version part `{:s}`.'.format(which))

    def start_development(self):
        self.dev = 1

    def finish_development(self, which='patch'):
        self.increase(which)

    def __lt__(self, other):
        return self.as_list() < other.as_list()

    def __eq__(self, other):
        return self.as_list() == other.as_list()

    @classmethod
    def check(cls, version):
        return _version_re.search(version) is not None


def display_table(lines):
    columns = [max([len(line[i]) for line in lines])
               for i in range(len(lines[0]))]

    click.echo('-' * (sum(columns) + 2 * (len(columns) - 1)))

    for line in lines:
        click.echo('  '.join(['%-*s' % (s, line[x])
                              for x, s in enumerate(columns)]))

    click.echo('-' * (sum(columns) + 2 * (len(columns) - 1)))
