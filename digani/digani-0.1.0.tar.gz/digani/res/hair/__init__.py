# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 17:57:13
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:29:49


"""
Hair Attributes:
- Color
- Length
- Type

"""

import os
import pygtrie
import itertools
from digani.res.base import ResourceBase

RES_HAIR_COLOR_LEVEL = [
    'Light',
    'Dark'
]

RES_HAIR_COLOR = [
    'Blond',
    'Blonde',
    'Red',
    'Brown',
    'Black',
    'Grey',
    'White',
    'Brunet',
    'Brunette'
]

RES_HAIR_LENGTH = [
    'Long',
    'Mid Back',
    'Shoulder'
]

RES_HAIR_TYPE = [
    'Straight',
    'Curls',
    'Curl',
]

class ResourceHair(ResourceBase):

    # res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    # def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
    #     super(ResourceHair, self).load(trie_obj, names_path=names_path)
    
    def load(self, trie_obj=res_trie_obj, names_path=None): 
        if names_path:
            super(ResourceHair, self).load(trie_obj, names_path=names_path)
        else:
            names = [' '.join([i, j]) for i, j in itertools.product(RES_HAIR_COLOR_LEVEL, RES_HAIR_COLOR)] + RES_HAIR_COLOR + RES_HAIR_LENGTH + RES_HAIR_TYPE
            super(ResourceHair, self).load_names(trie_obj, names)
            
    def match(self, token):
        return super(ResourceHair, self).contain(token, ResourceHair.res_trie_obj)

res_hair_obj = ResourceHair()
