# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 15:52:57
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 11:25:49


from base import AttributeFunctionBase
import dateutil.parser as dparser

import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

class AttributeFunctionDate(AttributeFunctionBase):    

    @staticmethod
    def valid_date(string):

        def has_only_digits(string):
            try:
                int(string)
            except:
                return False
            return True

        def valid_digit_length(string):
            digits = re_digits.findall(string)
            digits = ''.join(digits)
            if 4 >= len(digits) or len(digits) > 8: #20160712
                return False
            return True

        def has_date(string):
            try:
                date = dparser.parse(string) # fuzzy=True
            except:
                return False
            else:
                return True

        if has_only_digits(string):
            if not valid_digit_length(string):
                return False

        if not has_date(string):
            return False


    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionDate, AttributeFunctionDate).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionDate, AttributeFunctionDate).refine_attr_vals(attr_vals, AttributeFunctionDate.refine)
        
        if not super(AttributeFunctionDate, AttributeFunctionDate).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionDate, AttributeFunctionDate).valid_counts(attr_vals, AttributeFunctionDate.valid_date, threshold=0.4):
            return False

        return True




"""
import re
re_alphabet = re.compile(r'[a-zA-Z]+')
re_digits = re.compile(r'[0-9]+')

irrelations = [
    r'\d{1,3}',
]
reg_irrelation = r'|'.join(irrelations)
re_irrelation = re.compile(reg_irrelation)



def attr_func_date(attr_vals):
    count = 0
    for value in attr_vals:
        if not value or value == '':
            continue

        if re_irrelation.match(value):
            return False

        if not has_date(value):
            return False

        count += 1

    if count == 0:
        return False

    return True



if __name__ == '__main__':
    text = '201 s'
    if re_irrelation.match(text):
        print 'True'
    else:
        print 'False
"""