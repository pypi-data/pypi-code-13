from __future__ import absolute_import
from pycparserext import ext_c_lexer


class OpenCLCLexer(ext_c_lexer.OpenCLCLexer):
	pass

# Override pycparserext's implementation because it fails to parse
# some pragmas like #pragma unroll. The original implementation works
# just fine for our minification-related usage.
from pycparser.c_lexer import CLexer
OpenCLCLexer.t_PPHASH = CLexer.t_PPHASH
