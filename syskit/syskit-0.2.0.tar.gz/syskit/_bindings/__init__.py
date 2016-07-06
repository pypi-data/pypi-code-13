# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, division

import importlib
import textwrap

import cffi

import syskit


class Binding(object):
    """Access to the FFI bindings for this platform

    The bindings are stored as class attrbutes :attr:`ffi` and
    :attr:`lib`.
    """
    ffi = None
    lib = None

    def __init__(self):
        self._init()

    @classmethod
    def _init(cls):
        """Build the FFI modules if not yet available"""
        if cls.ffi is None and cls.lib is None:
            cls.ffi, cls.lib = cls._build()

    @classmethod
    def _build(cls):
        # This includes the function defs in both .cdef() and
        # .verify() so that the compiler will complain if we wrote the
        # wrong function def.
        modules = ['syskit._bindings.ffi_{}_process'.format(syskit.platform),
                   'syskit._bindings.ffi_utmpx']
        if syskit.platform == 'aix':
            modules.append('syskit._bindings.ffi_aix_perfstat')
        ffi = cffi.FFI()
        int_typedefs = {}
        structs = []
        macros = []
        functions = []
        verify_preamble = []
        includes = []
        libs = []
        verify_extra = []
        for modname in modules:
            module = importlib.import_module(modname)
            for alias, orig in module.INT_TYPEDEFS.items():
                if alias in int_typedefs and orig != int_typedefs[alias]:
                    raise ValueError(
                        'Conflicting typedefs for {}: {} and {} (last from {})'
                        .format(alias, int_typedefs[alias], orig, modname))
                else:
                    int_typedefs[alias] = orig
            structs.append(module.STRUCTS)
            macros.append(module.MACROS)
            functions.append(module.FUNCTIONS)
            verify_preamble.append(module.VERIFY_PREAMLE)
            includes.append(module.INCLUDES)
            libs.extend(module.LIBS)
            verify_extra.append(module.VERIFY_EXTRA)
        typedefs, check_func, retval_map = \
            cls._build_int_typedefs(int_typedefs)
        ffi.cdef(typedefs)
        ffi.cdef('\n'.join(structs))
        ffi.cdef('\n'.join(macros))
        ffi.cdef('\n'.join(functions))
        ffi.cdef('int check_types(void);')
        lib = ffi.verify(
            source='\n'.join(['\n'.join(verify_preamble),
                              '\n'.join(includes),
                              '\n'.join(functions),
                              check_func,
                              '\n'.join(verify_extra)]),
            ext_package='syskit',
            libraries=[str(l) for l in libs],
        )
        ret = lib.check_types()
        if ret < 0:
            which = 'size' if ret > -100 else 'signedness'
            if ret <= -100:
                ret = ret // 100
            raise Exception('check_types() failed {} for type: {}'
                            .format(which, retval_map[ret]))
        return ffi, lib

    @staticmethod
    def _build_int_typedefs(defs_map):
        """Build the integer typedefs and check function from a dict

        E.g. ``typedef unsigned short ushort_t;`` would have a key of
        ``ushort_t`` and a value of ``unsigned short``.  The check
        function will then check the size and signedness.

        This builds something like this for the cdef step::

           typedef unsigned short ushort_t;

        And the following for the verify step::

           struct checker {
               ushort_t aa;
           };

           int
           check_types(void)
           {
               struct checker checker;

               memset(&checker, 0xff, sizeof(struct checker));
               if (sizeof(ushort_t) != sizeof(unsiged short))
                   return -1;
               if (checker.aa) < 0)
                   return -100;
           }

        The mapping between the return codes and the type is returned
        as third argument.

        Returns ``(tyepdefs, check_func_source, retval_map)``.
        """
        defs = []
        signedness_fields = []
        checks = []
        retval_map = {}
        i = 0
        struct_name = 'aa'

        def nextname():
            a, b = struct_name
            if ord(b) < ord('z'):
                b = chr(ord(b) + 1)
            elif ord(a) < ord('z'):
                a = chr(ord(a) + 1)
                b = 'a'
            return a + b

        for alias, orig in defs_map.items():
            i -= 1
            retval_map[i] = alias
            typedef = 'typedef {orig} {alias};'
            struct_field = '{alias} {struct_name};'
            check = ['if (sizeof({alias}) != sizeof({orig}))',
                     '    return {i};',
                     'if (checker.{struct_name} {cmp} 0)',
                     '    return {i}00;']
            cmp = '<' if 'unsigned' in orig or 'uint' in orig else '>'
            fields = locals()
            defs.append(typedef.format(**fields))
            signedness_fields.append(struct_field.format(**fields))
            checks.extend(c.format(**fields) for c in check)
            struct_name = nextname()
        typedefs = '\n'.join(defs)
        check_func = textwrap.dedent("""
        struct checker {{
            {signedness_fields}
        }};

        int
        check_types(void)
        {{
            struct checker checker;

            memset(&checker, 0xff, sizeof(struct checker));
            {checks}
            return 0;
        }}
        """).format(signedness_fields='\n    '.join(signedness_fields),
                    checks='\n    '.join(checks))
        return typedefs, check_func, retval_map
