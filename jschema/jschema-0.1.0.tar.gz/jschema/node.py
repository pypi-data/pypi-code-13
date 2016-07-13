# -*- coding: utf-8 -*-
from copy import deepcopy
from errors import JrsNodeError


class Node(object):

    _schemas = {}
    @classmethod
    def set_schemas(cls, schemas):
        cls._schemas = schemas

    @staticmethod
    def clear(schema):
        value_type = type(schema)
        if value_type == dict:
            schema.pop("title", None)
            schema.pop("description", None)

            for value in schema.values():
                Node.clear(value)
        elif value_type == list:
            for value in schema:
                Node.clear(value)

    def __init__(self, key, parent=None, root=None):
        self._key = key
        self._parent = parent or Node._schemas
        self._root = root or self
        self._childs = []
        self._refs = []

    @property
    def parent(self):
        return self._parent

    @property
    def value(self):
        return self._parent[self._key]

    @value.setter
    def value(self, new_value):
        self._parent[self._key] = new_value

    def _store_ref(self):
        ref = self.value["$ref"]

        if ref.index("#") == 0:
            self._root._refs.append({
                "node": self,
                "ref": {
                    "path": ref[1:],
                    "context": self._root.value,
                    "resolved_ref": ref
                }
            })
        else:
            schemaId, path = ref.split("#")
            if not schemaId in self._schemas:
                raise JrsNodeError(u"Schema not exists", self)
            self._root._refs.append({
                "node": self,
                "ref": {
                    "path": path,
                    "context": Node._schemas[schemaId],
                    "resolved_ref": ref
                }
            })

    def find_refs(self):
        value_type = type(self.value)
        is_ref = value_type is dict and "$ref" in self.value
        is_dict = value_type is dict
        is_list = value_type is list

        if is_ref:
            self._store_ref()
        elif is_dict:
            self._childs = [
                Node(key, parent=self.value, root=self._root)
                for key in self.value
            ]
        elif is_list:
            self._childs = [
                Node(index, parent=self.value, root=self._root)
                for index in range(len(self.value))
            ]

        if self._childs:
            for child in self._childs:
                child.find_refs()

    def replace_refs(self):
        for item in self._refs:
            node = item["node"]
            ref = item["ref"]

            value = ref["context"]
            if ref["path"]:
                for key in ref["path"].strip("/").split("/"):
                    if key in value:
                        value = value[key]
                    else:
                        raise JrsNodeError(u"Can't resolve ref path", node)

            node.value = value
