# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-12 16:19:59
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 16:20:42


from digani.res.eye import res_eye_obj
from base import AttributeFunctionBase

class AttributeFunctionEye(AttributeFunctionBase):

    @staticmethod
    def valid_eye(string):
        if not res_eye_obj.match(string):
            return False
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionEye, AttributeFunctionEye).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionEye, AttributeFunctionEye).refine_attr_vals(attr_vals, AttributeFunctionEye.refine)

        if not super(AttributeFunctionEye, AttributeFunctionEye).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionEye, AttributeFunctionEye).valid_counts(attr_vals, AttributeFunctionEye.valid_eye, threshold=0.4):
            return False

        return True