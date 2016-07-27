# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 18:04:06
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-18 19:02:48




from digani.res.breast import res_breast_obj
from base import AttributeFunctionBase

import re
reg_breast = r'(?:\w+)'
re_breast = re.compile(reg_breast)

class AttributeFunctionBreast(AttributeFunctionBase):

    @staticmethod
    def valid_breast(string):
        extractions = re_breast.findall(string)
        # print extractions
        for extraction in extractions:
            try:
                integer_ext = int(extraction)
                if integer_ext >=28 and integer_ext <= 45:
                    continue
            except Exception as e:
                pass
            if not res_breast_obj.match(extraction):  
                return False
        if len(extractions) < 1 or (len(extractions) == 1 and not res_breast_obj.match(string)):  
            return False
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals


    @staticmethod
    def prejudge(attr_vals):
        return True

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionBreast, AttributeFunctionBreast).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionBreast, AttributeFunctionBreast).refine_attr_vals(attr_vals, AttributeFunctionBreast.refine, do_defreq=False)
        
        if not super(AttributeFunctionBreast, AttributeFunctionBreast).valid_counts(attr_vals, AttributeFunctionBreast.valid_breast, threshold=0.4):
            return False
        # print 'ss'
        # count = 0
        # size = 0
        # for value in attr_vals:
        #     if value and value != '':
        #         size += 1
        #     if res_breast_obj.match(value): 
        #         count += 1
        # if size == 0 or float(count) / size < .4:
        #     return False

        attr_vals = super(AttributeFunctionBreast, AttributeFunctionBreast).refine_attr_vals(attr_vals, AttributeFunctionBreast.refine, do_defreq=True)

        if not super(AttributeFunctionBreast, AttributeFunctionBreast).pre_judge(attr_vals,custom_judge=AttributeFunctionBreast.prejudge):
            return False

        if not super(AttributeFunctionBreast, AttributeFunctionBreast).valid_counts(attr_vals, AttributeFunctionBreast.valid_breast, threshold=0.4):
            return False

        return True