#!/usr/bin/env python
'''
    Main entry for pytomd
'''
from __future__ import absolute_import
import argparse
from pytomd.modules.manager import Manager


def menu():
    '''
    The Menu is here
    '''
    parser = argparse.ArgumentParser(
        description='output python to main README.md')
    parser.add_argument('-o',
                        action="store",
                        dest="output",
                        help='location to put README.md')
    parser.add_argument('-p',
                        action="store",
                        dest="path",
                        help='base path to scan files')
    parser.add_argument('-e',
                        action="store_true",
                        dest="execute",
                        default=False,
                        help='execute the values')
    parser.add_argument('-x',
                        action="store_true",
                        dest="example",
                        default=False,
                        help='Only output info with examples')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')
    return parser.parse_args()

def main():
    '''
    This is used in the cli and from a couple places
    '''
    options = menu()
    if options.execute:
        m1 = Manager(options.path,options)
if __name__ == '__main__':
    main()