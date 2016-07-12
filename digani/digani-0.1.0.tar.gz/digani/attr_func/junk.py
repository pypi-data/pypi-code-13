# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 15:54:26
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:04:32

from base import AttributeFunctionBase

import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

reg_junks = [
    # r'[0-9]+.*[a-z]+',
    # r'[a-z]+.*[0-9]+'
    r'(?:\d+)'
]
re_junks = re.compile(r'^' + r'|'.join(reg_junks) + r'$')

class AttributeFunctionJunk(AttributeFunctionBase):

    @staticmethod
    def valid_junk(string):
        if re_junks.search(string):
            return True
        return False

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        freq_dict = super(AttributeFunctionJunk, AttributeFunctionJunk).frequent_count(attr_vals)
        if len(freq_dict.keys()) < 5:
            return True

        # tokens_size_dict = super(AttributeFunctionJunk, AttributeFunctionJunk).tokens_size(attr_vals)
        # if max([v for (k, v) in tokens_size_dict.iteritems()]) > 5:
        #     return True

        # attr_vals = super(AttributeFunctionJunk, AttributeFunctionJunk).refine_attr_vals(attr_vals, AttributeFunctionJunk.refine)

        if not super(AttributeFunctionJunk, AttributeFunctionJunk).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionJunk, AttributeFunctionJunk).valid_counts(attr_vals, AttributeFunctionJunk.valid_junk, threshold=0.4):
            return False

        return True






if __name__ == '__main__':
    text = ': 34-35 34 B Eyes: Brown Smokes: Yes but not with '
    # text = '2015'
    # print re_junks.findall(text)


"""
import re
# from digani.common import string_helper

re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')


def frequency_count(attr_vals):
    freq_dict = {}
    for value in attr_vals:
        freq_dict.setdefault(value, 0)
        freq_dict[value] += 1
    return freq_dict

def attr_func_junk(attr_vals):
    size = len(attr_vals)

    # number of attribute values, junk if less than 5
    freq_dict = frequency_count(attr_vals)
    if len(freq_dict.keys()) <= 5:
        return True

    # if string_helper.is_integer(content):
    for value in attr_vals:
        if not value or value == '':
            continue

        if re_junks.search(value):
            return True

    return False
"""