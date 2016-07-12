# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-09 10:58:11
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 12:33:08

import pygtrie

def load_trie_obj(trie_obj, words):
    for word in words:
        trie_obj[word] = word
    return trie_obj

def match_names(word, trie_obj):
    word = word.strip().lower()
    return trie_obj.has_key(word)

def contain_names(word, trie_obj):
    word = word.strip().lower()
    for key in trie_obj.iterkeys():
        if word in key.split():
            return True
    return False

if __name__ == '__main__':

    test_word = 'oak'

    words = [
        "whitestone point",
        "white earth",
        "white house acres",
        "white pump",
        "white tower",
        "south whiteville",
        "white horse farm",
        "whitewood estates",
        "white hollow",
        "white oak run"
    ]
    trie_obj = pygtrie.CharTrie()
    trie_obj = load_trie_obj(trie_obj, words)
    print contain_names(test_word, trie_obj)