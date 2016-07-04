# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from .converter import NopConverterCreator
from .converter import IntegerConverterCreator
from .converter import FloatConverterCreator
from .converter import BoolConverterCreator
from .converter import DateTimeConverterCreator
from ._error import TypeConversionError
from ._function import is_nan
from ._typecode import Typecode


@six.add_metaclass(abc.ABCMeta)
class TypeCheckerInterface(object):

    @abc.abstractproperty
    def typecode(self):   # pragma: no cover
        pass

    @abc.abstractmethod
    def is_type(self):   # pragma: no cover
        pass


class TypeChecker(TypeCheckerInterface):

    @abc.abstractproperty
    def _converter_creator(self):   # pragma: no cover
        pass

    def __init__(self, value, is_convert=True):
        self._value = value
        self._converted_value = None
        self._is_convert = is_convert

    def is_type(self):
        if self._is_instance():
            return True

        if self._is_exclude_instance():
            return False

        if not self._is_convert:
            return False

        try:
            self._try_convert()
        except TypeConversionError:
            return False

        if not self._is_valid_after_convert():
            return False

        return True

    @abc.abstractmethod
    def _is_instance(self):
        pass

    def _is_exclude_instance(self):
        return False

    def _try_convert(self):
        self._converted_value = self._converter_creator.create(
            self._value).convert()

    def _is_valid_after_convert(self):
        return True


class NoneTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.NONE

    @property
    def _converter_creator(self):
        return NopConverterCreator()

    def _is_instance(self):
        return self._value is None

    def _is_valid_after_convert(self):
        return self._value is None


class IntegerTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.INT

    @property
    def _converter_creator(self):
        return IntegerConverterCreator()

    def _is_instance(self):
        if isinstance(self._value, six.integer_types):
            return not isinstance(self._value, bool)

        return False

    def _is_exclude_instance(self):
        return any([
            isinstance(self._value, bool),
            isinstance(self._value, float),
        ])


class FloatTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.FLOAT

    @property
    def _converter_creator(self):
        return FloatConverterCreator()

    def _is_instance(self):
        return any(
            [isinstance(self._value, float), self._value == float("inf")])

    def _is_exclude_instance(self):
        return isinstance(self._value, bool)

    def _is_valid_after_convert(self):
        return self._converted_value != float("inf")


class BoolTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.BOOL

    @property
    def _converter_creator(self):
        return BoolConverterCreator()

    def _is_instance(self):
        return isinstance(self._value, bool)

    def _is_valid_after_convert(self):
        return isinstance(self._converted_value, bool)


class DateTimeTypeChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.DATETIME

    @property
    def _converter_creator(self):
        return DateTimeConverterCreator()

    def _is_instance(self):
        import datetime

        return isinstance(self._value, datetime.datetime)


class InfinityChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.INFINITY

    @property
    def _converter_creator(self):
        return FloatConverterCreator()

    def _is_instance(self):
        return self._value == float("inf")

    def _is_valid_after_convert(self):
        return self._converted_value == float("inf")


class NanChecker(TypeChecker):

    @property
    def typecode(self):
        return Typecode.NAN

    @property
    def _converter_creator(self):
        return FloatConverterCreator()

    def _is_instance(self):
        return is_nan(self._value)

    def _is_valid_after_convert(self):
        return is_nan(self._converted_value)
