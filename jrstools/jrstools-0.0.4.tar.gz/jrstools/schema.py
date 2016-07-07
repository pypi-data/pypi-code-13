# -*- coding: utf-8 -*-
import io
from copy import deepcopy
import subprocess

import yaml

from node import Node
from error import JrsSchemaError


def load_schemas(root):
    schemas = {}
    res = subprocess.check_output(["find", root, "-name", "*.yaml"])
    for fpath in res.split():
        with io.open(fpath, encoding="utf-8") as fstream:
            s = yaml.load(fstream)
            if "id" not in s:
                raise JrsSchemaError("In root schema id must exists. file: {}".format(fpath))
            schemas[s["id"]] = s
    return schemas


def resolve_ref(node):
    for child in node.childs():
        if child.is_ref:
            child.replace_ref()
        if child.is_dict or child.is_list:
            resolve_ref(child)


def resolve_schemas(schemas):
    Node.set_schemas(schemas)

    import json

    iteration = 0
    while True:
        noRef = True
        for sch in schemas.itervalues():
            if "$ref" in unicode(sch):
                node = Node(
                    key=None,
                    node=sch,
                    parent=None,
                    root=sch
                )
                resolve_ref(node)
                noRef = False
        iteration += 1

        if noRef:
            break

        if iteration > 10:
            raise Exception("Something wrong in ref resolver")

    return schemas


def _clear_recursive(node):
    if type(node) == dict:
        if "title" in node:
            del node["title"]
        if "description" in node:
            del node["description"]
        if "resolved_ref" in node:
            del node["resolved_ref"]

        for value in node.itervalues():
            _clear_recursive(value)
    elif type(node) == list:
        for value in node:
            _clear_recursive(value)


def clear_schemas(schemas):
    schemasCopy = deepcopy(schemas)
    _clear_recursive(schemasCopy)
    return schemasCopy


def split_schemas(schemas):
    pass
