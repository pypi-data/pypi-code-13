# -*- coding: utf-8 -*-
"""
    Employee


"""
from trytond.pool import PoolMeta
from trytond.model import fields


__metaclass__ = PoolMeta
__all__ = ['Employee']


class Employee:
    __name__ = 'company.employee'

    quickbooks_source_name = fields.Char('Quickbooks Source Name')
