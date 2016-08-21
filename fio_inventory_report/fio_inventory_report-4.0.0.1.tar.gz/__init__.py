# -*- coding: utf-8 -*-
"""
    __init__.py

"""
from trytond.pool import Pool
from inventory import InventoryReport


def register():
    Pool.register(
        InventoryReport,
        module='inventory_report', type_='report'
    )
