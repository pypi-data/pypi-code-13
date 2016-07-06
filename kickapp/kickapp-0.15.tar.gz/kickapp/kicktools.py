#!/usr/bin/env python

#----------------------------------------------------------------------
def parcefiles(editfiles, kwargs):
    """"""
    for filename in editfiles:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        new_lines = "".join(lines)
        new_lines = new_lines.replace("{{", "#&<<").replace("}}", ">>&#")
        new_lines = new_lines.replace("{", "{{").replace("}", "}}")
        new_lines = new_lines.replace("#&<<", "{").replace(">>&#", "}")
        new_lines = new_lines.format(**kwargs)
        file = open(filename, "w")
        file.write(new_lines)
        file.close()


#----------------------------------------------------------------------
def getname(name):
    """"""
    return name.lower().replace("-", "_").replace(" ", "_")

