# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-07-08 13:40:38
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-07-11 10:34:10

import os
import json
import codecs

# [Finished in 739.7s]
GEO_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'all_city_dict.json')
# GEO_NAMES_PATH = os.path.join(os.path.dirname(__file__), 'sample.json')


def load(names_path=GEO_NAMES_PATH):
    # names = json.load(codecs.open(names_path, 'r', 'utf-8'))
    with open(names_path, 'rb') as file_handler:
        names = json.load(file_handler)
    return names

geo_names = load()

def load_data(dict_ref, value):
    if isinstance(value, basestring):
        dict_ref.setdefault(value.lower(), 0)
    else:
        for v in value:
            dict_ref.setdefault(v.lower(), 0)

def save_file(names, output):
    with open(output, 'wb') as file_handler:
        file_handler.write(json.dumps(names, indent=2, sort_keys=True))

def generate_geo_city_names():
    city_names = {}
    state_names = {}
    country_names = {}

    for (domain, content) in geo_names.iteritems():
        for (attribute, value) in content.iteritems():

            if attribute == 'name':
                load_data(city_names, value)

            if attribute == 'state':
                load_data(state_names, value)
                
            if attribute == 'country':
                load_data(country_names, value)
                
    save_file(city_names.keys(), os.path.join(os.path.dirname(__file__), 'city_names.json'))
    save_file(state_names.keys(), os.path.join(os.path.dirname(__file__), 'state_names.json'))
    save_file(country_names.keys(), os.path.join(os.path.dirname(__file__), 'country_names.json'))




    
if __name__ == '__main__':
    generate_geo_city_names()
    