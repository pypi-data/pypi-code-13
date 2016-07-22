# -*- coding: utf-8 -*-
import os

from jschema.errors import JrsMakeError
from jschema.make._options import Options
from jschema.make._dump_golang import dump_golang
from jschema.make._jinja2_env import jinja2_env


def make_golang(schema, options):
    opts = Options(options)

    struct_j2 = jinja2_env.get_template("struct_golang.j2")

    schemas = dump_golang(schema)
    for schema_id, schema in schemas.iteritems():
        split = schema_id.split(".")
        if len(split) == 1:
            ns = opts.ns
            name = split[0]
            dst_dir = opts.dst_dir
        elif len(split) == 2:
            ns, name = split
            dst_dir = os.path.join(opts.dst_dir, ns)
        else:
            raise JrsMakeError("Expect zero or one dot in schema id")

        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

        with open(os.path.join(dst_dir, name + ".go"), "w") as fstream:
            fstream.write(struct_j2.render({
                "ns": ns,
                "name": name,
                "schema": schema
            }))
