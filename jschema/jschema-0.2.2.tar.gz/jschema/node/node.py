# -*- coding: utf-8 -*-
from jschema.errors import JrsNodeError


class Node(object):

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

    def __init__(self, key, parent, root):
        self._key = key
        self._parent = parent
        self._root = root
        self._childs = []

    @property
    def key(self):
        return self._key

    @property
    def parent(self):
        return self._parent

    @property
    def root(self):
        return self._root

    def path(self, path=[]):
        if self._parent:
            path.append(self._key)
            return self._parent.path(path)
        else:
            return reversed(path)

    @property
    def value(self):
        return self._parent.value[self._key]

    @value.setter
    def value(self, new_value):
        self._parent.value[self._key] = new_value

    def _store_ref(self):
        ref = self.value["$ref"]

        if ref.index("#") == 0:
            self._root.add_ref({
                "node": self,
                "type": "local",
                "ref": {
                    "path": ref[1:],
                    "context": self._root.value,
                    "resolved_ref": ref
                }
            })
        else:
            schemaId, path = ref.split("#")
            if schemaId not in self._root._schemas:
                raise JrsNodeError(JrsNodeError.make_message(u"Schema '{}' not exists".format(schemaId), self))
            self._root.add_ref({
                "node": self,
                "type": "global",
                "ref": {
                    "id": schemaId,
                    "path": path,
                    "context": self._root._schemas[schemaId],
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
                Node(key, parent=self, root=self._root)
                for key in self.value
            ]
        elif is_list:
            self._childs = [
                Node(index, parent=self, root=self._root)
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
                        raise JrsNodeError(JrsNodeError.make_message(u"Can't resolve ref path", node))

            node.value = value
