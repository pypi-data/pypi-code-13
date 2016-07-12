# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-09 14:35:51
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-11 16:07:13

import os
import codecs
import json
from digani.attr_func import IGNORED_ATTRIBUTE_NAMES, ATTRIBUTE_NAMES_JUNK

FILIENAME_RULES_STEP01 = 'step01_rules.json'
FILIENAME_RULES_STEP02 = 'step02_rules.json'
FILIENAME_EXTRACTIONS_STEP01 = 'step01_extractions.jl'
FILIENAME_EXTRACTIONS_STEP02 = 'step02_extractions.jl'


def generate_step02_rules(mapping, step01_rules_path):
    rules = json.load(codecs.open(step01_rules_path, 'r', 'utf-8'))
    new_rules = []
    for rule in rules:
        name = mapping[rule['name']]
        if name.split('-')[0] == ATTRIBUTE_NAMES_JUNK:
            continue
        rule['name'] = name
        new_rules.append(rule)
    return new_rules

def generate_step02_extractions(mapping, step01_extractions_path):
    extractions = []
    with open(step01_extractions_path, 'rb') as file_handler:
        for line in file_handler:
            extraction = json.loads(line)
            keys = extraction.keys()
            # names = {}
            for key in keys:

                if key in IGNORED_ATTRIBUTE_NAMES:
                    continue

                name = mapping[key]
                # names.setdefault(name, 0)
                # names[name] += 1
                if name.split('-')[0] == ATTRIBUTE_NAMES_JUNK:
                    continue
                # if name in extraction:
                #     extraction[name] += ',' + extraction.pop(key)
                # else:
                # '-' + str(names[name])
                extraction[name if name != 'unknown' else key] = extraction.pop(key)

            extractions.append(extraction)
    return extractions


def generate(mapping, output_dir, show_extractions=False):

    step01_rules_path = os.path.join(output_dir, FILIENAME_RULES_STEP01)
    step02_rules_path = os.path.join(output_dir, FILIENAME_RULES_STEP02)

    step01_extractions_path = os.path.join(output_dir, FILIENAME_EXTRACTIONS_STEP01)
    step02_extractions_path = os.path.join(output_dir, FILIENAME_EXTRACTIONS_STEP02)


    # rules
    rules = generate_step02_rules(mapping, step01_rules_path)
    file_handler = open(step02_rules_path, 'wb')
    file_handler.write(json.dumps(rules, indent=2, sort_keys=True))
    file_handler.close()

    if show_extractions:
        extractions = generate_step02_extractions(mapping, step01_extractions_path)
        file_handler = open(step02_extractions_path, 'wb')
        for extraction in extractions:
            file_handler.write(json.dumps(extraction) + '\n')
        file_handler.close()

