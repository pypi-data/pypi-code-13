#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
"""
Utility to try nominatim
"""

import sys
sys.path.insert(0, "..")
from optparse import OptionParser
from nominatim import Nominatim

def parse_args():
    p = OptionParser(usage='%prog address',
           description='get nominatim metadata')
    options, args = p.parse_args()
    if len(args) < 1:
        p.error('not enough arguments')
    return  args

def main():
    addresses = parse_args()
    nom = Nominatim(base_url="http://nominatim.openstreetmap.org")

    for address in addresses:
        print "search:",address
        result=nom.query(address,limit=3)
        if len(result) >= 1:
            print result[0]["lat"]
            print result[0]["lon"]

    return 0

if __name__ == "__main__":
    sys.exit(main())
