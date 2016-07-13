# -*- coding: utf-8 -*-
import io
import subprocess

import yaml

from node import Node
from errors import JrsSchemaError

from make_json import make_json
from make_js import make_js
from make_docs import make_docs

MAKE_FORMATS = {
    "json": make_json,
    "js": make_js,
    "docs": make_docs
}


class Schema(object):

    def __init__(self, root):
        self._root = root
        self._schemas = {}
        self._nodes = {}

    def load(self):
        res = subprocess.check_output(["find", self._root, "-name", "*.yaml"])
        for fpath in res.split():
            with io.open(fpath, encoding="utf-8") as fstream:
                schema = yaml.load(fstream)
                if "id" not in schema:
                    raise JrsSchemaError("Attribute 'id' not exists: {}".format(fpath))
                self._schemas[schema["id"]] = schema

    def resolve_refs(self):
        Node.set_schemas(self._schemas)
        for key in self._schemas:
            schema_node = Node(key)
            schema_node.find_refs()
            schema_node.replace_refs()
            self._nodes[key] = schema_node

    def clear(self):
        for schema in self._schemas.values():
            Node.clear(schema)

    def make(self, make_format, options):
        MAKE_FORMATS[make_format](self._schemas, options)
