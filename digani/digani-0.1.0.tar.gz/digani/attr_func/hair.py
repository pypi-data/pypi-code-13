# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 18:03:54
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 15:26:12

from digani.res.hair import res_hair_obj
from base import AttributeFunctionBase

class AttributeFunctionHair(AttributeFunctionBase):

    @staticmethod
    def valid_hair(string):
        if not res_hair_obj.match(string):
            return False
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionHair, AttributeFunctionHair).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionHair, AttributeFunctionHair).refine_attr_vals(attr_vals, AttributeFunctionHair.refine)

        if not super(AttributeFunctionHair, AttributeFunctionHair).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionHair, AttributeFunctionHair).valid_counts(attr_vals, AttributeFunctionHair.valid_hair, threshold=0.4):
            return False

        return True