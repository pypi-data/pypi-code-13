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

import abc

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import collections

try:
    from collections import OrderedDict
    PY26_ORDEREDDICT = False
except ImportError:
    from ordereddict import OrderedDict
    PY26_ORDEREDDICT = True

import six
import yaml
import lxml.etree
import lxml.objectify

try:
    import simplejson as json
except ImportError:
    import json

from .dictconfig import DictConfiguration


CONFIGPARSER_DEFAULTS = {
    'strict': False,  # python 3+
    'empty_lines_in_values': False
}


if six.PY2:
    CONFIGPARSER_DEFAULTS.pop('strict')
    CONFIGPARSER_DEFAULTS.pop('empty_lines_in_values')


class ParserMeta(abc.ABCMeta):
    def __new__(cls, name, bases, attrs):
        abstract = attrs.pop('abstract', False)
        key = attrs.pop('name', None)

        cls_new = super(ParserMeta, cls).__new__(
            cls,
            name,
            bases,
            attrs)

        # check if message type is registered
        parsers = getattr(cls_new, '_parsers', None)
        if parsers is None:
            parsers = {}
            setattr(cls_new, '_parsers', parsers)

        # only register if not abstract
        if not abstract and key:
            parsers[key] = cls_new

        return cls_new


@six.add_metaclass(ParserMeta)
class Parser(object):
    abstract = True

    def __init__(self):
        pass

    @classmethod
    def load(cls, data, source):
        # pylint: disable=E1101
        loader = cls._parsers.get(source.hint, None)

        if loader:
            # pylint: disable=W0212
            return loader()._load(data)

        result = None
        for x in cls._parsers.values():
            try:
                # pylint: disable=W0212
                result = x()._load(data)
                break
            except Exception as e:
                # logging.exception(e)
                result = None
                continue
        return result

    @abc.abstractmethod
    def _load(self, data):
        pass


class YamlParser(Parser):
    name = 'yaml'

    def _load(self, data):
        super(YamlParser, self)._load(data)
        loaded_data = yaml.safe_load(data)
        config_instance = DictConfiguration()
        config_instance.update(loaded_data)
        return config_instance


class JsonParser(Parser):
    name = 'json'

    def _load(self, data):
        super(JsonParser, self)._load(data)
        loaded_data = None
        if hasattr(data, 'read'):
            loaded_data = json.load(data)
        else:
            loaded_data = json.loads(data)
        config_instance = DictConfiguration()
        config_instance.update(loaded_data)
        return config_instance


class IniParser(Parser):
    name = 'ini'

    def _load(self, data):
        super(IniParser, self)._load(data)
        config_instance = DictConfiguration()
        parser = configparser.RawConfigParser(
            dict_type=MultiOrderedDict,
            **CONFIGPARSER_DEFAULTS)
        if six.PY2:
            instream = data
            if not hasattr(instream, 'read'):
                instream = six.StringIO(data)
            parser.readfp(instream)
        else:
            if isinstance(data, six.string_types):
                # pylint: disable=E1101
                parser.read_string(data)
            else:
                parser.readfp(data)
        for section in parser.sections():
            for item, value in parser.items(section):
                key = '{0:s}.{1:s}'.format(section, item)
                value = _parse_value(value)
                if not isinstance(value, six.string_types) and\
                        isinstance(value, collections.Sequence):
                    value = [_parse_value(x) for x in value]
                config_instance[key] = value
        return config_instance


class XmlParser(Parser):
    name = 'xml'

    def _load(self, data):
        super(XmlParser, self)._load(data)
        config_instance = DictConfiguration()
        tree = None
        if not hasattr(data, 'read'):
            data = six.StringIO(data) if isinstance(data, six.string_types)\
                    else six.BytesIO(data)
        tree = lxml.objectify.parse(data)

        # use queue to avoid recursion and prime it with the immediate children
        elements = collections.deque()
        for x in tree.getroot().iterchildren():
            elements.append(('', x))

        while True:
            try:
                prefix, element = elements.popleft()
            except IndexError:
                break
            key = element.tag
            if prefix:
                key = '{0:s}.{1:s}'.format(prefix, element.tag)
            if isinstance(element, lxml.objectify.ObjectifiedDataElement):
                previous = config_instance.get(key, None)
                value = _parse_value(element.pyval)
                if previous:
                    if isinstance(previous, collections.MutableSequence):
                        previous.append(value)
                    else:
                        value = [previous, value]
                        config_instance[key] = value
                else:
                    config_instance[key] = value
            else:
                for x in element.iterchildren():
                    elements.append((key, x))

        return config_instance


def _parse_value(value):
    handlers = [
        (int, (ValueError, )),
        (float, (ValueError, )),
        (_bool, (ValueError, ))
    ]

    if not isinstance(value, six.string_types):
        # already a python type
        return value

    for parser, errors in handlers:
        try:
            return parser(value)
        # pylint: disable=W0703
        except Exception as e:
            if isinstance(e, errors):
                continue

    return value


def _bool(value):
    if value is None:
        raise ValueError('invalid literal for _bool()')
    str_bool_mapping = {
        'yes': True,
        'true': True,
        'on': True,
        'no': False,
        'false': False,
        'off': False,
    }
    if not isinstance(value, six.string_types):
        raise ValueError('invalid literal for _bool()')
    try:
        return str_bool_mapping[value.lower()]
    except KeyError:
        raise ValueError('invalid literal for _bool()')


class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self:
            if PY26_ORDEREDDICT:
                if isinstance(value, six.string_types):
                    self[key].append(value)
                    return
            if isinstance(value, list):
                self[key].extend(value)
                return
            elif isinstance(value, six.string_types):
                if len(self[key]) > 1:
                    return
        elif PY26_ORDEREDDICT:
            if isinstance(value, six.string_types):
                value = [value, ]
            elif isinstance(value, list):
                if len(value) == 1:
                    value = value[0]

        super(MultiOrderedDict, self).__setitem__(key, value)
