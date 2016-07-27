#!/usr/bin/env python3


def linebyline (d):

    rep = "\n    {\n"

    for key in d:
        rep += "\t{0}: {1}\n".format(key, d[key])

    return rep + "    }\n"
