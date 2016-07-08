#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import appier
import shopify
import easypay

import shopdesk

LOOP_TIMEOUT = 30.0
""" The time value to be used to sleep the main sequence
loop between ticks, this value should not be too small
to spend many resources or to high to create a long set
of time between external interactions """

ORDER_TIMEOUT = 2.0 * 24.0 * 3600.0
""" The default order timeout value that is going to
be used to measure the amount of time before an order
is considered expired and it's canceled """

WARNING_TIMEOUT = 1.0 * 24.0 * 3600.0
""" The default order timeout value that is going to
be used to measure the amount of time before an order
is considered to be warned and an email is sent """

class Scheduler(appier.Scheduler):

    def __init__(
        self,
        owner,
        order_timeout = ORDER_TIMEOUT,
        warning_timeout = WARNING_TIMEOUT,
        *args,
        **kwargs
    ):
        appier.Scheduler.__init__(
            self,
            owner,
            timeout = LOOP_TIMEOUT,
            *args,
            **kwargs
        )
        self.order_timeout = order_timeout
        self.warning_timeout = warning_timeout

    def tick(self):
        appier.Scheduler.tick(self)
        self.logger.debug("Start of tick operation ...")
        self.check_orders()
        self.cancel_orders()
        self.warn_orders()
        self.issue_references()
        self.note_references()
        self.email_references()
        self.logger.debug("Ended tick operation")

    def load(self):
        appier.Scheduler.load(self)
        self.load_shopify()
        self.load_easypay()

    def load_shopify(self):
        self.shopify = shopify.Api(
            api_key = appier.conf("SHOPIFY_API_KEY"),
            password = appier.conf("SHOPIFY_PASSWORD"),
            secret = appier.conf("SHOPIFY_SECRET"),
            store_url = appier.conf("SHOPIFY_STORE")
        )

    def load_easypay(self):
        self.easypay = easypay.ShelveApi(
            production = appier.conf("EASYPAY_PRODUCTION", cast = bool),
            username = appier.conf("EASYPAY_USERNAME"),
            password = appier.conf("EASYPAY_PASSWORD"),
            cin = appier.conf("EASYPAY_CIN"),
            entity = appier.conf("EASYPAY_ENTITY")
        )
        self.easypay.bind("paid", self.on_paid)
        self.easypay.start_scheduler()

    def check_orders(self):
        self.logger.debug("Checking shopify orders ...")
        orders = self.shopify.list_orders(limit = 30)
        new_orders = []
        for order in orders:
            _order = shopdesk.Order.get(s_id = order["id"], raise_e = False)
            if _order: continue
            new_orders.append(order)
        self.logger.debug("Found '%d' new shopify orders", len(new_orders))
        for order in new_orders:
            order_id = order["id"]
            transactions = self.shopify.transactions_order(order_id)
            _order = shopdesk.Order.from_shopify(order, transactions = transactions)
            _order.save()

    def cancel_orders(self):
        expiration = time.time() - self.order_timeout
        orders = shopdesk.Order.find(
            payment = shopdesk.Order.ISSUED,
            created = {
                "$lt" : expiration
            }
        )
        self.logger.debug("Canceling '%d' outdated orders ..." % len(orders))
        for order in orders: order.cancel_s(self.easypay, self.shopify)

    def warn_orders(self):
        warning = time.time() - self.warning_timeout
        orders = shopdesk.Order.find(
            payment = shopdesk.Order.ISSUED,
            warning_sent = False,
            created = {
                "$lt" : warning
            }
        )
        self.logger.debug("Warning '%d' unpaid orders ..." % len(orders))
        for order in orders: order.email_warning_s()

    def issue_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.PENDING)
        self.logger.debug("Issuing references for '%d' orders ..." % len(orders))
        for order in orders: order.issue_reference_s(self.easypay)

    def note_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.ISSUED, note_sent = False)
        self.logger.debug("Noting down '%d' orders ..." % len(orders))
        for order in orders: order.note_reference_s(self.shopify)

    def email_references(self):
        orders = shopdesk.Order.find(payment = shopdesk.Order.ISSUED, email_sent = False)
        self.logger.debug("Sending emails for '%d' orders ..." % len(orders))
        for order in orders: order.email_reference_s()

    def on_paid(self, reference, details):
        identifier = reference["identifier"]
        order = shopdesk.Order.get(reference_id = identifier, raise_e = False)
        order.pay_s(self.shopify)
