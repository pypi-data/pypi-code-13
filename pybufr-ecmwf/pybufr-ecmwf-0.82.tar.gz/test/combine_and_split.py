#!/usr/bin/env python

'''
a little test script that combines several BUFR files
together, and then runs the sort tool
example_programs/sort_bufr_msgs.py to split them again.
'''

from __future__ import print_function
import os, glob

datadir = '../pybufr_ecmwf/ecmwf_bufr_lib/bufrdc_000405/data/'
datafiles = glob.glob(os.path.join(datadir, '*.bufr'))

print(__file__)
print(len(datafiles))
