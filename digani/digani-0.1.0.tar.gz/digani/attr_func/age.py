# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-12 10:55:55
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 11:25:21


from base import AttributeFunctionBase
import dateutil.parser as dparser

import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

class AttributeFunctionAge(AttributeFunctionBase):

    @staticmethod
    def valid_age(string):

        def has_only_digits(string):
            try:
                int(string)
            except:
                return False
            return True

        def valid_digit_length(string):
            digits = re_digits.findall(string)
            digits = ''.join(digits)
            if len(digits) != 2:
                return False
            return True

        if not has_only_digits(string):
            return False

        if not valid_digit_length(string):
            return False

        age = int(string)
        if age < 10 or age > 99:
            return False

        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionAge, AttributeFunctionAge).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionAge, AttributeFunctionAge).refine_attr_vals(attr_vals, AttributeFunctionAge.refine)
        
        if not super(AttributeFunctionAge, AttributeFunctionAge).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionAge, AttributeFunctionAge).valid_counts(attr_vals, AttributeFunctionAge.valid_age, threshold=0.4):
            return False

        return True