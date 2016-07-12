# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 13:40:38
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-11 18:01:40

import os
import pygtrie
from digani.res.base import ResourceBase

class ResourceCountry(ResourceBase):

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load()

    def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
        super(ResourceCountry, self).load(trie_obj, names_path=names_path)

    def match(self, token):
        return super(ResourceCountry, self).match(token, ResourceCountry.res_trie_obj)

res_country_obj = ResourceCountry()