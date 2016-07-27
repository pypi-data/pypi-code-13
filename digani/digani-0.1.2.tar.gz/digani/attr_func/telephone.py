# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 14:30:09
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-27 12:13:52

import re
from base import AttributeFunctionBase
from pnmatcher import PhoneNumberMatcher
from location import AttributeFunctionLocation
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')
matcher = PhoneNumberMatcher()

class AttributeFunctionTelephone(AttributeFunctionBase):

    @staticmethod
    def valid_telephone(string):

        def valid_digit_length(string):
            digits = re_digits.findall(string)

            if not digits:
                return False
            digits = ''.join(digits)
            if not (len(digits) >= 6 and len(digits) <= 13):
                return False
            return True

        def has_alphabet(string):
            if re_alphabet.findall(string):
                return True
            else:
                return False

        def has_only_digits(string):
            try:
                int(string)
            except:
                return False
            return True

        def is_valid(string, contain_alphabet=False):
            if contain_alphabet:
                ab = re_alphabet.findall(string)
                if len(ab) > 2:
                    return False
            else:
                if has_alphabet(string):
                    return False
            if not valid_digit_length(string):
                return False

            extraction = matcher.match(string, source_type='text')
            if not extraction:
                return False
            if len(extraction) > 1:
                return False
            return True

        def has_multiple_telephones(string):
            ht = {}
            for extraction in string.split(): 
                if is_valid(extraction, contain_alphabet=False):
                    ht.setdefault(extraction, 0)
                    ht[extraction] += 1
            return ht

        if not string or ''.join(string.split()) == '':
            return False
        telephones = has_multiple_telephones(string)
        # print telephones
        if len(telephones) > 1:
            return False
        elif len(telephones) < 1:
            # print "len(telephones) < 1"
            if not is_valid(string, contain_alphabet=True):
                return False
        # else:
        digits = ''.join(re_digits.findall(string))
        if len(digits) > 12:
            return False
        if AttributeFunctionLocation.contain_location(string):
            return False
        if not is_valid(string, contain_alphabet=True):
            return False
        # if len(re_alphabet.findall(string)) > 2:
        #     return False

        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def prejudge(attr_vals):
        for value in attr_vals:
            findings = re_alphabet.findall(value)
            # if len(''.join(findings)) > 10:
            if len(findings) > 10:
                return False
        return True

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionTelephone, AttributeFunctionTelephone).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionTelephone, AttributeFunctionTelephone).refine_attr_vals(attr_vals, AttributeFunctionTelephone.refine)
        # print attr_vals
        if not super(AttributeFunctionTelephone, AttributeFunctionTelephone).pre_judge(attr_vals, custom_judge=AttributeFunctionTelephone.prejudge):
            return False

        if not super(AttributeFunctionTelephone, AttributeFunctionTelephone).valid_counts(attr_vals, AttributeFunctionTelephone.valid_telephone, threshold=0.8):
            return False

        return True



if __name__ == '__main__':
    attr_vals = [
        '248-291-4424',
        '248-291-4422',        
    ]
    print AttributeFunctionTelephone.match(attr_vals)

"""
import re

from pnmatcher import PhoneNumberMatcher
matcher = PhoneNumberMatcher()

re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

def attr_func_telephone(attr_vals):

    
    count = 0
    size = len(attr_vals)
    
    for value in attr_vals:
        if not value or value == '':
            continue

        if re_alphabet.findall(value):
            return False

        digits = re_digits.findall(value)
        if not digits:
            return False

        digits = ''.join(digits)
        if len(digits) < 6 or len(digits) > 13:
            return False

        extraction = matcher.match(value, source_type='text')
        # print value, extraction
        if not extraction:
            return False

        count += 1

    if count == 0:
        return False
    if float(count) / size < 0.8:
        return False
    return True
"""