# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 13:48:43
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-14 18:54:05

from digani.res.person import res_person_obj
from base import AttributeFunctionBase

class AttributeFunctionPerson(AttributeFunctionBase):

    @staticmethod
    def valid_person(string):
        def has_multiple_person(string):
            extractions = string.split()
            names = {}
            for extraction in extractions:
                if res_person_obj.match(extraction):
                    names.setdefault(extraction, 0)
                    names[extraction] += 1

            if len(names) < 1:
                return False
            return True
        if not string or ''.join(string.split()) == '':
            return False
        if not has_multiple_person(string):
            return False
        if not res_person_obj.match(string):
            return False
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):
        # freq_dict = super(AttributeFunctionPerson, AttributeFunctionPerson).frequent_count(attr_vals)

        attr_vals = super(AttributeFunctionPerson, AttributeFunctionPerson).refine_attr_vals(attr_vals, AttributeFunctionPerson.refine)

        if not super(AttributeFunctionPerson, AttributeFunctionPerson).pre_judge(attr_vals):
            return False

        if not super(AttributeFunctionPerson, AttributeFunctionPerson).valid_counts(attr_vals, AttributeFunctionPerson.valid_person, threshold=0.4):
            return False

        return True
  

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
    obj = AttributeFunctionPerson(attr_vals)
    print obj.attr_vals

"""
def attr_func_person(attr_vals):

    count = 0
    size = len(attr_vals)
    for value in attr_vals:
        if not value or value == '':
            continue

        if person.match(value):
            # print value
            count += 1

    if count == 0:
        return False
    # print count, size
    if float(count) / size < 0.4:
        return False
    return True
"""