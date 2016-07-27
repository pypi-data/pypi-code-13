# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 14:54:19
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-08 14:58:57

import pygtrie as trie
import json
import re


def match_names(tokens, trie_obj):
    # copy from dig-name-extractor at
    # https://github.com/usc-isi-i2/dig-phrase-extraction/blob/master/scripts/name_extractor/name_extractor.py
    
    result = set()
    for token in tokens:
        token = re.search('[a-zA-Z].*[a-zA-Z]', token)
        if token:
            value = trie_obj.value.get(token.group(0))
            if isinstance(value, basestring):
                result.add(value)
    return result

def extract(text, trie_obj):
    tokens = text.split(' ')
    names = match_names(tokens, trie_obj)
    return list(names)