import os
import six
import re
import json
import yaml
import yamlordereddictloader
from itertools import chain
from collections import OrderedDict

def iter_depth(arr):
    if isinstance(arr, dict) and arr:
        return 1 + max(iter_depth(arr[a]) for a in arr)
    if isinstance(arr, list) and arr:
        return 1 + max(iter_depth(a) for a in arr)
    if isinstance(arr, tuple) and arr:
        return iter_depth(list(arr))
    return 0


def load_dict_val(name):
    ext = os.path.splitext(name)[1]
    with open(name, 'r') as stream:
        return parse_string_to_dict(stream.read(), ext)


def parse_string_to_dict(string_data, type=None):
    if not isinstance(string_data, str):
        raise ValueError("Input Data is not 'String'")
    if not type:
        raise ValueError("Not found data type. You must choose type 'yaml' or 'json'")

    json_flag = re.match("\.json|json", type)
    yaml_flag = re.match("yml|\.yml|yaml|\.yaml", type)

    if yaml_flag:
        return yaml.load(string_data)
    if json_flag:
        return json.loads(string_data)


def load_ordered_keys(key_data, filename=None, ext=None):

    if key_data and filename:
        return -1

    if filename:
        if not os.path.exists(filename):
            raise IOError("Not found '{filename}'".format(filename=filename))
        if not ext:
            ext = os.path.splitext(filename)[1]

    if not ext:
        raise ValueError("You must set value for 'ext' field!")

    json_flag = re.match("\.json|json", ext)
    yaml_flag = re.match("yml|\.yml|yaml|\.yaml", ext)

    if isinstance(key_data, str):
        if json_flag:
            return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(key_data)
        if  yaml_flag:
            return yaml.load(key_data, Loader=yamlordereddictloader.Loader)

    if json_flag:
        with open(filename) as stream:
            return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(stream.read())
    if yaml_flag:
        return yaml.load(open(filename), Loader=yamlordereddictloader.Loader)


def kflatten(dict_value, ordered_keys, type=None):
    if isinstance(dict_value, str):
        dict_value = parse_string_to_dict(dict_value, type=type)

    ordered_and_flatten_list = []
    def _kflatten(_dict_value, _ordered_keys):
        if isinstance(_ordered_keys, OrderedDict):
            # Todo Python 2, 3
            if six.PY2:
                map(lambda sub_key: _kflatten(_dict_value[sub_key], _ordered_keys[sub_key]), _ordered_keys)
            else:
                list(map(lambda sub_key: _kflatten(_dict_value[sub_key], _ordered_keys[sub_key]), _ordered_keys))
        if isinstance(_ordered_keys, list):
            for key in _ordered_keys:
                if isinstance(key, OrderedDict):
                    map(lambda sub_key: _kflatten(_dict_value[sub_key], key[sub_key]), key)
                if isinstance(key, str):
                    ordered_and_flatten_list.append(_dict_value[key])

    _kflatten(dict_value, ordered_keys)

    if iter_depth(ordered_and_flatten_list) > 1:
        return tuple(chain.from_iterable(ordered_and_flatten_list))
    else:
        return tuple(ordered_and_flatten_list)


if __name__ == '__main__':
    ordered_keys = load_ordered_keys(None, filename="../tests/src/test_keys.yml")
    dict_data = load_dict_val("../tests/src/test_data.yml")

    print(kflatten(dict_data, ordered_keys))
