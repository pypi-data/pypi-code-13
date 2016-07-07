# coding=utf-8
#
# This file is part of Hypothesis Legacy Support, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Hypothesis Legacy Support is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Hypothesis Legacy Support is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Hypothesis Legacy Support.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, print_function, absolute_import

import base64
import hashlib
from gzip import GzipFile as GF
from contextlib import contextmanager


@contextmanager
def GzipFile(filename, mode, mtime=None):
    result = GF(filename, mode)
    try:
        yield result
    finally:
        result.close()


def bit_length(n):
    c = 0
    while n:
        c += 1
        n >>= 1
    return c


def sha1(x):
    return hashlib.sha1(str(x))


def b64encode(x):
    return base64.b64encode(str(x))


def b64decode(x):
    return base64.b64decode(str(x))
