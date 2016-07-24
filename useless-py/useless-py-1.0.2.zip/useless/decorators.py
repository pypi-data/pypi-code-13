#!/usr/bin/env python

__author__ = 'Ronie Martinez'


def extends(additional_class):
    """
    Inheritance using a decorator.
    :param additional_class: Additional base class to inherit from.
    :return:
    """
    def _extends(original_class):
        class NewClass(original_class, additional_class):
            pass
        NewClass.__name__ = original_class.__name__
        return NewClass
    return _extends
