# -*- coding: utf-8 -*-
from decimal import Decimal

from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.exceptions import UserError

__metaclass__ = PoolMeta
__all__ = ['ShipmentOut']


class ShipmentOut:
    "Shipment Out"
    __name__ = 'stock.shipment.out'

    def _get_carrier_context(self):
        "Pass shipment in the context"
        context = super(ShipmentOut, self)._get_carrier_context()

        if not self.carrier.carrier_cost_method == 'pricelist':
            return context

        context = context.copy()
        context['shipment'] = self.id
        return context

    def get_pricelist_shipping_cost(self):
        """
        Return pricelist shipping cost
        """
        Product = Pool().get('product.product')
        Carrier = Pool().get('carrier')
        Company = Pool().get('company.company')

        carrier, = Carrier.search([('carrier_cost_method', '=', 'pricelist')])

        total = Decimal('0')

        company = Transaction().context.get('company')
        if not company:
            raise UserError("Company not in context.")

        default_currency = Company(company).currency

        with Transaction().set_context(
                customer=self.customer.id,
                price_list=carrier.price_list.id,
                currency=default_currency.id):
            for move in self.outgoing_moves:
                total += \
                    Product.get_sale_price([move.product])[move.product.id] * \
                    Decimal(move.quantity)

        return total, default_currency.id

    def get_shipping_rate(self, carrier, carrier_service=None, silent=False):
        Currency = Pool().get('currency.currency')

        cost, currency_id = self.get_pricelist_shipping_cost()
        if carrier.carrier_cost_method == 'pricelist':
            rate_dict = {
                'carrier_service': carrier_service,
                'cost': cost,
                'cost_currency': Currency(currency_id),
                'carrier': carrier,
                'display_name': carrier.rec_name
            }
            return [rate_dict]

        return []
