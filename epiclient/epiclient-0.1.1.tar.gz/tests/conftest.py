# -*- coding: utf-8 -*-

import os

cwd = os.getcwd()


def pytest_addoption(parser):
    parser.addoption(
            '--runlive', action='store_true',
            help='test with live capture agents')


def read_datafile(filename):
    filename = os.path.join(cwd, 'tests/json/%s.json' % filename)
    data = ''
    with open(filename, 'r') as myfile:
        data = myfile.read()

    return data.rstrip()  # read() adds a newline at the end of the file??
