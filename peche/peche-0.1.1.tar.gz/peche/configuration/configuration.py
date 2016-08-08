#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import os


class Configuration(object):
    _kwargs = {}
    _config = {}

    def __init__(self, context, path, **kwargs):
        self.path = path
        self._kwargs = kwargs
        self._context = context

        self._load()

    def _load(self):
        components = [self._context.name]
        components.extend(self.path.split('.'))

        conf_paths = []

        for index, component in enumerate(components):
            tree = [self._context.config_root]
            tree.extend(components[1:index + 1])

            tree.append('conf.json')

            conf_paths.append(os.path.join(*tree))

        for path in conf_paths:
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'r') as f:
                    config = json.load(f)
                    self._config.update(config)

        self._config.update(self._kwargs)

