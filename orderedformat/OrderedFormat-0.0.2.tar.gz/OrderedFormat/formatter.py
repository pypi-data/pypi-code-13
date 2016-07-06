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

def parse_string_to_dict(string_data, load_type=None):
    if not isinstance(string_data, str):
        raise ValueError("Input Data is not 'String'")
    if not load_type:
        raise ValueError("Not found data type. You must choose type 'yaml' or 'json'")

    json_flag = re.match("\.json|json", load_type)
    yaml_flag = re.match("yml|\.yml|yaml|\.yaml", load_type)

    if yaml_flag:
        return yaml.load(string_data)
    if json_flag:
        return json.loads(string_data)

def load_dict_val(filename):
    ext = os.path.splitext(filename)[1]
    with open(filename, 'r') as stream:
        return parse_string_to_dict(stream.read(), ext)

def load_ordered_keys(filename, raw_txt=None,  load_type=None):

    if raw_txt and filename:
        return -1

    if filename:
        if not os.path.exists(filename):
            raise IOError("Not found '{filename}'".format(filename=filename))
        if not load_type:
            load_type = os.path.splitext(filename)[1]

    if not load_type:
        raise ValueError("You must set value for 'ext' field!")

    json_flag = re.match("\.json|json", load_type)
    yaml_flag = re.match("yml|\.yml|yaml|\.yaml", load_type)

    if isinstance(raw_txt, str):
        if json_flag:
            return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(raw_txt)
        if  yaml_flag:
            return yaml.load(raw_txt, Loader=yamlordereddictloader.Loader)

    if json_flag:
        with open(filename) as stream:
            return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(stream.read())
    if yaml_flag:
        return yaml.load(open(filename), Loader=yamlordereddictloader.Loader)


def kflatten(dict_value, ordered_keys, load_type=None):
    _local_dict_value = dict_value
    if isinstance(dict_value, str):
        _local_dict_value = parse_string_to_dict(dict_value, load_type=load_type)

    ordered_and_flatten_list = []
    def _kflatten(_dict_value, _ordered_keys):
        if isinstance(_ordered_keys, OrderedDict):
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

    _kflatten(_local_dict_value, ordered_keys)

    if iter_depth(ordered_and_flatten_list) > 1:
        return tuple(chain.from_iterable(ordered_and_flatten_list))
    else:
        return tuple(ordered_and_flatten_list)


if __name__ == '__main__':
    ordered_keys = load_ordered_keys("../tests/src/test_keys.yml")
    dict_data = load_dict_val("../tests/src/test_data.yml")

    print(kflatten(dict_data, ordered_keys))

    yml_data = """
    human:
      name: John
      age: 22
    """

    key_data = """
    human:
    - name
    - age
    - name
    """

    raw_keys = load_ordered_keys(None, raw_txt=key_data, load_type="yaml")
    kflatten(yml_data, raw_keys, load_type="yaml")