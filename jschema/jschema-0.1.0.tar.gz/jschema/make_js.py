import os
import io
import json

from jinja2 import Environment, FileSystemLoader
from errors import JrsMakeError


def make_js(schemas, options):
    if "dst" not in options:
        raise JrsMakeError("options['dst'] not exists")

    dst = options["dst"]
    if not os.path.exists(os.path.dirname(dst)):
        raise JrsMakeError("Path not exists '{}'".format(os.path.dirname(dst)))

    j2 = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
        trim_blocks=True,
        lstrip_blocks=True
    )

    with io.open(dst, "w", encoding="utf-8") as fstream:
        fstream.write(j2.get_template("export_js.j2").render({
            "schemas": dict([
                (
                    key, unicode(
                        json.dumps(sch, indent=2, separators=(',', ': '))
                    )
                )
                for key, sch in schemas.iteritems()
            ])
        }))
