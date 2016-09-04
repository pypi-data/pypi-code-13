# -*- coding: utf-8 -*-
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__metaclass__ = PoolMeta
__all__ = ['Carrier']


class Carrier:
    __name__ = "carrier"

    price_list = fields.Many2One(
        "product.price_list", "Price List", states={
            "required": Eval("carrier_cost_method") == "pricelist",
            "invisible": Eval("carrier_cost_method") != "pricelist"
        }
    )

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('pricelist', 'Price List')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)
