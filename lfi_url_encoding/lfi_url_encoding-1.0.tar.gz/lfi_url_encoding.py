#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Author : Alexandre ZANNI
# tested with python 3.4.1 & 3.5.2
# linted with pep8 1.7.0 :
#   http://pep8.readthedocs.io/en/release-1.7.x/intro.html#feature

# Lib for argument parsing
import argparse

# Description for help
parser = argparse.ArgumentParser(
            description='LFI-encoding - Encoding url for LFI',
            epilog="Author : Alexandre ZANNI")
# create a group for incompatible options
group = parser.add_mutually_exclusive_group(required=True)
# simple or double encoding
group.add_argument('-s', '--simple', help='Simple encoding',
                   metavar='<string>', required=False)
group.add_argument('-d', '--double', help='Double encoding',
                   metavar='<string>', required=False)
# optional args
parser.add_argument('-a', '--advanced', action="store_true", default=False,
                    help='Advanced encoding (\'&\', \'+\', \'=\')',
                    required=False)
parser.add_argument('-n', '--null_byte', action="store_true", default=False,
                    help='Append a null byte', required=False)

# get args
args = parser.parse_args()

"""
# if no args then print the help
if len(vars(args)) == 0:
    parser.print_help()
"""

# basic dict
UTF8_enc = {'.': '2E', '/': '2F', ' ': '20', '!': '21', '\"': '22', '#': '23',
            '$': '24', '\'': '27', '(': '28', ')': '29', '*': '2A', ';': '3B',
            '<': '3C', '>': '3E', '[': '5B', ']': '5D', '\\': '5C', '^': '5E',
            '`': '60', '{': '7B', '}': '7D', '|': '7C'}
UTF8_extra = {'&': '26', '+': '2B', '-': '2D', ':': '3A', '=': '3D', '?': '3F',
              '@': '40', '_': '5F', '~': '7E'}
# advanced dict
if args.advanced:
    UTF8_enc.update(UTF8_extra)

# find the option chosen
if(args.simple is not None):
    option = args.simple
    base = '%'
elif(args.double is not None):
    option = args.double
    base = '%25'
else:
    raise ValueError

# process the URL
out = ''
# cc = current char
for cc in option:
    if(cc in UTF8_enc):
        cc = base + UTF8_enc[cc]
    out += cc

# Option null byte
if args.null_byte:
    out += base + '00'

# print the output
print(out)
