from __future__ import absolute_import
from pycparserext import ext_c_parser


class Parser(ext_c_parser.OpenCLCParser):
	# Use our patched lexer instead. See lexer.py for details.
	from oclminifier.lexer import OpenCLCLexer as lexer_class

# Override pycparserext's implementation because it fails to parse pointers in
# type declarations. Once again, the original implementation works just fine
# for our minification-related usage.
from pycparser import CParser
Parser.p_declarator_2 = CParser.p_declarator_2
