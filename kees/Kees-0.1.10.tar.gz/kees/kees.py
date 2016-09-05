#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, FeatureNotFound

from re import sub
from random import choice

from urllib.request import urlopen
from urllib.parse import quote
from urllib.error import HTTPError

import argparse
import sys

SEARCH_URL = 'http://www.mijnwoordenboek.nl/vertaal/{from}/{to}/{word}'
LANGUAGES = ['nl', 'en', 'de', 'fr', 'es']

# style attrib of the font tag that contains the translation
FONT_STYLE = 'color:navy;font-size:10pt'
# div that contains the 'other sources' translations:
to_DIV = '.span8 > div:nth-of-type(1)'


def _get_response(url):
    try:
        return urlopen(url)
    except HTTPError:
        raise


def _get_soup(args):
    response = _get_response(SEARCH_URL.format_map(args))
    try:
        return BeautifulSoup(response, 'lxml')
    except FeatureNotFound as e:
        raise ImportError('Please install the lxml module ({})'.format(e))


def _get_translations(soup):
    div = soup.select(to_DIV + '> font')
    return [word for group in [elem.text.split(',') for elem in div
            if FONT_STYLE in elem['style']] for word in group]


def _get_other_sources(soup):
    tables = soup.select(to_DIV + '> table')
    other_sources = []
    for t in tables:
        # if 'border' in t:     # does not return anything
        if t.get('border', None) is not None:
            for td in t('td'):
                # if 'style' in td:
                if td.get('style', None) is not None:
                    other_sources.extend([w for w in
                                          td.text.split(';')])
    return other_sources


def _process(trs):
    clean_words = set()
    for t in trs:
        stripped = t.strip()
        subbed = sub(r'\s+[\(].*[\)]', '', stripped)
        clean_words.add(subbed)
    return clean_words


def _parse_elements(args):
    soup = _get_soup(args)
    raw_translations = _get_translations(soup) + _get_other_sources(soup)
    translations = _process(raw_translations)
    return translations


def translate(args):
    args['word'] = quote(' '.join(args['word']).strip())
    if args['to']:
        args['from'] = 'nl'
    elif args['from']:
        args['to'] = 'nl'

    translations = sorted(list(_parse_elements(args)))

    if args['random'] is True:
        result = choice(translations)
    else:
        result = '\n'.join([w for w in translations])

    print('{}'.format(result))


def run():
    parser = argparse.ArgumentParser(description='translate words to or from'
                                     ' Dutch')
    parser.add_argument('word', metavar='WORD', type=str, nargs='*',
                        help='word to be translated')
    parser.add_argument('-f', '--from', type=str,
                        help='available languages: nl, en, de, fr, sp'
                        ' (default: nl)')
    parser.add_argument('-t', '--to', type=str,
                        help='available languages: nl, en, de, fr, sp'
                        ' (default: en)')
    parser.add_argument('-r', '--random', action='store_true', help='return a'
                        ' random translation')

    args = vars(parser.parse_args())

    if not args['word']:
        parser.print_help()
        return

    try:
        translate(args)
    except (ValueError, IndexError) as e:
        print('no translation found')
        sys.exit(1)
