# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 18:03:23
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-14 18:54:25

from base import AttributeFunctionBase
from digani.res.zipcode import res_zipcode_obj

import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

class AttributeFunctionZipCode(AttributeFunctionBase):

    @staticmethod
    def valid_zip(string):
        def has_only_digits(string):
            try:
                int(string)
            except:
                return False
            return True

        def valid_digit_length(string):
            digits = re_digits.findall(string)
            digits = ''.join(digits)
            if len(digits) != 6:    # 3-6 for US zip
                return False
            return True
        if not string or ''.join(string.split()) == '':
            return False
        if not has_only_digits(string):
            return False

        if not valid_digit_length(string):
            return False

        if not res_zipcode_obj.match(string):
            return False

        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionZipCode, AttributeFunctionZipCode).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionZipCode, AttributeFunctionZipCode).refine_attr_vals(attr_vals, AttributeFunctionZipCode.refine)
        
        if not super(AttributeFunctionZipCode, AttributeFunctionZipCode).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionZipCode, AttributeFunctionZipCode).valid_counts(attr_vals, AttributeFunctionZipCode.valid_zip, threshold=0.4):
            return False

        return True
