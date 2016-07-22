# -*- coding: utf-8 -*-
import os
from json import dumps as json_dumps

from jinja2 import Environment, FileSystemLoader

jinja2_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.with_"]
)

types_golang = {
    "boolean": "bool",
    "integer": "int",
    "number": "float64"
}


def golang_type(type_name, items):
    if type_name == "array":
        array_type = items["type"]
        if array_type in types_golang:
            array_type = types_golang[array_type]
        result = "[]" + array_type
    else:
        result = type_name
        if type_name in types_golang:
            result = types_golang[type_name]
    return result

jinja2_env.filters["type"] = lambda value, expected: type(value) == expected
jinja2_env.filters["intersectionAny"] = lambda arr1, arr2: len(set(arr1).intersection(arr2)) > 0
jinja2_env.filters["intersectionValue"] = lambda arr1, arr2: list(set(arr1).intersection(arr2))[0]
jinja2_env.filters["jsonDumps"] = lambda value: json_dumps(value, indent=2, separators=(",", ": "))
jinja2_env.filters["upperCamelCase"] = lambda value: "".join([word.capitalize() for word in value.split("_")])
jinja2_env.filters["golangType"] = golang_type
