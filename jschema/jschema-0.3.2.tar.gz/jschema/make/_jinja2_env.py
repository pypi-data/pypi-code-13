# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader

from jschema.make._filters import type_filter
from jschema.make._filters import intersection_any_filter
from jschema.make._filters import intersection_value_filter
from jschema.make._filters import json_dumps_filter
from jschema.make._filters import upper_camel_case_filter
from jschema.make._filters import golang_type_filter

jinja2_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.with_"]
)
jinja2_env.filters["type"] = type_filter
jinja2_env.filters["intersectionAny"] = intersection_any_filter
jinja2_env.filters["intersectionValue"] = intersection_value_filter
jinja2_env.filters["jsonDumps"] = json_dumps_filter
jinja2_env.filters["upperCamelCase"] = upper_camel_case_filter
jinja2_env.filters["golangType"] = golang_type_filter
jinja2_env.filters["ljust"] = lambda value, size: value.ljust(size)
