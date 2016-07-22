# -*- coding: utf-8 -*-
import os
from jschema.errors import JrsMakeError


class Options(object):

    def __init__(self, options):
        self._options = options
        self._dst_path = None
        self._dst_dir = None
        self._ns = None

    @property
    def dst_path(self):
        if self._dst_path is None:
            if "dst_path" not in self._options:
                raise JrsMakeError("options['dst_path'] not exists")

            self._dst_path = self._options["dst_path"]
            dst_dir = os.path.dirname(self._dst_path)
            if not os.path.exists(dst_dir):
                os.path.makedirs(dst_dir)

        return self._dst_path

    @property
    def dst_dir(self):
        if self._dst_dir is None:
            if "dst_dir" not in self._options:
                raise JrsMakeError("options['dst_dir'] not exists")

            dst_dir = self._dst_dir = self._options["dst_dir"]
            if not os.path.exists(dst_dir):
                os.path.makedirs(dst_dir)

        return self._dst_dir

    @property
    def ns(self):
        if self._ns is None:
            if "ns" not in self._options:
                raise JrsMakeError("options['ns'] not exists")

            self._ns = self._options["ns"]

        return self._ns
