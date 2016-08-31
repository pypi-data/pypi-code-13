"""
Perform integration tests of our Stripe billing extensions.
"""
from google.appengine.ext import ndb

from webapptitude import testkit
from webapptitude import billing

import time
import random
import contextlib


class BillingTest(testkit.TestCase):

    @classmethod
    def generate_test_id(cls, prefix):
        return '%s%d' % (prefix, random.randint(1E3, 1E7))

    @classmethod
    def setUpClass(cls):
        super(BillingTest, cls).setUpClass()
        cls.test_plan_creation = int(time.time())
        cls.test_plan_id = cls.generate_test_id('test_plan_')
        cls.test_plan_filter = dict(gt=cls.test_plan_creation)
        billing.setupStripe("sk_test_BQokikJOvBiI2HlWgH4olfQ2", '2016-07-06')

    @property
    def cache_http(self):
        return billing.stripe.default_http_client

    @contextlib.contextmanager
    def prepare_test_environ(self, plan=True, customer=True):
        plan = billing.Plan.create(
            amount=2000,
            interval="month",
            name="Amazing Gold Plan",
            currency="usd",
            id=self.test_plan_id
        )

        cust = billing.CustomerModel.create(
            "Joe Customer",
            "joe+customer@gmail.com",
            "425-867-5309",
            plan.id,
            source=dict(
                object="card",
                number='4242424242424242',
                exp_month=11,
                exp_year=2052,
                cvc=111
            )
        )

        try:
            yield plan, cust
        finally:
            # cust.delete()
            # plan.delete()
            pass

    @testkit.debug_on(AssertionError)
    def test_verify_customer_plan(self):
        with self.prepare_test_environ() as (plan, cust):
            self.assertIsInstance(cust, ndb.Model)

            plans = billing.Plan.all()
            self.assertIn(plan, plans)

            index = -1
            for i, p in enumerate(plans):
                if p.id == plan.id:
                    index = i
                    break

            self.assertEqual(plans[i].price, 20.00)
            self.assertSequenceEqual(plans[i].billing_interval, ('month', 1))

            plans[i].save(amount=2195)
            self.assertEqual(plans[i].price, 21.95)

            cust_plans = cust.plans
            self.assertEqual(cust_plans[0].id, plans[i].id)
