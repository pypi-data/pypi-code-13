# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" String method configuration. """

from fractions import Fraction

from ._approx import ApproxPrefix


class BaseConfig(object):
    """
    Whether and how to show the base.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "use_prefix=%(use_prefix)s",
       "use_subscript=%(use_subscript)s"
    ])

    def __init__(self, use_prefix=False, use_subscript=True):
        """
        Initializer.

        :param bool use_prefix: show base using prefix, e.g., 0x, 0
        :param bool use_subscript: show base using subscript
        """
        self.use_prefix = use_prefix
        self.use_subscript = use_subscript

    def __str__(self): # pragma: no cover
        values = {
           'use_prefix' : self.use_prefix,
           'use_subscript' : self.use_subscript
        }
        return "BaseConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class StripConfig(object):
    """
    Stripping trailing zeros.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "strip=%(strip)s",
       "strip_exact=%(strip_exact)s",
       "strip_whole=%(strip_whole)s"
    ])

    def __init__(self, strip=False, strip_exact=False, strip_whole=True):
        """
        Initializer.

        :param bool strip: strip all trailing zeros
        :param bool strip_exact: strip if value is exact
        :param bool strip_whole: strip if value is exact and non-fractional

        strip is stronger than strip_exact which is stronger than strip_whole
        """
        self.strip = strip
        self.strip_exact = strip_exact
        self.strip_whole = strip_whole

    def __str__(self): # pragma: no cover
        values = {
           'strip' : self.strip,
           'strip_exact' : self.strip_exact,
           'strip_whole' : self.strip_whole
        }
        return "StripConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class DigitsConfig(object):
    """
    How to display digits.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "separator=%(separator)s",
       "use_caps=%(use_caps)s",
       "use_letters=%(use_letters)s"
    ])

    def __init__(
       self,
       separator='~',
       use_caps=False,
       use_letters=True
    ):
        """
        Initializer.

        :param str separator: separate for digits
        :param bool use_caps: if set, use capital letters
        :param bool use_letters: if set, use letters

        If digits in this base require more than one character.
        """
        self.separator = separator
        self.use_caps = use_caps
        self.use_letters = use_letters

    def __str__(self): # pragma: no cover
        values = {
           'separator' : self.separator,
           'use_caps' : self.use_caps,
           'use_letters' : self.use_letters
        }
        return "DigitsConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class ApproxConfig(object):
    """
    Whether and how to show approximation information.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "xform=%(xform)s"
    ])

    def __init__(
       self,
       xform=ApproxPrefix([Fraction(1, 2)]).xform
    ):
        """
        Initializer.

        :param xform: a transformer for a number, to show approximation info
        :type xform: (Rational * str) -> str
        """
        self.xform = xform

    def __str__(self): # pragma: no cover
        values = {
           'xform' : self.xform
        }
        return "ApproxConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__


class DisplayConfig(object):
    """
    Superficial aspects of display.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = ", ".join([
       "approx_config=%(approx_config)s",
       "base_config=%(base_config)s",
       "digits_config=%(digits_config)s",
       "strip_config-%(strip_config)s"
    ])

    def __init__(
       self,
       approx_config=ApproxConfig(),
       base_config=BaseConfig(),
       digits_config=DigitsConfig(),
       strip_config=StripConfig()
    ):
        """
        Initializer.

        :param ApproxConfig approx_config: how to show approximation information
        :param BaseConfig base_config: how to show base
        :param DigitsConfig digits_config: how to display digits
        :param StripConfig strip_config: how to strip zeros

        There are only two base prefixes acknowledged, 0 for octal and 0x for
        hexadecimal.
        """
        self.approx_config = approx_config
        self.base_config = base_config
        self.digits_config = digits_config
        self.strip_config = strip_config

    def __str__(self): # pragma: no cover
        values = {
           'approx_config' : self.approx_config,
           'base_config' : self.base_config,
           'digits_config' : self.digits_config,
           'strip_config' : self.strip_config
        }
        return "DisplayConfig(%s)" % (self._FMT_STR % values)
    __repr__ = __str__
