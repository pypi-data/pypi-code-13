#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import posixpath
import shutil
import faff


class GccCompiler(object):

    def __init__(self, data):
        self._data = dict(data)

        self._root = os.path.abspath(self._data.get("ROOT"))
        self._name = str(self._data.get("NAME", "main"))
        self._build = os.path.join(
            self._root, self._data.get("BUILD", "build")
        )
        self._cflags = tuple(self._data.get("CFLAGS", []))
        sources = tuple(self._data.get("SOURCES", []))
        self._sources = [faff.FileTarget("{ROOT}", *x) for x in sources]
        self._objects = [faff.FileTarget("{BUILD}", *x, ext=".o") for x in sources]

        # TODO: Variable context management.
        faff.Variable("ROOT", self._root)
        faff.Variable("BUILD", self._build)
        CFLAGS = faff.Variable("CFLAGS")
        for cflag in self._cflags:
            CFLAGS += str(cflag)

        @faff.rule([self._objects, self._sources])
        def _compile(target, depends, args):
            faff.Run("gcc -c {CFLAGS} {_D} -o {_T}", self._root)

        self.compile = _compile
        self.compile_target = faff.RuleTarget(self.compile)

        source_list = faff.FileTarget("{BUILD}", "source.list")
        source_list < None
        faff.Variable("SOURCE_LIST", str(source_list))
        with open(str(source_list), "w") as f:
            objects = ["{}/{}.o".format(
                self._data.get("BUILD", "build"),
                posixpath.join(*x)[:-2]) for x in sources
            ]
            f.write("\n".join(objects))
            f.write("\n")

        @faff.rule()
        def _clean(target, depends, args):
            shutil.rmtree(self._build)

        self.clean = _clean
        self.clean_target = faff.RuleTarget(self.clean)


class BinaryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(BinaryGccCompiler, self).__init__(data)

        self._binary = faff.FileTarget(self._build, self._name)

        @faff.rule(self._binary, depends=self.compile_target)
        def _all(target, depends, args):
            faff.Run("gcc -o {_T} @{SOURCE_LIST}", self._root)

        self.all = _all
        self.all_target = faff.RuleTarget(self.all)


class LibraryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(LibraryGccCompiler, self).__init__(data)
