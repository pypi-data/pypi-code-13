# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-10 21:50:44
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 14:32:57

import re

reg_de_bracket = r'\(.*\)'
re_de_bracket = re.compile(reg_de_bracket)


class AttributeFunctionBase(object):

    @staticmethod
    def tokens_size(attr_vals):
        tokens_size_dict = {}
        for value in attr_vals:
            tokens_size.setdefault(value, len(value.split()))
        return tokens_size

    @staticmethod
    def frequent_count(attr_vals):
        freq_dict = {}
        for value in attr_vals:
            freq_dict.setdefault(value, 0)
            freq_dict[value] += 1
        return freq_dict

    @staticmethod
    def refine_attr_vals(attr_vals, refine, threshold=0.6):
        freq_token_dict = {}
        size = len(attr_vals)
        for value in attr_vals:
            for token in value.split():
                freq_token_dict.setdefault(token, 0)
                freq_token_dict[token] += 1
        to_be_removed = []
        for (k, v) in freq_token_dict.iteritems():
            if (v != 0 and v % size == 0) or (float(v) / size >= threshold):
                to_be_removed.append(k)

        for i in range(len(attr_vals)):
            if to_be_removed:
                attr_vals[i] = attr_vals[i].strip()
                for tbrw in to_be_removed:
                    attr_vals[i] = attr_vals[i].replace(tbrw, '')

        # attr_vals = [''.join([_.replace(tbrw, '').strip() for tbrw in to_be_removed]) if to_be_removed else _ for _ in attr_vals]
        attr_vals = [' '.join(re_de_bracket.sub('', _).split()) for _ in attr_vals]
        return refine(attr_vals)

    @staticmethod
    def pre_judge(attr_vals):
        return True

    @staticmethod
    def valid_counts(attr_vals, match, threshold=0.4):
        count = 0
        size = len(attr_vals)
        for value in attr_vals:
            if not value or value == '':
                continue
            if match(value):
                count += 1
        if count == 0:
            return False
        if float(count) / size < threshold:
            return False
        return True



if __name__ == '__main__':
    attr_vals = [
        'of hello',
        'of world',
        'of work',
        'of yes',
        'of ok',
        'sjkdflj',
        'foiwejfowi',
    ]
    obj = AttributeFunctionBase(attr_vals)
    # print obj.freq_dict
    print obj.attr_vals



"""

def initialize(self, attr_vals, threshold=0.3):
    # e.g. of <keyword>, remove of
    freq_dict = {}
    freq_token_dict = {}
    size = len(attr_vals)
    for value in attr_vals:
        for token in value.split():
            freq_token_dict.setdefault(token, 0)
            freq_token_dict[token] += 1
        freq_dict.setdefault(value, 0)
        freq_dict[value] += 1
    to_be_removed = []
    for (k, v) in freq_token_dict.iteritems():
        if (v != 0 and v % size == 0) or (float(v) / size >= threshold):
            to_be_removed.append(k)
    refiend_attr_vals = [''.join([_.replace(tbrw, '').strip() for tbrw in to_be_removed]) if to_be_removed else _ for _ in attr_vals]
    return freq_dict, refiend_attr_vals
"""
