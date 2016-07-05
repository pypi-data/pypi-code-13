#
# Copyright (c) 2010 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from ovirtcli.format.format import Formatter
from ovirtcli.format.xml_ import XmlFormatter
from ovirtcli.format.text import TextFormatter


def get_formatter(format):
    """Return the formatter class for `format', or None if it doesn't exist."""
    for sym in globals():
        obj = globals()[sym]
        if isinstance(obj, type) and issubclass(obj, Formatter) \
                and obj.name == format:
            return obj
