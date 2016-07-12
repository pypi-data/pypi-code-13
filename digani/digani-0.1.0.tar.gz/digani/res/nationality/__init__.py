# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-12 15:58:26
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:31:06

import os
import pygtrie
from digani.res.base import ResourceBase

class ResourceNationality(ResourceBase):

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
        super(ResourceNationality, self).load(trie_obj, names_path=names_path)

    def match(self, token):
        return super(ResourceNationality, self).match(token, ResourceNationality.res_trie_obj)

res_nationality_obj = ResourceNationality()