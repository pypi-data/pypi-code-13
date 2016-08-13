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
            self._root, *self._data.get("BUILD", ("build",))
        )
        self._install = self._data.get("INSTALL", ("{ROOT}", "install",))
        self._gcc = str(self._data.get("GCC", "gcc"))
        self._ar = str(self._data.get("AR", "ar"))
        self._cflags = tuple(self._data.get("CFLAGS", []))
        headers = tuple(self._data.get("HEADERS", []))
        self._headers = [faff.api.FileTarget("{ROOT}", *x) for x in headers]
        sources = tuple(self._data.get("SOURCES", []))
        self._sources = [faff.api.FileTarget("{ROOT}", *x) for x in sources]
        self._objects = [faff.api.FileTarget("{BUILD}", *x, ext=".o") for x in sources]

        # TODO: Variable context management.
        faff.api.Variable("ROOT", self._root)
        faff.api.Variable("BUILD", self._build)
        faff.api.Variable("GCC", self._gcc)
        faff.api.Variable("AR", self._ar)
        CFLAGS = faff.api.Variable("CFLAGS")
        for cflag in self._cflags:
            CFLAGS += str(cflag)

        @faff.api.rule([self._objects, self._sources])
        def _compile(target, depends, args):
            faff.api.run("{GCC} -c {CFLAGS} {_D} -o {_T}", self._root)

        self.compile = _compile
        self.compile_target = faff.api.RuleTarget(self.compile)

        src_list = faff.api.FileTarget("{BUILD}", "source.list")
        src_list.out_of_date()

        @faff.api.rule(src_list)
        def _source_list(target, depends, args):
            with open(str(target), "w") as f:
                objects = ["{}/{}.o".format(
                    faff.api.Variable.expand(posixpath.join(*self._data.get("BUILD", ("build",)))),
                    posixpath.join(*x)[:-2]) for x in sources
                ]
                f.write("\n".join(objects))
                f.write("\n")

        self.source_list = _source_list
        self.source_list_target = faff.api.RuleTarget(self.source_list)

        @faff.api.rule()
        def _clean(target, depends, args):
            # TODO: Better error handling.
            try:
                shutil.rmtree(faff.api.Variable.expand("{BUILD}"))
            except:
                pass

        self.clean = _clean
        self.clean_target = faff.api.RuleTarget(self.clean)


class BinaryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(BinaryGccCompiler, self).__init__(data)

        self._binary = faff.api.FileTarget("{BUILD}", self._name)

        @faff.api.rule([self._binary, [self.compile_target, self.source_list_target]])
        def _all(target, depends, args):
            faff.api.run("{GCC} -o {_T} @{BUILD}/source.list", self._root)

        self.all = _all
        self.all_target = faff.api.RuleTarget(self.all)


class LibraryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(LibraryGccCompiler, self).__init__(data)

        self._library = faff.api.FileTarget("{BUILD}", self._name)

        @faff.api.rule([self._library, [self.compile_target, self.source_list_target]])
        def _all(target, depends, args):
            faff.api.run("{AR} rs {_T} @{BUILD}/source.list", self._root)

        self.all = _all
        self.all_target = faff.api.RuleTarget(self.all)

        @faff.api.rule(self.all_target)
        def _install(target, depends, args):
            self._library.copy(*self._install)

        self.install = _install
        self.install_target = faff.api.RuleTarget(self.install)
