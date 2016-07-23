#! /usr/bin/env python

# TODO

from pyglsl_parser.parser import parse
from pyglsl_parser.enums import ShaderType

path = '/home/nicholasbishop/bel/shaders/library.glsl'
#path = '/home/nicholasbishop/bel/demo.py'
with open(path) as rfile:
    source = rfile.read()

# TODO: upstream bug: if first character encountered is invalid, e.g. '#', it doesn't catch it as an error but as an EOF

kind = ShaderType.Vertex
ast = parse(source, path, kind)
print(ast.kind)
print(ast.types)
print(ast.global_variables)
print(ast.functions)
