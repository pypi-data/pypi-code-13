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


def resolve_ref(node, local):
    for child in node.childs():
        if (local and child.is_local_ref()) or (not local and child.is_global_ref()):
            child.replace_ref()
        elif child.is_dict or child.is_list:
            resolve_ref(child, local)


def resolve_schemas(schemas):
    Node.set_schemas(schemas)
    for sch in schemas.itervalues():
        if "$ref" in unicode(sch):
            resolve_ref(Node(
                key=None,
                node=sch,
                parent=None,
                root=sch
            ), local=True)

    iteration = 0
    while True:
        noRef = True
        for sch in schemas.itervalues():
            if "$ref" in unicode(sch):
                resolve_ref(Node(
                    key=None,
                    node=sch,
                    parent=None,
                    root=sch
                ), local=False)
                noRef = False
        iteration += 1

        if noRef:
            break

        if iteration == 10:
            raise Exception("Have unresolved local refs on one iteration")

    return schemas


def _clear_recursive(node):
    if type(node) == dict:
        if "title" in node:
            del node["title"]
        if "description" in node:
            del node["description"]
        if "resolved_$ref" in node:
            del node["resolved_$ref"]

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
