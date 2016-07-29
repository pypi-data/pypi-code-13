#!/usr/bin/env python
"""
Usage:
  rolodexer INFILE [-o OUTFILE] [-V | --verbose]
  rolodexer -h | --help | -v | --version
    
Options:
  -o OUTFILE --output=OUTFILE       specify output file [default: stdout]
  -V --verbose                      print verbose output
  -h --help                         show this text
  -v --version                      print version

"""

from __future__ import print_function
# from os.path import join, dirname
from os.path import exists, isdir, dirname
from docopt import docopt
from rolodexer.histogram import Histogram
import parser as rolodexer
import json
import sys

JSON_ARGS = dict(indent=2, sort_keys=True)

def print_colors(histo):
    print("Colors: %s" % len(histo), file=sys.stderr)
    for color, count in histo.iteritems():
        print("\t%15s\t\t%s" % (color, int(count)), file=sys.stderr)
    print('', file=sys.stderr)

def cli(argv=None):
    if not argv:
        argv = sys.argv
    
    arguments = docopt(__doc__, argv=argv[1:],
                                help=True,
                                version='0.1.2')
    
    # print(argv)
    # print(arguments)
    # sys.exit()
    
    entries = []
    errors  = []
    colors  = Histogram()
    
    ipth = arguments.get('INFILE')
    opth = arguments.get('--output')
    verbose = bool(arguments.get('--verbose'))
    
    with open(ipth, 'rb') as fh:
        idx = 0
        while True:
            linen = fh.readline()
            if not linen:
                break
            line = linen.strip()
            tokens = rolodexer.tokenize(line)
            try:
                terms = rolodexer.classify(tokens)
            except rolodexer.RolodexerError:
                errors.append(idx)
            else:
                entries.append(terms)
                if 'color' in terms:
                    colors.inc(terms.get('color'))
            idx += 1
        
        output_dict = { u"entries": entries, u"errors": errors }
        
        if verbose:
            print("Entries parsed: %s" % len(entries), file=sys.stderr)
            print("Errors encountered: %s" % len(errors), file=sys.stderr)
            print_colors(colors)
        
        if opth == 'stdout':
            output_json = json.dumps(output_dict, **JSON_ARGS)
            print(output_json, file=sys.stdout)
        elif not exists(opth) and isdir(dirname(opth)):
            if verbose:
                print("rolodexer: saving output to %s" % opth, file=sys.stderr)
            with open(opth, 'wb') as fp:
                json.dump(output_dict, fp, **JSON_ARGS)

if __name__ == '__main__':
    cli(sys.argv)