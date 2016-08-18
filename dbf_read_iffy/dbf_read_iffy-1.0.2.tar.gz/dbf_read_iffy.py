# -*- coding: utf-8 -*-

"""
Make possible to read from dbf's with codepage unsupported by modules dbf and codecs (895 cz Kamenicky, ..)


import dbf
from dbf_read_iffy import fix_init, fix_895

fix_init(dbf)
t = dbf.Table('autori.dbf')
t.open('read-only')
for record in t:
    print fix_895(record.autor)
t.close()
"""


from __future__ import unicode_literals   # must be 1st import


def fix_620(txt):
    """
    convert 620 pl Mazovia if imported as 437

    NOT IMPLEMENTED YET
    """

    # TODO: implement Mazovia
    return fix_iffy(txt, {})

def fix_895(txt):
    """
    convert 895 cz Kamenicky if imported as 437

    https://cs.wikipedia.org/wiki/K%C3%B3d_Kamenick%C3%BDch
    https://en.wikipedia.org/wiki/Code_page_437
    http://www.rapidtables.com/code/text/unicode-characters.htm
    """

    return fix_iffy(txt, {
        '\xc7': 'Č',
        # '\xfc': 'ü',
        # '\xe9': 'é',  # 130
        '\xe2': 'ď',
        # '\xe4': 'ä',
        '\xe0': 'Ď',
        '\xe5': 'Ť',
        '\xe7': 'č',  # 135
        '\xea': 'ě',
        '\xeb': 'Ě',
        '\xe8': 'Ĺ',
        '\xef': 'Í',
        '\xee': 'ľ',  # 140
        '\xec': 'ĺ',
        '\xc4': 'Ä',
        '\xc5': 'Á',
        # '\xc9': 'É',
        '\xe6': 'ž',  # 145
        '\xc6': 'Ž',
        # '\xf4': '\xf4',  # o vokan
        # '\xf6': 'ö',
        '\xf2': 'Ó',
        '\xfb': 'ů',  # 150
        '\xf9': 'Ú',
        '\xff': 'ý',
        # '\xd6': 'Ö',
        # '\xdc': 'Ü',
        '\xa2': 'Š',  # 155
        '\xa3': 'Ľ',
        '\xa5': 'Ý',
        '\u20a7': 'Ř',
        '\u0192': 'ť',
        # '\xe1': 'á',  # 160
        # '\xed': 'í',
        # '\xf3': 'ó',
        # '\xfa': 'ú',
        '\xf1': 'ň',
        '\xd1': 'Ň',  # 165
        '\xaa': 'Ů',
        '\xba': '\xd4',  # O vokan
        '\xbf': 'š',
        '\u2310': 'ř',
        '\xac': 'ŕ',  # 170
        '\xbd': 'Ŕ',
        })

def fix_iffy(txt, conversion_map):
    retval = ''
    for ch in txt:
        retval += conversion_map.get(ch, ch)
    return retval

def fix_init(dbf):
    if dbf.code_pages['h'][0] is None:
        dbf.code_pages['h'] = ('cp437', 'Kamenicky (Czech) MS-DOS')
    if dbf.code_pages['i'][0] is None:
        dbf.code_pages['i'] = ('cp437', 'Mazovia (Polish) MS-DOS')
