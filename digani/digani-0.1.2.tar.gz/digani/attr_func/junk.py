# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 15:54:26
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-18 18:07:58

from digani.res.city import res_city_obj
from digani.res.state import res_state_obj
from digani.res.country import res_country_obj
from digani.common import gram_helper
from base import AttributeFunctionBase
from pnmatcher import PhoneNumberMatcher
matcher = PhoneNumberMatcher()

import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')
# re_punctuations = re.compile(r'[!"#\$%&\'()\*\+,-\./:;<=>\?@\[\\]\^_`{\|}~]')



"""
--> 4. 1 --> Ms.Pretty Kittyy --> 4. 1 --> Vicki --> 4. 1 --> Domina Venus --> 4. 1 --> Amy --> 4. 1 --> Kandi --> 4. 1 --> Jezabel --> 4. 1 --> Lisa --> 4. 1 --> Kristen Vanhaughton --> 4. 1 --> Kim ...
"""

reg_junks = [
    r'(?:^\d+?\s+?(?:second|minute|hour|day|week|year)s?$)',
    r'(?:^\d+?\s*?:?\s*?\d+?\s*?(?:am|pm)$)',
    r'(?:^[\d\s:\.]+$)',
    r'(?:^(?:\s*?<!--.*?-->\s*?)$)',
    # r'(?:(?<=\b-->\b)\s*\w+)+',
    r'(?:[\s\w]+?-->[\s\w]+?-->[\s\w]+?)',
    r'(?:^\s*?-->\s*?$)',
    r'(?:\s*?<.*?>\s*?){3,}',
    r'(?:^[\s\-]*?(?:\b[a-zA-Z]+\b){,5}[\s\-]*?$)'
]
re_junks = re.compile(r'(?:'+r'|'.join(reg_junks)+r')')

class AttributeFunctionJunk(AttributeFunctionBase):

    @staticmethod
    def valid_junk(string):
        def multiple_locations(string):
            ht = {}

            pot = [] # string.split()
            pot += gram_helper.generate_strngram(string, 2)
            pot += gram_helper.generate_strngram(string, 3)

            for extraction in pot:
                if res_city_obj.match(extraction):
                    ht.setdefault(extraction, 0)
                    ht[extraction] += 1
                if len(ht) > 5:
                    # print ht, len(ht)
                    return True
            
            return False

        def multiple_telephones(string):
            extraction = matcher.match(string, source_type='text')
            if len(extraction) > 1:
                return True
            return False

        # def valid_digit_length(string):
        #     digits = re_digits.findall(string)
        #     # digits = ''.join(digits)
        #     for digit in digits:
        #         if 4 >= len(digit) or len(digit) > 8: #20160712
        #             return False
        #         if not (int(digit) > 0 and int(digit)  < 31):
        #             return False
        #     return True

        # if len(string.split()) < 10:
        #     if not valid_digit_length(string):
        #         return True

        if multiple_locations(string):
            return True
        if multiple_telephones(string):
            return True

        if re_junks.search(string):
            # print 're_junks'
            return True
        # print 'not junk'
        return False

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):

        def sparse_value(attr_vals, threshold=5):
            freq_dict = super(AttributeFunctionJunk, AttributeFunctionJunk).frequent_count(attr_vals)
            if len(freq_dict.keys()) < threshold:
                return True

            token_dict = super(AttributeFunctionJunk, AttributeFunctionJunk).token_count(attr_vals)
            # print token_dict
            if len(token_dict.keys()) < threshold:
                return True

            return False

        # tokens_size_dict = super(AttributeFunctionJunk, AttributeFunctionJunk).tokens_size(attr_vals)
        # if max([v for (k, v) in tokens_size_dict.iteritems()]) > 5:
        #     return True

        attr_vals = super(AttributeFunctionJunk, AttributeFunctionJunk).refine_attr_vals(attr_vals, AttributeFunctionJunk.refine, do_defreq=False, do_tokenize=False, do_clean=True)
        
        threshold = 5
        if sparse_value(attr_vals, threshold=threshold):
            return True
        
        if not super(AttributeFunctionJunk, AttributeFunctionJunk).pre_judge(attr_vals,disable_prejudge=True):
            return False

        # print attr_vals

        if not super(AttributeFunctionJunk, AttributeFunctionJunk).valid_counts(attr_vals, AttributeFunctionJunk.valid_junk, threshold=0.4):
            return False
        return True






if __name__ == '__main__':
    # text = ': 34-35 34 B Eyes: Brown Smokes: Yes but not with '
    # text = '2015'
    text = '3 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 3 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 3 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 1 picture --> \" > --> 4 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 4 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 1 picture --> \" > --> 4 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" > 1 picture --> \" > --> 4 pictures --> \" > --> <div style=\"position: relative; width: 100px; height: 100px;margin-top:14px;\"class= \"\" >'
    # print AttributeFunctionJunk.match(text)
    print re_junks.findall(text)
    


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