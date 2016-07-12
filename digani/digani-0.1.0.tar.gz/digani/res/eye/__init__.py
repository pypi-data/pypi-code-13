# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 17:56:52
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:29:59

import os
import pygtrie
import itertools
from digani.res.base import ResourceBase

RES_EYE_COLOR_LEVEL = [
    'Light',
    'Dark'
]

RES_EYE_COLOR = [
    'Brown',
    'Hazel'
]

class ResourceEye(ResourceBase):

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    # def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
    #     super(ResourceEye, self).load(trie_obj, names_path=names_path)
    
    def load(self, trie_obj=res_trie_obj, names_path=None): 
        if names_path:
            super(ResourceEye, self).load(trie_obj, names_path=names_path)
        else:
            names = [' '.join([i, j]) for i, j in itertools.product(RES_EYE_COLOR_LEVEL, RES_EYE_COLOR)] + RES_EYE_COLOR
            super(ResourceEye, self).load_names(trie_obj, names)

    def match(self, token):
        return super(ResourceEye, self).match(token, ResourceEye.res_trie_obj)

res_eye_obj = ResourceEye()