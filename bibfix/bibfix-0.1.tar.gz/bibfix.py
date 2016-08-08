#!/usr/bin/env python3
import argparse
import re
import sys

import bibtexparser


def main():

    parser = argparse.ArgumentParser(
        description='Fixes unescaped acronyms in titles in bibtex files '
                    'by automatically detecting them and optionally parsing '
                    'them from a specification file.')

    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help='Encoding to use for parsing and writing the bib files')

    parser.add_argument(
        '-i', '--include',
        help='A file with strings to additionally escape. '
             'Each line marks a single string to protect with curly braces')

    parser.add_argument(
        'infile',
        metavar='INFILE',
        help='The bibtex file to process')
    parser.add_argument(
        'outfile',
        metavar='OUTFILE',
        help='The bibtex file to write to or - for stdout.')

    args = parser.parse_args()

    parser = bibtexparser.bparser.BibTexParser()
    parser.ignore_nonstandard_types = False
    with open(args.infile, encoding=args.encoding) as infile:
        database = bibtexparser.load(infile, parser=parser)

    if args.include:
        with open(args.include, encoding=args.encoding) as include_file:
            includes = include_file.readlines()
            includes = [s.strip() for s in includes if s.strip()]
        for entry in database.entries:
            for pattern in includes:
                entry['title'] = entry['title'].replace(
                    pattern, '{' + pattern + '}')

    acro_re = re.compile(r'(\w*[A-Z]\w*[A-Z]\w*)')
    for entry in database.entries:
        # matches = acro_re.finditer(entry['title'])
        entry['title'] = acro_re.sub(r'{\1}', entry['title'])

    if args.outfile == '-':
        bibtexparser.dump(database, sys.stdout)
    else:
        with open(args.outfile, 'w', encoding=args.encoding) as outfile:
            bibtexparser.dump(database, outfile)

if __name__ == "__main__":
    main()
