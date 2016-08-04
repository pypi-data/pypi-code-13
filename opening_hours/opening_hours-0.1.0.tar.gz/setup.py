#!/usr/bin/python

from setuptools import setup
from subprocess import call
import sys
import os
import codecs

if (len(sys.argv) > 1 and (sys.argv[1] == "build" or sys.argv[1] == "install")):
    if (call(["make", "-C", "C_OpeningHours"])):
        sys.exit(1)
    if (sys.argv[1] == "install"):
	if (call(["make", "-C", "C_OpeningHours", "install"])):
            sys.exit(1)
    else:
        sys.exit(0)

long_description = ''
if os.path.exists('README.md'):
    long_description = codecs.open('README.md', encoding='UTF-8', mode='r').read()

setup(
    name         = 'opening_hours',
    version      = '0.1.0',
    description  = 'Python wrapper embedding the C_OpeningHours writing on my own, implementation of the opening hours standard as described here: https://wiki.openstreetmap.org/wiki/Key:opening_hours',
    author       = 'Luka Boulagnon (Asphahyre) during internship at WeAreAnts.fr',
    author_email = 'asphahyre@geluti.org',
    url          = 'https://github.com/anthill/Python_OpeningHours',
    packages     = ['opening_hours'],
    license      = 'MIT',
    keywords     = ['OSM', 'OpenStreetMap', 'opening_hours'],
    install_requires=[
        'ctypes'
    ],
    long_description = long_description,
)

