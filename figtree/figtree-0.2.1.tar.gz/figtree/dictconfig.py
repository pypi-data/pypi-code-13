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

import collections
import six


class DictConfiguration(collections.MutableMapping):
    def __init__(self,
                 *args,
                 **kwargs):
        self._internal_store = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        keys = self._parse_key(key)

        context = self._internal_store
        location = []

        for item in keys:
            location.append(item)
            if context is None:
                raise KeyError('{0:s} ({1:s})'.format('.'.join(location), key))
            if not isinstance(context, collections.Mapping):
                raise KeyError('{0:s} ({1:s}) is not a mapping'.format(
                    '.'.join(location), key))

            try:
                context = context[item]
            except KeyError:
                raise KeyError('{0:s} ({1:s})'.format('.'.join(location), key))

        return context

    def __setitem__(self, key, value):
        keys = self._parse_key(key)

        context = self._internal_store

        for item in keys[:-1]:
            child = context.get(item, None)
            if child is None or not isinstance(child, collections.Mapping):
                child = DictConfiguration()
                context[item] = child
            # should be unreachable code
            # if not isinstance(child, DictConfiguration):
            #     child = DictConfiguration(child)
            #     context[item] = child

            context = child

        context[keys[-1]] = self._maybe_make_dict_config(value)

    def __delitem__(self, key):
        keys = self._parse_key(key)

        context = self._internal_store
        location = []

        for item in keys[:-1]:
            location.append(item)
            if context is None:
                raise KeyError('{0:s} ({1:s})'.format('.'.join(location), key))
            if not isinstance(context, collections.Mapping):
                raise KeyError('{0:s} ({1:s}) is not a mapping'.format(
                    '.'.join(location) or '', key))

            context = context.get(item, None)

        if not isinstance(context, collections.Mapping):
            raise KeyError('{0:s} ({1:s}) is not a mapping'.format(
                '.'.join(location), key))
        del context[keys[-1]]

    def __iter__(self):
        return iter(self._internal_store)

    def __len__(self):
        return len(self._internal_store)

    def _parse_key(self, key):
        result = []
        if not key:
            raise KeyError('empty key')
        if not isinstance(key, six.string_types):
            raise TypeError('key is not a string')

        keys = key.split('.')

        for item in keys:
            if not item:
                raise KeyError('empty key segement in path')
            result.append(item)

        if not result:
            raise KeyError('empty key')

        return result

    def merge(self, other):
        if not isinstance(other, collections.Mapping):
            raise ValueError('Cannot merge non-mapping type')

        other = self._make_dict_config(other)

        for k, v in six.iteritems(other):
            if k not in self:
                self[k] = v
                continue

            this_v = self[k]
            if isinstance(this_v, collections.Mapping) and\
                    isinstance(v, collections.Mapping):
                this_v.merge(v)
            else:
                self[k] = v

    @classmethod
    def _make_dict_config(cls, value, recurse=True):
        if value is None:
            return None

        result = None

        if isinstance(value, cls):
            result = value
        else:
            # let this raise an error just like a normal dictionary if the user
            # gave us an invalid value
            result = cls(value)

        if not recurse:
            return result

        # queues will better handle heavily nested configurations, but I pitty
        # the developer who has config nested so deep that it could blow the
        # stack
        remaining = collections.deque()
        remaining.extend([(result, k, v) for k, v in six.iteritems(result)])

        while True:
            try:
                # get the next item to massage
                cur_parent, cur_key, cur_value = remaining.popleft()
            except IndexError:
                break

            if not isinstance(cur_value, collections.Mapping):
                # the current value is not a mapping, so leave it be
                # we don't process values of other structured types, such
                # as tuples and lists
                continue

            if not isinstance(cur_value, cls):
                # this is some other type of mapping, make it ours
                cur_value = cls(cur_value)
                cur_parent[cur_key] = cur_value

            # queue up the inspection of its children
            remaining.extend(
                [(cur_value, k, v) for k, v in six.iteritems(cur_value)])

        return result

    @classmethod
    def _maybe_make_dict_config(cls, value, recurse=True):
        if value is None:
            return None

        if not isinstance(value, collections.Mapping):
            return value

        return cls._make_dict_config(value, recurse=recurse)

    def __str__(self):
        return self._internal_store.__str__()

    def __repr__(self):
        return self._internal_store.__repr__()
