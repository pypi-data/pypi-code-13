# coding=utf-8

from monstro.core.exceptions import MonstroError


class ORMError(MonstroError):

    pass


class ValidationError(ORMError):

    def __init__(self, error=None):
        self.error = error

        super().__init__(self.error)


class DoesNotExist(ORMError):

    pass
