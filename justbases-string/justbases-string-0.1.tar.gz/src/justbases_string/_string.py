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

""" Obtaining a string from a list of digits. """

import itertools
import string

from ._errors import BaseDisplayValueError


class Digits(object):
    """
    Transforms digits as ints to corresponding symbols.
    """
    # pylint: disable=too-few-public-methods

    _LOWER_DIGITS = string.digits + string.ascii_lowercase
    _UPPER_DIGITS = string.digits + string.ascii_uppercase

    MAX_SIZE_BASE_FOR_CHARS = len(string.digits + string.ascii_uppercase)

    def __init__(self, config, base):
        """
        Initializer.

        :param DigitsConfig config: configuration for displaying digits
        :param int base: the base of the values to display

        :raises BaseDisplayValueError: if config options are bad
        """
        if config.use_letters:
            if base > self.MAX_SIZE_BASE_FOR_CHARS:
                raise BaseDisplayValueError(
                   base,
                   "base",
                   "must be no greater than number of available characters"
                )
        self.CONFIG = config
        self.base = base

    def xform(self, number):
        """
        Get a number as a string.

        Does not use separator if using letters or if base is no more than 10.

        :param number: a number
        :type number: list of int
        :returns: the number as a string
        :rtype: str
        """
        if self.CONFIG.use_letters:
            digits = \
               self._UPPER_DIGITS if self.CONFIG.use_caps else \
               self._LOWER_DIGITS
            return ''.join(digits[x] for x in number)
        else:
            separator = '' if self.base <= 10 else self.CONFIG.separator
            return separator.join(str(x) for x in number)


class Strip(object):
    """
    Handle stripping digits.
    """
    # pylint: disable=too-few-public-methods


    @staticmethod
    def _strip_trailing_zeros(value):
        """
        Strip trailing zeros from a list of ints.

        :param value: the value to be stripped
        :type value: list of str

        :returns: list with trailing zeros stripped
        :rtype: list of int
        """
        return list(
           reversed(
              list(itertools.dropwhile(lambda x: x == 0, reversed(value)))
           )
        )

    def __init__(self, config, base):
        """
        Initializer.

        :param StripConfig config: configuration for stripping zeros
        :param int base: the base
        """
        # pylint: disable=unused-argument
        self.CONFIG = config

    def xform(self, number, relation):
        """
        Strip trailing zeros from a number according to config and relation.

        :param number: a number
        :type number: list of int
        :param int relation: the relation of the display value to the actual
        """

        # pylint: disable=too-many-boolean-expressions
        if (self.CONFIG.strip) or \
           (self.CONFIG.strip_exact and relation == 0) or \
           (self.CONFIG.strip_whole and relation == 0 and \
            all(x == 0 for x in number)):
            return Strip._strip_trailing_zeros(number)
        else:
            return number


class Number(object):
    """
    Handle generic number display stuff.

    Returns modifications to the number string.
    """
    # pylint: disable=too-few-public-methods

    _FMT_STR = "".join([
       "%(sign)s",
       "%(base_prefix)s",
       "%(left)s",
       "%(radix)s",
       "%(right)s",
       "%(repeating)s",
       "%(base_separator)s",
       "%(base_subscript)s"
    ])

    def __init__(self, config, base):
        """
        Initializer.

        :param BaseConfig config: display configuration
        :param int base: the base
        """
        self.CONFIG = config
        self.base = base

    def xform(self, left, right, repeating, sign):
        """
        Return prefixes for tuple.

        :param str left: left of the radix
        :param str right: right of the radix
        :param str repeating: repeating part
        :param int sign: -1, 0, 1 as appropriate
        :returns: the number string
        :rtype: str
        """

        base_prefix = ''
        if self.CONFIG.use_prefix:
            if self.base == 8:
                base_prefix = '0'
            elif self.base == 16:
                base_prefix = '0x'
            else:
                base_prefix = ''

        base_subscript = str(self.base) if self.CONFIG.use_subscript else ''

        result = {
           'sign' : '-' if sign == -1 else '',
           'base_prefix' : base_prefix,
           'left' : left,
           'radix' : '.' if (right != "" or repeating != "") else "",
           'right' : right,
           'repeating' : ("(%s)" % repeating) if repeating != "" else "",
           'base_separator' : '' if base_subscript == '' else '_',
           'base_subscript' : base_subscript
        }

        return self._FMT_STR % result


class String(object):
    """
    Convert size components to string according to configuration.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, display, base):
        """
        Initializer.

        :param DisplayConfig display: the display config
        :param int base: the base of the radix

        :raises BaseDisplayValueError: if the configuration cannot work
        """
        self.DIGITS = Digits(display.digits_config, base)
        self.NUMBER = Number(display.base_config, base)
        self.STRIP = Strip(display.strip_config, base)

        self.base = base
        self.CONFIG = display

    def xform(
       self,
       sign,
       integer_part,
       non_repeating_part,
       repeating_part,
       relation
    ):
        """
        Transform information about a number to a string.

        :param int sign: the sign
        :param integer_part: the integer part
        :type integer_part: list of int
        :param non_repeating_part: the non-repeating part
        :type non_repeating_part: list of int
        :param repeating_part: the repeating part
        :type repeating_part: list of int
        :param Rational relation: relation of display value to actual value
        :returns: a string representing the value
        :rtype: str

        :raises BaseDisplayValueError:
        """
        # pylint: disable=too-many-arguments
        if any(x < 0 or x >= self.base for x in integer_part):
            raise BaseDisplayValueError(
               integer_part,
               "integer_part",
               "must have all elements non-negative and less than base"
            )

        if any(x < 0 or x >= self.base for x in non_repeating_part):
            raise BaseDisplayValueError(
               non_repeating_part,
               "non_repeating_part",
               "must have all elements non-negative and less than base"
            )

        if any(x < 0 or x >= self.base for x in repeating_part):
            raise BaseDisplayValueError(
               repeating_part,
               "repeating_part",
               "must have all elements non-negative and less than base"
            )

        if repeating_part == []:
            non_repeating_part = self.STRIP.xform(non_repeating_part, relation)

        right_str = self.DIGITS.xform(non_repeating_part)
        left_str = self.DIGITS.xform(integer_part) or '0'
        repeating_str = self.DIGITS.xform(repeating_part)

        number = self.NUMBER.xform(
           left_str,
           right_str,
           repeating_str,
           sign
        )

        return self.CONFIG.approx_config.xform(relation, number)
