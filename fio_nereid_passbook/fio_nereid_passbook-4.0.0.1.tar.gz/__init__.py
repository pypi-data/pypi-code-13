# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from passbook import Pass, Registration


def register():
    Pool.register(
        Pass,
        Registration,
        module='nereid_passbook', type_='model'
    )
