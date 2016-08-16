# Copyright 2016 Geoffrey MacGill
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import with_statement

import os.path
import abc
import collections
import io

import requests

from six.moves.urllib import parse
import six

from .dictconfig import DictConfiguration
from .parsers import Parser


FILE_EXTENSION_HINTS = {
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'cfg': 'ini',
    'conf': 'ini',
    'cnf': 'ini',
    'config': 'ini',
    'ini': 'ini',
    'xml': 'xml'
}

MIME_TYPE_HINTS = {
    'text/yaml': 'yaml',
    'text/x-yaml': 'yaml',
    'application/yaml': 'yaml',
    'application/x-yaml': 'yaml',
    'application/json': 'json',
    'text/plain': 'ini',
    'text/xml': 'xml',
    'application/xml': 'xml'
}


@six.add_metaclass(abc.ABCMeta)
class BaseConfigSource(object):
    def __init__(self,
                 source,
                 hint=None):
        self._source = source
        self._hint = None
        if hint:
            resolved = FILE_EXTENSION_HINTS.get(hint.lower(), None)
            if not resolved:
                raise ValueError('Unrecognized config type {0:s}'.format(hint))
            self._hint = resolved

    def __str__(self):
        return self.source

    def __repr__(self):
        return "{0:s}('{1:s}', {2:s})".format(
            self.__class__.__name__,
            self.source or 'None',
            self.hint or 'None')

    @property
    def source(self):
        return self._source

    @property
    def hint(self):
        return self._hint

    @abc.abstractmethod
    def load(self):
        pass


class FileConfigSource(BaseConfigSource):
    def __init__(self,
                 source,
                 hint=None,
                 encoding=None):
        # parse the extension if no hint provided
        if not source:
            raise ValueError('Source not provided for file config')
        if source[0] == '@':
            source = source[1:]
        self._encoding = encoding

        super(FileConfigSource, self).__init__(source,
                                               hint)

        self._url_parts = parse.urlparse(self.source)
        # default scheme to file
        self._scheme = self._url_parts.scheme or 'file'
        self._scheme = self._scheme.lower()

        # update hint for local file if not explicitly set
        if self._scheme == 'file' and not self.hint:
            root, ext = os.path.splitext(self.source)
            if not ext:
                ext = root
            if ext.startswith('.'):
                ext = ext[1:]
            self._hint = FILE_EXTENSION_HINTS.get(ext, None)

    @property
    def encoding(self):
        return self._encoding

    def load(self):
        super(FileConfigSource, self).load()
        if self._scheme == 'file':
            return self._load_file()
        elif self._scheme.startswith('http'):
            return self._load_http()
        else:
            raise ValueError('Unsupported source scheme {0:s}'.format(
                self._scheme))

    def _load_file(self):
        with io.open(self.source,
                     mode='rt',
                     encoding=(self.encoding or None)) as instream:
            if not self.hint:
                # avoid multiple reads if we don't know what the file hint is
                return Parser.load(instream.read(), self)
            else:
                return Parser.load(instream, self)

    def _load_http(self):
        try:
            response = requests.get(self.source)
            response.raise_for_status()
        except (requests.HTTPError,
                requests.ConnectionError,
                requests.Timeout):
            return None

        if not self.hint:
            content_type = response.headers.get('content-type', None)
            if content_type:
                self._hint = MIME_TYPE_HINTS.get(content_type.lower(), None)

            # maybe a file extnsion of path?
            if not self.hint:
                root, ext = os.path.splitext(self._url_parts.path)
                if not ext:
                    ext = root
                if ext.startswith('.'):
                    ext = ext[1:]
                self._hint = FILE_EXTENSION_HINTS.get(ext, None)

        return Parser.load(response.text, self)


class EmptyConfigSource(BaseConfigSource):
    def __init__(self,
                 source,
                 hint=None):
        super(EmptyConfigSource, self).__init__(source,
                                                hint)

    def load(self):
        super(EmptyConfigSource, self).load()
        return None


class LiteralConfigSource(BaseConfigSource):
    def __init__(self,
                 source,
                 hint=None):
        if not hint:
            raise ValueError('Hint must be provided for a literal source')
        super(LiteralConfigSource, self).__init__(source,
                                                  hint)

    def load(self):
        super(LiteralConfigSource, self).load()
        return Parser.load(self.source, self)


class ObjectConfigSource(BaseConfigSource):
    def __init__(self,
                 source,
                 hint=None):
        super(ObjectConfigSource, self).__init__(source,
                                                 hint)

    def load(self):
        super(ObjectConfigSource, self).load()
        config_instance = DictConfiguration()
        config_instance.update(self.source)
        return config_instance


def load_config(targets, defaults=None, merge=True):
    targets = _normalize_targets(targets)
    config_instance = DictConfiguration()

    for target in targets:
        if isinstance(target, EmptyConfigSource):
            continue

        next_config = target.load()
        if next_config:
            config_instance.merge(next_config)
            if not merge:
                break

    return config_instance


def load_first_found_config(targets, defaults=None):
    return load_config(targets, merge=False)


def _normalize_targets(targets):
    # make this a list if not a list
    if isinstance(targets, six.string_types) or\
            isinstance(targets, collections.Mapping) or\
            not isinstance(targets, collections.Iterable):
        targets = (targets, )

    return [_normalize_target(x) for x in targets]


def _normalize_target(target):
    if not target:
        return EmptyConfigSource(target)

    if isinstance(target, BaseConfigSource):
        return target

    resolved = EmptyConfigSource(target)

    if isinstance(target, six.string_types):
        resolved = FileConfigSource(target)
    elif isinstance(target, collections.Mapping):
        resolved = ObjectConfigSource(target)

    return resolved
