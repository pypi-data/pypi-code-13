# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 13:40:38
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:42:35

import os
import pygtrie
from digani.res.base import ResourceBase


ETHNICITY_COLOR = [
    'White',
    'Black',
    'Yellow'
]

class ResourceEthnicity(ResourceBase):

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    # def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
    #     super(ResourceEthnicity, self).load(trie_obj, names_path=names_path)
    def load(self, trie_obj=res_trie_obj, names_path=res_names_path): 
        super(ResourceEthnicity, self).load(trie_obj, names_path=names_path)
        names = [' '.join([i, j]) for i, j in itertools.product(ETHNICITY_COLOR, trie_obj.keys())]
        super(ResourceEthnicity, self).load_names(trie_obj, names)
        

    def match(self, token):
        return super(ResourceEthnicity, self).match(token, ResourceEthnicity.res_trie_obj)

res_ethnicity_obj = ResourceEthnicity()