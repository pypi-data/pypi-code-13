#
# Copyright (c) 2016, Michael Conroy
#


import re


from exceptions import ValidationException, ValidationConfigurationException


__all__ = (
    'BaseValidator',
    'BaseTypeValidator',

    'IntVal',
    'FloatVal',
    'BoolVal',

    'EnumVal',
    'UniqueVal',
    'RegexVal',
    'EmptyVal',
    'AnyVal',
)


FAILURE_COUNT_INITIALIZE = 0


class BaseValidator(object):
    """ Base class for validators """

    failure_count = FAILURE_COUNT_INITIALIZE

    def validate(self, field, row):
        """
        Validate given field with row context.

        Implementations must override this method.
        """

        raise NotImplementedError("%s.validate()" % self.__class__.__name__)

    def fails(self):
        """
        Return failed fields.

        Implementations must override this method.
        """

        raise NotImplementedError("%s.validate()" % self.__class__.__name__)


class BaseTypeValidator(BaseValidator):
    """ Base class for type validators """

    def __init__(self):
        super(BaseTypeValidator, self).__init__()
        self.invalid_set = set([])

    def validate(self, field, row={}):
        try:
            if (field or not self.empty_ok):
                self.cast(field)
        except ValueError as exc:
            self.invalid_set.add(field)
            raise ValidationException(exc)

    def fails(self):
        return self.invalid_set


class IntVal(BaseTypeValidator):

    def __init__(self, empty_ok=False):
        super(IntVal, self).__init__()
        self.empty_ok = empty_ok
        self.cast = int


class FloatVal(BaseTypeValidator):

    def __init__(self, empty_ok=False):
        super(FloatVal, self).__init__()
        self.empty_ok = empty_ok
        self.cast = float


class BoolVal(BaseTypeValidator):

    def __init__(self, empty_ok=False):
        super(BoolVal, self).__init__()
        self.empty_ok = empty_ok
        self.cast = bool


class EnumVal(BaseValidator):
    """ Validates a field against an enumerated list """

    def __init__(self, enum_list=[], empty_ok=False):
        super(EnumVal, self).__init__()
        self.empty_ok = empty_ok
        self.enum_set = set(enum_list)  # Make enumerations unique
        self.invalid_enum_set = set([])
        if empty_ok:
            self.enum_set.add('')

    def validate(self, field, row={}):
        if field not in self.enum_set:
            self.invalid_enum_set.add(field)
            raise ValidationException(
                "'{}' is not in {}".format(field, self.enum_set))

    def fails(self):
        return self.invalid_enum_set


class UniqueVal(BaseValidator):
    """ Validates uniqueness in a column """

    def __init__(self, unique_list=[]):
        super(UniqueVal, self).__init__()
        self.unique_set = set(unique_list)  # Make list unique
        self.duplicates = set([])
        self.unique_values = set([])

    def validate(self, field, row={}):
        if self.unique_set:
            extra = self.unique_set - set(row.keys())
            if extra:
                raise ValidationConfigurationException(extra)

        key = tuple([field] + [row[k] for k in self.unique_set])
        if key not in self.unique_values:
            self.unique_values.add(key)
        else:
            self.duplicates.add(key)
            if self.unique_set:
                raise ValidationException(
                    "'{}' is already in the column (unique with: {})".format(
                        field, key[1:]))
            else:
                raise ValidationException(
                    "'{}' is already in the column".format(field))

    def fails(self):
        return self.duplicates


class RegexVal(BaseValidator):
    """ Validates field against a regular expression """

    def __init__(self, pattern=r'$a', empty_ok=False):
        super(RegexVal, self).__init__()
        self.regex = re.compile(pattern)
        self.empty_ok = empty_ok
        self.regex_failures = set([])

    def validate(self, field, row={}):
        if (field or not self.empty_ok) and not self.regex.match(field):
            self.regex_failures.add(field)
            raise ValidationException(
                "'{}' does not match pattern /{}/".format(field,
                                                          self.regex.pattern))

    def fails(self):
        return self.regex_failures


class EmptyVal(BaseValidator):
    """ Validates field is always empty """

    def __init__(self):
        super(EmptyVal, self).__init__()
        self.nonempty_values = set([])

    def validate(self, field, row={}):
        if field != '':
            self.nonempty_values.add(field)
            raise ValidationException(
                "'{}' is not an empty string".format(field))

    def fails(self):
        return self.nonempty_values


class AnyVal(BaseValidator):
    """ Ignores validating a field """

    def validate(self, field, row={}):
        pass

    def fails(self):
        pass
