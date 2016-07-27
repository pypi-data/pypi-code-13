# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-10 21:50:44
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-25 19:38:15

import re
from digani.common.token_helper import tokenize

# reg_de_bracket = r'\(.*?\)'
# re_de_bracket = re.compile(reg_de_bracket)
# re_htmlc = re.compile(r'&\w+?;')
# re_de_unicode = re.compile(r'\\+u.*?\b')
re_space = re.compile(r'^(?:\s+|)$')
re_split = re.compile(r'[\s,]')

reg_clean = [
    # r'(?:\(.*?\))',  # remove content between bracket
    r'&\w+?;',
    r'\\+u.*?\b',
    r'\(.*?\)',
    r'\<.*?\>',
    r'(?:[\b\A\s]|^)\d+\)'
]
re_clean = re.compile(r'|'.join(reg_clean))

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
            if value == '':
                continue
            freq_dict.setdefault(value, 0)
            freq_dict[value] += 1
        return freq_dict

    @staticmethod
    def token_count(attr_vals):
        token_dict = {}
        for content in attr_vals:
            for token in content.split():
                if token == '':
                    continue
                token_dict.setdefault(token, 0)
                token_dict[token] += 1
        return token_dict

    @staticmethod
    def refine_attr_vals(attr_vals, refine, threshold=0.6, do_lower=True, do_tokenize=True, do_defreq=True, do_clean=True):
        # attr_vals = [re_de_unicode.sub('', _) for _ in attr_vals]
        # attr_vals = [' '.join(re_htmlc.sub('', _).split()) for _ in attr_vals]
        # attr_vals = [' '.join(re_de_bracket.sub('', _).split()) for _ in attr_vals]
        
        if do_lower:
            attr_vals = [_.lower() for _ in attr_vals]
        # print attr_vals
        if re_clean:
            attr_vals = [' '.join(re_clean.sub(' ', _).split()) for _ in attr_vals]
        # print attr_vals
        if do_tokenize:
            attr_vals = [tokenize(_) for _ in attr_vals]

        if do_defreq:
            freq_token_dict = {}
            size = 0
            for value in attr_vals:
                if value != '':
                    size += 1
                for token in value.split():
                    freq_token_dict.setdefault(token, 0)
                    freq_token_dict[token] += 1
            to_be_removed = []
            for (k, v) in freq_token_dict.iteritems():
                # print k, v
                if ((v != 0 and v % size == 0) or (float(v) / size >= threshold)) and size > 3:
                    to_be_removed.append(k)
            # print to_be_removed, size
            for i in range(len(attr_vals)):
                if to_be_removed:
                    attr_vals[i] = attr_vals[i].strip()
                    for tbrw in to_be_removed:
                        attr_vals[i] = ' '.join([_ for _ in attr_vals[i].split() if _ != tbrw]) #attr_vals[i].replace(tbrw, '')
        # print attr_vals
        attr_vals = refine(attr_vals)
        return [' '.join(_.split()) for _ in attr_vals]

    @staticmethod
    def pre_judge(attr_vals, custom_judge=None, disable_prejudge=False):

        if not disable_prejudge:
            # only none remains
            if len([_ for _ in attr_vals if not _ or _ == '' or re_space.match(_)]) == len(attr_vals):
                return False

            # only one value
            freq_dict = AttributeFunctionBase.frequent_count(attr_vals)
            # [_ for _ in freq_dict.keys() ]
            if freq_dict and len(freq_dict) == 1:
                return False

        if custom_judge != None and not custom_judge(attr_vals):
            return False
        return True

    @staticmethod
    def valid_counts(attr_vals, match, threshold=0.4):
        count = 0
        empty_count = 0
        size = len(attr_vals)
        for value in attr_vals:
            if not value or value == '':
                empty_count += 1
                continue
            if match(value):
                count += 1
        # print count, size, empty_count
        if count == 0:
            return False
        if float(count) / (size-empty_count) < threshold:
            return False
        return True



if __name__ == '__main__':
    attr_vals = [
        'Of hello',
        'of world',
        'of work',
        'of yes',
        'of ok',
        'sjkdflj',
        'foiwejfowi',
    ]
    obj = AttributeFunctionBase()
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
