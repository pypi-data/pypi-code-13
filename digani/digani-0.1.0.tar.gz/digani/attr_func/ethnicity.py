# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 14:10:13
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-11 14:49:39


from base import AttributeFunctionBase

class AttributeFunctionEthnicity(AttributeFunctionBase):

    def __init__(self, attr_vals):
        AttributeFunctionBase.__init__(self, attr_vals)





if __name__ == '__main__':
    attr_vals = [
        'of hello',
        'of world',
        'of work',
        'of yes',
        'of ok',
        'of sjkdflj',
        'foiwejfowi',
    ]
    obj = AttributeFunctionEthnicity(attr_vals)
    print obj.attr_vals