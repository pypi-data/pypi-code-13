import os
from copy import deepcopy
from collections import defaultdict

from jschema.errors import JrsMakeError
from jschema.make._filters import upper_camel_case_filter
from jschema.make._jinja2_env import jinja2_env


class GolangMaker(object):

    def __init__(self, schema, opts):
        self._schema = schema
        self._opts = opts
        self._deps = defaultdict(list)
        self._structs = {}

    def _split_id(self, value):
        split = value.split(".")
        if len(split) == 1:
            ns = self._opts.ns
            name = split[0]
        elif len(split) == 2:
            ns = split[0]
            name = split[1]
        else:
            raise JrsMakeError("Expect zero or one dot in schema id")

        return ns, name, len(split)

    def _append_dep(self, sch_id, ns):
        if ns not in self._deps:
            self._deps[sch_id].append(ns)

    def find_structs(self):
        for key, node in self._schema.nodes.iteritems():
            for item in node.refs:
                if item["context"]["type"] not in ["object", "method"]:
                    continue

                # expect only:
                #  * object#
                #  * method#params
                #  * method#result
                if item["path"] not in ["", "params", "result"]:
                    continue

                if item["context"]["id"] not in self._structs:
                    self._structs[item["context"]["id"]] = deepcopy(item["context"])
                    self._structs[item["context"]["id"]]["origin"] = item["context"]

                ref_schema = self._structs[item["context"]["id"]]

                if node.key not in self._structs:
                    self._structs[node.key] = deepcopy(node.value)
                    self._structs[node.key]["origin"] = node.value

                target_schema = self._structs[node.key]
                ptr = target_schema
                if item["node"].path:
                    for key in item["node"].path:
                        ptr = ptr[key]

                suffix = ""
                if item["path"] in ["params", "result"]:
                    suffix = item["path"].capitalize()

                ns, name, split_length = self._split_id(ref_schema["id"])
                pointer = upper_camel_case_filter(name) + suffix
                if ns != node.ns:
                    pointer = ns + "." + pointer
                    self._append_dep(target_schema["id"], ns)

                ptr["pointer"] = pointer

        # save all methods
        for key, sch in self._schema.schemas.iteritems():
            if sch["type"] == "method" and sch["id"] not in self._structs:
                sch_copy = deepcopy(sch)
                sch_copy["origin"] = sch
                self._structs[sch["id"]] = sch_copy

    def save_structs(self):
        struct_j2 = jinja2_env.get_template("struct_golang.j2")

        for sch_id, sch in self._structs.iteritems():
            ns, name, split_length = self._split_id(sch_id)
            dst_dir = self._opts.dst_dir
            if split_length == 2:
                dst_dir = os.path.join(dst_dir, ns)

            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            with open(os.path.join(dst_dir, name + ".go"), "w") as fstream:
                fstream.write(struct_j2.render({
                    "deps": self._deps[sch_id],
                    "ns": ns,
                    "name": name,
                    "schema": sch,
                    "import_root": self._opts.import_root
                }))
