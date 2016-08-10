"""
https://en.wikipedia.org/wiki/Telephone_numbers_in_Australia
"""

from .utils import random_int_list, pickone


def landline():
    prefix = ['02', '03', '07', '08']
    return pickone(prefix) + random_int_list(8)


def mobile():
    prefix = ['04', '05']
    return pickone(prefix) + random_int_list(8)
