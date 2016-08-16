#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import posixpath
import shutil
from ... import (VariableContext, Variable, option, RuleTarget, FileTarget,
                 rule, dry_run, run)


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
        self._headers = [FileTarget("{ROOT}", *x) for x in headers]
        sources = tuple(self._data.get("SOURCES", []))
        self._sources = [FileTarget("{ROOT}", *x) for x in sources]
        self._objects = [FileTarget("{BUILD}", *x, ext=".o") for x in sources]

        # TODO: Variable context management.
        Variable("ROOT", self._root)
        Variable("BUILD", self._build)
        Variable("GCC", self._gcc)
        Variable("AR", self._ar)
        CFLAGS = Variable("CFLAGS")
        for cflag in self._cflags:
            CFLAGS += str(cflag)

        @rule([self._objects, self._sources])
        def _compile(**kwargs):
            run("{GCC} -c {CFLAGS} {_D} -o {_T}", self._root)

        self.compile = _compile
        self.compile_target = RuleTarget(self.compile)

        src_list = FileTarget("{BUILD}", "source.list")
        src_list.out_of_date()

        @rule(src_list)
        def _source_list(**kwargs):
            with open(str(kwargs.get("target")), "w") as f:
                objects = ["{}/{}.o".format(
                    Variable.expand(posixpath.join(*self._data.get("BUILD", ("build",)))),
                    posixpath.join(*x)[:-2]) for x in sources
                ]
                f.write("\n".join(objects))
                f.write("\n")

        self.source_list = _source_list
        self.source_list_target = RuleTarget(self.source_list)

        @rule()
        def _clean(**kwargs):
            # TODO: Better error handling.
            try:
                shutil.rmtree(Variable.expand("{BUILD}"))
            except:
                pass

        self.clean = _clean
        self.clean_target = RuleTarget(self.clean)


class BinaryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(BinaryGccCompiler, self).__init__(data)

        self._binary = FileTarget("{BUILD}", self._name)

        @rule([self._binary, [self.compile_target, self.source_list_target]])
        def _all(**kwargs):
            run("{GCC} -o {_T} @{BUILD}/source.list", self._root)

        self.all = _all
        self.all_target = RuleTarget(self.all)


class LibraryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(LibraryGccCompiler, self).__init__(data)

        self._library = FileTarget("{BUILD}", self._name)

        @rule([self._library, [self.compile_target, self.source_list_target]])
        def _all(**kwargs):
            run("{AR} rs {_T} @{BUILD}/source.list", self._root)

        self.all = _all
        self.all_target = RuleTarget(self.all)

        @rule(self.all_target)
        def _install(**kwargs):
            self._library.copy(*self._install)

        self.install = _install
        self.install_target = RuleTarget(self.install)
