# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 13:40:38
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 10:14:56

import os
import pygtrie
from digani.res.base import ResourceBase

class ResourceCity(ResourceBase):

    # res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_names_path = os.path.join(os.path.dirname(__file__), 'names_small.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
        super(ResourceCity, self).load(trie_obj, names_path=names_path)

    def match(self, token):
        return super(ResourceCity, self).match(token, ResourceCity.res_trie_obj)

res_city_obj = ResourceCity()


"""
import os
import json
import codecs
import pygtrie
from digani.common import trie_helper

# RES_CITY_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'names.json')
RES_CITY_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'names_small.json')

city_names_trie_obj = pygtrie.CharTrie()

def load(names_path=RES_CITY_NAMES_PATH):
    global city_names_trie_obj

    if not city_names_trie_obj or names_path:
        names = json.load(codecs.open(names_path, 'r', 'utf-8'))
        trie_obj = trie_helper.load_trie_obj(city_names_trie_obj, names)
        city_names_trie_obj = trie_obj

    return city_names_trie_obj

city_names_trie_obj = load()

def match(token):
    return trie_helper.match_names(token, city_names_trie_obj)
    
if __name__ == '__main__':
    pass
"""