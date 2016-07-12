# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 15:53:40
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-12 12:49:33


from digani.res.email import res_email_obj
from base import AttributeFunctionBase

class AttributeFunctionEmail(AttributeFunctionBase):

    @staticmethod
    def valid_email(string):
        return res_email_obj.match(string)

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionEmail, AttributeFunctionEmail).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionEmail, AttributeFunctionEmail).refine_attr_vals(attr_vals, AttributeFunctionEmail.refine)

        if not super(AttributeFunctionEmail, AttributeFunctionEmail).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionEmail, AttributeFunctionEmail).valid_counts(attr_vals, AttributeFunctionEmail.valid_email, threshold=0.4):
            return False

        return True