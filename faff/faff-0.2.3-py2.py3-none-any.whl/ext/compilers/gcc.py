#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import collections
import posixpath
import shutil
from ... import (VariableContext, Variable, option, RuleTarget, FileTarget,
                 rule, dry_run, run)


class GccData(object):
    MAP = collections.OrderedDict({
        # Key: required, validator, default.
        # Absolute path to root directory.
        ("ROOT", (True, "_abspath_validator")),
        # Name of output.
        ("NAME", (True, "_str_validator")),
        # Absolute path to build directory.
        ("BUILD", (False, "_list_validator", ("build",))),
        # TODO: Install abspath.
        # GCC compiler commands.
        ("GCC", (False, "_str_validator", "gcc")),
        ("AR", (False, "_str_validator", "ar")),
        # C compiler flags.
        ("CFLAGS", (False, "_list_validator", tuple([]))),
        # TODO: Installable headers.
        # Source files.
        ("SOURCES", (True, "_list_validator")),
    })

    def __init__(self, data):
        self._data = {}
        for key, item in self.MAP.items():
            if item[0]:
                value = data[key]
            else:
                value = data.get(key, item[2])
            if hasattr(self, item[1]):
                validator = getattr(self, item[1])
                self._data[key] = validator(value)

    def _str_validator(self, value):
        return str(value)

    def _list_validator(self, value):
        return list(value)

    def _abspath_validator(self, value):
        return os.path.abspath(value)

    def _build_validator(self, value):
        value = os.path.join(self.get("ROOT"), *value)
        return os.path.abspath(value)

    @property
    def data(self):
        return self._data

    @property
    def root(self):
        return self.get("ROOT")

    @property
    def name(self):
        return self.get("NAME")

    @property
    def absolute_build(self):
        path = os.path.join(self.root, *self.get("BUILD"))
        return os.path.abspath(path)

    @property
    def relative_build(self):
        return posixpath.join(*self.get("BUILD"))

    def get(self, key):
        return self._data[key]


class GccCompiler(object):

    def __init__(self, data):
        self._data = GccData(dict(data))
        self._context = VariableContext()
        ctx = {"context": self._context}

        # Default variable values.
        # Absolute directory paths.
        Variable("ROOT", self._data.root, **ctx)
        Variable("BUILD", self._data.absolute_build, **ctx)

        # GCC commands.
        Variable("GCC", self._data.get("GCC"), self._context)
        Variable("AR", self._data.get("AR"), self._context)

        # C compiler flags.
        CFLAGS = Variable("CFLAGS", context=self._context)
        for cflag in self._data.get("CFLAGS"):
            CFLAGS += cflag

        # File targets.
        # TODO: Source file target for dependencies.
        self._sources = self._data.get("SOURCES")
        self._source_files = [
            FileTarget("{ROOT}", *x, context=self._context)
            for x in self._sources]
        self._object_files = [
            FileTarget("{BUILD}", *x, ext=".o", context=self._context)
            for x in self._sources]

        self._relative_objects = []
        for src in self._sources:
            path = posixpath.join(self._data.relative_build, *src)
            pre, ext = posixpath.splitext(path)
            self._relative_objects.append(pre + ".o")

        # Generic rules.
        # Source compiler rule.
        @rule([self._object_files, self._source_files], context=self._context)
        def __compile_source(**kwargs):
            run(
                "{GCC} -c {CFLAGS} {_D} -o {_T}",
                self._data.root, context=self._context)

        self._compile_source = __compile_source
        self._compile_source_target = RuleTarget(
            self._compile_source, context=self._context)

        # Source file list rule.
        self._source_list_file = FileTarget(
            "{BUILD}", "source.list", context=self._context)
        self._source_list_file.exists()

        @rule(context=self._context)
        def __source_list(**kwargs):
            with open(str(self._source_list_file), "w") as f:
                obj = [
                    Variable.expand(x, self._context)
                    for x in self._relative_objects]
                f.write("\n".join(obj))
                f.write("\n")

        self._source_list = __source_list
        self._source_list_target = RuleTarget(
            self._source_list, context=self._context)

        # Clean rule.
        @rule(context=self._context)
        def __clean(**kwargs):
            # TODO: Error handling.
            try:
                shutil.rmtree(Variable.expand("{BUILD}", self._context))
            except:
                pass

        self._clean = __clean
        self._clean_target = RuleTarget(self._clean, context=self._context)

    @property
    def compile_source_target(self):
        return self._compile_source_target

    @property
    def source_list_target(self):
        return self._source_list_target

    @property
    def clean_target(self):
        return self._clean_target


class BinaryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(BinaryGccCompiler, self).__init__(data)

        self._binary = FileTarget(
            "{BUILD}", self._data.name, context=self._context)

        @rule(
            [self._binary,
                [self.compile_source_target, self.source_list_target]],
            context=self._context)
        def __all(**kwargs):
            run(
                "{GCC} -o {_T} @{BUILD}/source.list",
                self._data.root, context=self._context)

        self._all = __all
        self._all_target = RuleTarget(self._all, context=self._context)

    @property
    def all_target(self):
        return self._all_target


class LibraryGccCompiler(GccCompiler):

    def __init__(self, data):
        super(LibraryGccCompiler, self).__init__(data)

        self._library = FileTarget(
            "{BUILD}", self._data.name, context=self._context)

        @rule(
            [self._library,
                [self.compile_source_target, self.source_list_target]],
            context=self._context)
        def __all(**kwargs):
            run(
                "{AR} rs {_T} @{BUILD}/source.list",
                self._data.root, context=self._context)

        self._all = __all
        self._all_target = RuleTarget(self._all, context=self._context)

    @property
    def all_target(self):
        return self._all_target

        # @rule(self.all_target)
        # def _install(**kwargs):
        #     self._library.copy(*self._install)
        #
        # self.install = _install
        # self.install_target = RuleTarget(self.install)
