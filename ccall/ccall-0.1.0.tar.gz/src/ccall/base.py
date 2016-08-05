import functools
import os

import cffi
import pycparser

from ccall.safe import safe_input, safe_output


class CFile:
    """
    Interface to a C source file.
    """

    def __init__(self, path):
        self.path = path
        self.basename = os.path.splitext(self.path)[0]
        self.soname = '_' + self.basename + '.so'
        self.definitions = []

    def extract_definitions(self):
        """
        Extract all function and type definitions from the given source file.
        """

        ast = self._get_ast()
        for _, node in ast.children():
            if isinstance(node, pycparser.c_ast.FuncDef):
                name = get_function_name(node)
                out_type = get_function_restype(node)
                args = get_function_argtypes(node)
                args_data = ', '.join(args)
                cdef = '%s %s(%s);' % (out_type, name, args_data)
                self.definitions.append(cdef)
            else:
                node.show()
                raise NotImplementedError(node)

    def process(self, extract_definitions=True):
        if extract_definitions:
            self.extract_definitions()

        cdef_data = '\n'.join(self.definitions)
        self.compile()
        self.ffi = cffi.FFI()
        self.ffi.cdef(cdef_data)
        self.lib = self.ffi.dlopen(os.path.abspath(self.soname))
        return CLib(self.lib)

    def compile(self):
        os.system('tcc -shared %s -o %s' % (self.path, self.soname))

    def _get_ast(self):
        with open(self.path) as F:
            data = F.read()

        parser = pycparser.CParser()
        data = '\n'.join(
            line
            for line in data.splitlines()
            if not line.strip().startswith('#')
        )
        return parser.parse(data, self.path)

    def cdef(self, decl):
        self.definitions.append(decl)


class CLib:
    """
    A lib object
    """

    def __init__(self, lib):
        self.__lib = lib
        self.__cache = {}

    def __getattr__(self, item):
        try:
            return self.__cache[item]
        except KeyError:
            cfunc = getattr(self.__lib, item)

            @functools.wraps(cfunc)
            def func(*args):
                args = [safe_input(x) for x in args]
                result = cfunc(*args)
                return safe_output(result)

            return func


class LazyCLib:
    """
    Lazy CLib accessor. It only creates and initialize the C lib object when the
    first attribute is requested.
    """

    def __init__(self, path):
        self.__path = path
        self.__lib = None

    def __getattr__(self, item):
        if self.__lib is None:
            self.__lib = CFile(self.__path).process()
        return getattr(self.__lib, item)


def get_function_name(node):
    """
    Return function name from a FuncDecl node.
    """

    return node.decl.name


def get_function_restype(node):
    """
    Return the return type from a FuncDecl node.
    """
    return node.decl.type.type.type.names[0]


def get_function_argtypes(node):
    """
    Return a list of input type declarations from FuncDecl node.
    """

    argtypes = []
    for _, arg in node.decl.type.args.children():
        if isinstance(arg.type, pycparser.c_ast.TypeDecl):
            decl = arg.type.type.names[0]
        elif isinstance(arg.type, pycparser.c_ast.PtrDecl):
            decl = arg.type.type.type.names[0] + '*'
        else:
            arg.show()
            raise NotImplementedError
        argtypes.append(decl)
    return argtypes
