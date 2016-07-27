# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 17:01:36
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-13 11:33:40


import os
import pygtrie
from digani.res.base import ResourceBase

class ResourceBreast(ResourceBase):

    res_names_path = os.path.join(os.path.dirname(__file__), 'names.json')
    res_trie_obj = pygtrie.CharTrie()

    def __init__(self):
        ResourceBase.__init__(self)
        self.load(names_path=os.path.join(os.path.dirname(__file__), 'breast_size.json'))
        self.load(names_path=os.path.join(os.path.dirname(__file__), 'breast_unit.json'))

    def load(self, trie_obj=res_trie_obj, names_path=res_names_path):
        super(ResourceBreast, self).load(trie_obj, names_path=names_path)

    def match(self, token):
        return super(ResourceBreast, self).match(token, ResourceBreast.res_trie_obj)

res_breast_obj = ResourceBreast()




"""
import os
import json
US_POSTAL_CODES_PATH = os.path.join(os.path.dirname(__file__), 'breast_unit.json')

def generate(path=US_POSTAL_CODES_PATH):
    output = os.path.join(os.path.dirname(__file__), 'breast_size_1.json')
    output = open(output, 'wb')
    with open(path, 'rb') as file_handler:
        ans = []
        for row in file_handler:
            if row.strip() not in ans:
                ans.append(row.strip())
            # print row
            # break
        output.write(json.dumps(ans, indent=2, sort_keys=True))
    output.close()
generate()
"""