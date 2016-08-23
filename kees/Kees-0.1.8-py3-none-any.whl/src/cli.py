#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys

from . import kees


def get_parser():
    parser = argparse.ArgumentParser(description='translate words to or from'
                                     ' Dutch')
    parser.add_argument('word', metavar='WORD', type=str, nargs='*',
                        help='word to be translated')
    parser.add_argument('-f', '--from', type=str, default='NL',
                        help='available languages: NL, EN, DE, FR, SP'
                        ' (default: NL)')
    parser.add_argument('-t', '--to', type=str, default='EN',
                        help='available languages: NL, EN, DE, FR, SP'
                        ' (default: EN)')
    parser.add_argument('-a', '--all', action='store_true', help='return all'
                        ' translations (default 1)')
    return parser


def run():
    p = get_parser()
    args = vars(p.parse_args())

    if not args['word']:
        p.print_help()
        return

    try:
        kees.translate(args)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    run()
