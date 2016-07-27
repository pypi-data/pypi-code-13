# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-11 18:03:13
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-18 21:55:57

import re
from digani.res.city import res_city_obj
from digani.res.state import res_state_obj
from digani.res.country import res_country_obj
from base import AttributeFunctionBase
from digani.common import gram_helper
# print res_state_obj.res_trie_obj.values()

re_location_split = re.compile(r'[\s,]')

class AttributeFunctionLocation(AttributeFunctionBase):

    @staticmethod
    def location_dicts(string):

        def load_dicts(pot, country_dict, state_dict, city_dict):
            for extraction in pot:
                if res_country_obj.match(extraction):
                    country_dict.setdefault(extraction, 0)
                    country_dict[extraction] += 1
                elif res_state_obj.match(extraction):
                    state_dict.setdefault(extraction, 0)
                    state_dict[extraction] += 1
                elif res_city_obj.match(extraction):
                    city_dict.setdefault(extraction, 0)
                    city_dict[extraction] += 1
                else:
                    # leave blank
                    continue
            return country_dict, state_dict, city_dict


        ht = {}

        # pot = string.split()    # []
        pot = []
        pot += gram_helper.generate_strngram(string, 2)
        pot += gram_helper.generate_strngram(string, 3)

        country_dict = {}
        state_dict = {}
        city_dict = {}

        country_dict, state_dict, city_dict = load_dicts(pot, country_dict, state_dict, city_dict)

        spot = []
        locations = country_dict.keys() + state_dict.keys() + city_dict.keys()
        for sw in string.split():
            flag = False
            for location in locations:
                if sw in location.split():
                    flag = True
                    break
            if not flag:
                spot.append(sw)

        country_dict, state_dict, city_dict = load_dicts(spot, country_dict, state_dict, city_dict)

        return country_dict, state_dict, city_dict

    @staticmethod
    def contain_location(string):
        country_dict, state_dict, city_dict = AttributeFunctionLocation.location_dicts(string)
        if (len(country_dict) > 0) or (len(state_dict) > 0) or (len(city_dict) > 0):
            return True
        return False

    @staticmethod
    def multiple_locations(string):
        country_dict, state_dict, city_dict = AttributeFunctionLocation.location_dicts(string)
        
        threshold = 1
        if (len(country_dict) > threshold) or (len(state_dict) > threshold) or (len(city_dict) > threshold):
            return True
        return False

    @staticmethod
    def valid_locations(string):
        country_dict, state_dict, city_dict = AttributeFunctionLocation.location_dicts(string)
        threshold = 1
        if (len(country_dict) > threshold) or (len(state_dict) > threshold) or (len(city_dict) > threshold):
            return False
        
        # print '#'*6
        # print string
        # print country_dict
        # print state_dict
        # print city_dict
        # print '#'*6

        if (len(country_dict) == 1) or (len(state_dict) == 1) or (len(city_dict) == 1):
            return True
        return False

    @staticmethod
    def valid_location(string):
        def is_valid(string):
            if not (res_city_obj.match(string) or res_state_obj.match(string) or res_country_obj.match(string)):
                return False
            return True

        if not string or ''.join(string.split()) == '':
            return False

        if len(string.split(' ')) > 6:
            # for mulple cities inside a cell
            return False

        string = ' '.join(re_location_split.split(string)).strip()
        if not AttributeFunctionLocation.valid_locations(string):
            return False

        # if not is_valid(string):
        #     return False


        # tokens = string.split(',')
        # if len(tokens) == 2:
        #     for token in tokens:
        #         if not is_valid(token.strip()):
        #             return False
        # elif len(tokens) > 2:
        #     return False
        # else:
        #     return is_valid(string)
        return True

    @staticmethod
    def refine(attr_vals):
        # specific refine function here
        return attr_vals

    @staticmethod
    def match(attr_vals):

        # freq_dict = super(AttributeFunctionLocation, AttributeFunctionLocation).frequent_count(attr_vals)


        # in auburn, alabama
        # auburn alabama los angeles
        # auburn alabama arlington
        # auburn alabama new york

        attr_vals = super(AttributeFunctionLocation, AttributeFunctionLocation).refine_attr_vals(attr_vals, AttributeFunctionLocation.refine, do_defreq=False)
        
        if len([_ for _ in attr_vals if AttributeFunctionLocation.multiple_locations(_)]) / float(len(attr_vals)) > .6:
            return False

        attr_vals = super(AttributeFunctionLocation, AttributeFunctionLocation).refine_attr_vals(attr_vals, AttributeFunctionLocation.refine, do_defreq=True)
        # print attr_vals
        if not super(AttributeFunctionLocation, AttributeFunctionLocation).pre_judge(attr_vals):
            return False
        
        if not super(AttributeFunctionLocation, AttributeFunctionLocation).valid_counts(attr_vals, AttributeFunctionLocation.valid_location, threshold=0.6):
            return False

        return True

"""

(super(AttributeFunctionLocation, AttributeFunctionLocation).valid_counts(attr_vals, res_city_obj.match, threshold=0.4) or \
super(AttributeFunctionLocation, AttributeFunctionLocation).valid_counts(attr_vals, res_state_obj.match, threshold=0.4) or \
super(AttributeFunctionLocation, AttributeFunctionLocation).valid_counts(attr_vals, res_country_obj.match, threshold=0.4) \
):
"""