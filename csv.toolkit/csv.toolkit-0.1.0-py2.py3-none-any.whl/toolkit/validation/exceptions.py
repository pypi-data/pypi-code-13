#
# Copyright (c) 2016, Michael Conroy
#


__all__ = (
    'ValidationException',
    'ValidationConfigurationException',
)


class ValidationException(Exception):
    """ Base validation exception """

    pass


class ValidationConfigurationException(ValidationException):
    """ Exception for poorly configured validator configuration """

    pass
