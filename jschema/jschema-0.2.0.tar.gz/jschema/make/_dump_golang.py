# -*- coding: utf-8 -*-
from copy import deepcopy


def dump_golang(schema):
    structs = {}
    for key, sch in schema.schemas.iteritems():
        if sch["type"] == "object":
            structs[key] = sch

    dumped = {}
    for key, node in schema._nodes.iteritems():
        for item in node._refs:
            if item["ref"]["id"] not in structs:
                continue

            struct = structs[item["ref"]["id"]]
            dumped[struct["id"]] = struct

            sch_copy = deepcopy(node.value)
            sch_copy["origin"] = node.value
            ptr = sch_copy
            path = item["node"].path()
            if path:
                for key in path:
                    ptr = ptr[key]

            ptr["pointer_to"] = struct["id"].split(".")[-1]
            dumped[sch_copy["id"]] = sch_copy

    return dumped
