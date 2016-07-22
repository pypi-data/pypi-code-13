# -*- coding: utf-8 -*-
import io

from jschema.make._options import Options
from jschema.make._dump_methods import dump_methods
from jschema.make._jinja2_env import jinja2_env


def make_ajv(schema, options):
    opts = Options(options)
    template = jinja2_env.get_template("schema_ajv.j2")

    with io.open(opts.dst_path, "w", encoding="utf-8") as fstream:
        fstream.write(template.render({"schemas": dump_methods(schema)}))
