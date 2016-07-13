import os
import io
import json

from errors import JrsMakeError


def make_json(schemas, options):
    if "dst" not in options:
        raise JrsMakeError("options['dst'] not exists")
    dst = options["dst"]

    if not os.path.exists(dst):
        raise JrsMakeError("Path not exists '{}'".format(dst))


    for key, sch in schemas.iteritems():
        fpath = "{}/{}.json".format(dst, key)
        with io.open(fpath, "w", encoding="utf-8") as fstream:
            fstream.write(unicode(json.dumps(sch, indent=2, separators=(',', ': '))) + u"\n")
