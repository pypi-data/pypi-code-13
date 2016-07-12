# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-07 13:16:06
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-11 16:02:02

import os
import re
import json
import data_loader
from attr_func import *

def load_attribute_values(jsonlines):
    attribute_values_dict = {}
    for jsonline in jsonlines:
        try:
            json_obj = json.loads(jsonline)
        except Exception as e:
            raise Exception(e, 'parse json string error')
        for (k, v) in json_obj.iteritems():
            attribute_values_dict.setdefault(k, [])
            attribute_values_dict[k].append(v)
    return attribute_values_dict


def identify_attribute_name(attr_vals, attr_func_handlers=ATTRIBUTE_NAMES):
    for attr_name in ATTRIBUTE_NAMES_IN_ORDER:
        if attr_func_handlers[attr_name](attr_vals):
            return attr_name
    return None


FILIENAME_MAPPING_STEP02 = 'step02_mapping.json'

def identify(filepath):
    
    mapping = {}

    jsonlines = data_loader.load_jsonlines_from_file(filepath)
    attribute_values_dict = load_attribute_values(jsonlines)

    names = {}
    for (attribute, values) in attribute_values_dict.items():
        if attribute in IGNORED_ATTRIBUTE_NAMES:
            continue

        name = identify_attribute_name(values)
        names.setdefault(name, 0)
        names[name] += 1

        name_no_seperator = '-'
        mapping[attribute] = name + name_no_seperator + str(names[name])

    path = os.path.join('/'.join(filepath.split('/')[:-1]), FILIENAME_MAPPING_STEP02)
    file_handler = open(path, 'wb')
    file_handler.write(json.dumps(mapping, indent=2, sort_keys=True))
    file_handler.close()

    return mapping

if __name__ == '__main__':
    pass

