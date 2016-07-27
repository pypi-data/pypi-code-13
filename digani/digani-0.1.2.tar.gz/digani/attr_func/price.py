
# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 18:03:54
# @Date:   2016-07-27 11:56:42
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-27 14:02:14

from base import AttributeFunctionBase
from digpe import DIGPE
import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

pe = DIGPE()

class AttributeFunctionPrice(AttributeFunctionBase):

    @staticmethod
    def valid_price(string):
        def has_only_digits(string):
            try:
                int(string)
            except:
                return False
            return True

        def valid_price_range(price):
            if price >= 30: # and price <= 200:
                return True
            return False

        if not re_digits.findall(string):
            return False

        if len(re_alphabet.findall(string)) >= 5:
            return False

        if has_only_digits(string):
            price = int(string)
            if not valid_price_range(price):
                return False

        extractions = pe.extract(string)
        print extractions
        if extractions:
            for extraction in extractions['price']:
                # extraction = extraction['price']
                # print 'prict_ext:', extraction
                if not valid_price_range(extraction):
                    return False
        else:
            return False
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionPrice, AttributeFunctionPrice).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionPrice, AttributeFunctionPrice).refine_attr_vals(attr_vals, AttributeFunctionPrice.refine)
        # print attr_vals
        if not super(AttributeFunctionPrice, AttributeFunctionPrice).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionPrice, AttributeFunctionPrice).valid_counts(attr_vals, AttributeFunctionPrice.valid_price, threshold=0.4):
            return False

        return True

