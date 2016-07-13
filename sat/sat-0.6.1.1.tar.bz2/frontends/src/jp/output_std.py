#! /usr/bin/python
# -*- coding: utf-8 -*-

# jp: a SàT command line tool
# Copyright (C) 2009-2016 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Standard outputs"""


from sat_frontends.jp.constants import Const as C
import json

__outputs__ = ["Default", "Json"]
DEFAULT = u'default'
JSON = u'json'
JSON_RAW = u'json_raw'


class Default(object):
    """Default outputs"""

    def __init__(self, jp):
        jp.register_output(C.OUTPUT_TEXT, DEFAULT, self.text)
        jp.register_output(C.OUTPUT_LIST, DEFAULT, self.list)

    def text(self, data):
        print data

    def list(self, data):
        print u'\n'.join(data)


class Json(object):
    """outputs in json format"""

    def __init__(self, jp):
        jp.register_output(C.OUTPUT_LIST, JSON, self.dump_pretty)
        jp.register_output(C.OUTPUT_LIST, JSON_RAW, self.dump)
        jp.register_output(C.OUTPUT_DICT, JSON, self.dump_pretty)
        jp.register_output(C.OUTPUT_DICT, JSON_RAW, self.dump)

    def dump(self, data):
        print json.dumps(data)

    def dump_pretty(self, data):
        print json.dumps(data, indent=4)
