# -*- coding: utf-8 -*-

import chardet

ENCODINGS_TO_TRY = (
    'utf-8',
    'windows-1252',
    'latin-1',
    'macroman',
)

def to_unicode(text, encodings_to_try=ENCODINGS_TO_TRY):
    if isinstance(text, unicode):
        return text

    # we punt our way through, hoping that thigs
    # will blow up if we're wrong
    #
    # windows-1252 and latin-1 are very similiar,
    # it may be worthwhile pulling them out
    for encoding in encodings_to_try:
        try:
            return text.decode(encoding)
        except UnicodeDecodeError:
            continue

    # okay, so we are still getting errors, we should
    # take a proper look
    guess = chardet.detect(text)
    encoding = guess['encoding']
    return text.decode(encoding)

def to_str(text):
    return to_unicode(text).encode('utf-8')
