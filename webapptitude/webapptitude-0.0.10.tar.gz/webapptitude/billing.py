"""
Billing features via Stripe.

Useful classes:
    - CustomerModel(ndb.Model)
    - Plan(stripe.Plan)

Useful methods:
    - setupStripe(api_secret=None, api_version=None)

This module implements an HTTP caching layer for Stripe, so that applications
can rely on Stripe's data model to deliver relevant data to web users (e.g.
a pricing page).

It's recommended to use the setupStripe method, which:
    - Accepts API key and API version as environment variables.
    - Integrates the HTTP cache

The CustomerModel provides basic coordination between datastore and Stripe
operations, e.g. creating the customer records with a subscription.


"""

import stripe
import hashlib
import os
import re
import urlparse
import logging

# from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.api import lib_config

from httpclient import MemcacheProxy


_config = lib_config.register('billing', dict(
    stripe_secret_key="MISSING_SECRET",
    stripe_api_version="2016-03-07"
))


def md5(*text):
    checksum = hashlib.md5(text[0])
    for t in text[1:]:
        checksum.update(t)
    return checksum.hexdigest()


def setupStripe(api_secret=None, api_version=None):  # noqa
    """Prepare the Stripe configuration."""
    if api_secret is None:
        api_secret = _config.stripe_secret_key
        api_secret = os.environ.get('STRIPE_SECRET_KEY', api_secret)
    if api_version is None:
        api_version = _config.stripe_api_version
        api_version = os.environ.get('STRIPE_API_VERSION', api_version)

    httpopts = dict(verify_ssl_certs=stripe.verify_ssl_certs)

    stripe.api_version = api_version
    stripe.api_key = api_secret
    stripe.default_http_client = URLFetchCache(**httpopts)


class URLFetchCache(stripe.http_client.UrlFetchClient):
    """A thin caching interface over the Stripe HTTP client implementation."""

    default_lifetime = 1800
    debug = int(os.environ.get('DEBUG', '0'))

    cacherules = [  # pairs regex to cache duration (seconds)
        (r'^/v1/customers/[a-z0-9_]+', (5 * 60)),
        (r'^/v1/subscriptions/[a-z0-9_]+', (5 * 60)),
        (r'^/v1/subscriptions$', (5 * 60)),
        (r'^/v1/plans/[a-z0-9_]+', (5 * 60)),
        (r'^/v1/plans$', (5 * 60))
    ]

    def __init__(self, *args, **kwargs):
        """Prepare the HTTP client with cache configuration."""
        self.cache = MemcacheProxy(namespace='stripe#',
                                   lifetime=self.default_lifetime)
        super(URLFetchCache, self).__init__(*args, **kwargs)

    @classmethod
    def calculate_cache_key(cls, method, url, headers):
        """Build the cache key from request and headers."""
        header_checksum = ['%s:%r' % (k, v) for (k, v) in headers.items()]
        header_checksum = md5(*header_checksum)
        return '%s;%s;%s' % (method, url, header_checksum)

    @classmethod
    def get_cache_lifetime(cls, url):
        """Produce a cache time based on URL matchin rules, or default."""
        path = urlparse.urlsplit(url).path
        for pattern, lifetime in cls.cacherules:
            if re.match(pattern, path):
                return lifetime
        return cls.default_lifetime

    def request(self, method, url, headers, post_data=None):
        """
        Execute the HTTP request.

        This method is required by Stripe's HTTP client API contract.
        """
        is_cacheable = (method.upper() in ('GET', 'HEAD'))
        is_cacheable = (post_data is None) and is_cacheable
        lifetime = self.get_cache_lifetime(url)
        _super = super(URLFetchCache, self)

        if is_cacheable and (lifetime > 0):
            if self.debug:
                info = (method, url, headers)
                logging.info('Cache key calculating: %r' % (info,))
            cachekey = self.calculate_cache_key(method, url, headers)
            if self.debug:
                logging.info('Checking cache for key: %r' % (cachekey))
            cacheval = self.cache.get(cachekey)  # Fetch from cache

            if cacheval is None:  # Not found in cache
                if self.debug:
                    logging.info('Cache key not found: %r' % (cachekey))
                cacheval = _super.request(method, url, headers,
                                          post_data=post_data)
                self.cache.set(cachekey, cacheval, time=lifetime)  # populate

            return cacheval

        else:
            # NOTE: we delete non-cacheable entries from cache
            # This enables updates to be reflected near real-time.
            if self.debug and (method.upper() in ('GET', 'HEAD')):
                info = (lifetime, method, url, post_data)
                logging.info('Caching not applied: %r' % (info,))
            cachekey = self.calculate_cache_key(method, url, headers)
            self.cache.delete(cachekey)
            return _super.request(method, url, headers, post_data=post_data)


def getSubscriptionsByPlanId(planId, created=None):
    for s in stripe.Subscription.all(plan=planId).auto_paging_iter():
        yield stripe.Customer.retrieve(s.customer), s


def deleteSubscriptionsByPlanId(planId, **kwargs):
    for cust, subs in getSubscriptionsByPlanId(planId, **kwargs):
        yield cust, subs.delete()


def getSubscriptionsByCustomerId(customerId, limit=100):
    return stripe.Customer.retrieve(customerId).subscriptions.all(limit=limit)


class Plan(stripe.Plan):

    # These attributes cannot be updated once the plan is created.
    # Altering them will require creating a new Plan entry and rolling existing
    # customers onto the new one. By default this will calculate prorated price
    # effects as needed.
    fixed_attrs = ('id', 'name', 'amount', 'interval', 'interval_count',
                   'currency', 'trial_period_days', 'statement_descriptor')

    integer_attribs = ('interval_count', 'trial_period_days')
    currency_attribs = ('amount',)

    @classmethod
    def augment(cls, planInstance):
        assert isinstance(planInstance, stripe.Plan)
        planInstance.__class__ = cls
        return planInstance

    @classmethod
    def all(cls, limit=300):
        return [cls.augment(p) for p in stripe.Plan.all(limit=limit)]

    @property
    def price(self):
        """Calculate the plan price as a floating point value."""
        return float(self.amount) / float(100)

    @property
    def billing_interval(self):
        # e.g. interval=month, interval_count=3 means "billed every 3 months"
        return (self.interval, self.interval_count)

    @classmethod
    def replace_subscriptions(cls, plan_old, plan_new):
        """Switch all subscriptions on an old plan to a new plan."""
        for cust, subs in getSubscriptionsByPlanId(plan_old):
            subs.plan = plan_new
            subs.save()

    def save(self, **props):
        """
        Modify a plan, replacing the old entry if needed.

        Automates the process of replacing plan entries when fixed properties
        are modified. Stripe doesn't allow (eg) the price of a plan to change.

        This function accepts properties (e.g. id=newPlanId) as keyword
        arguments, which override the state of the current plan.
        """
        needs_recreate = False
        for k, v in props.iteritems():
            if k in self.fixed_attrs:
                needs_recreate = True

        if needs_recreate:
            old_id = self.id

            for k in self.fixed_attrs:
                if k not in props:  # retain current state where not overriden
                    props[k] = getattr(self, k, None)

                setattr(self, k, props[k])  # adopt the aggregate state

            for k in ('metadata',):  # inherit these properties directly
                props[k] = getattr(self, k, None)

            stripe.Plan(old_id).delete()  # this flags old plan as deleted
            ret = Plan.augment(Plan.create(**props))  # prepare a new plan

            # update related subscriptions
            self.replace_subscriptions(old_id, ret.id)

            return ret  # the new plan
        else:
            return super(Plan, self).save()


class CustomerModel(ndb.Model):
    """Coordinate operations on Customers across Stripe and NDB."""

    name = ndb.StringProperty(required=True, indexed=True)
    contact_phone = ndb.StringProperty(required=True, indexed=True)
    contact_email = ndb.StringProperty(required=True, indexed=True)
    stripe_id = ndb.StringProperty(required=True, indexed=True)

    @classmethod
    def deleteCustomersByEmailAddress(cls, emailAddress):
        query = cls.query(cls.contact_email == emailAddress)
        # This is going to be slow. TODO: be faster w/ keys.
        for cust in query:
            cust.delete()

        # keys = query.fetch(keys_only=True)
        # ndb.delete_multi(keys)
        # TODO: delete from Stripe

    @classmethod
    def create(cls, name, email, phone, plan=None, **props):
        """Construct a Stripe customer and link the NDB instance."""
        payment_source = props.pop('source', None)
        stripe_cust = None
        try:
            stripe_cust = stripe.Customer.create(
                email=email,
                plan=plan,
                source=payment_source,
                metadata={'phone_number': phone},
                description="%s <%s>" % (name, phone)
            )
            instance = cls(
                name=name, contact_email=email, contact_phone=phone,
                stripe_id=stripe_cust.id
            )
            instance.put()
            return instance
        except Exception, e:
            if (stripe_cust and stripe_cust.id):
                stripe_cust.delete()
            raise e

    def delete(self):
        """Remove the Stripe customer and NDB instance."""
        try:
            cust = stripe.Customer.retrieve(self.stripe_id)
            if cust is not None:
                cust.delete()
        finally:
            self.key.delete()

    def subscribe(self, plan_id, **props):
        """Establish a new subscription."""
        return stripe.Subscription.create(
            customer=self.stripe_id,
            plan=plan_id,
            **props
        )

    def unsubscribe(self, plan_id, at_period_end=True):
        """Remove an existing subscription."""
        for sub in self.subscriptions:
            if sub.get('plan').get('id') == plan_id:
                sub.delete(at_period_end=at_period_end)

    def change_plan(self, plan_old, plan_new, prorate=True):
        """Replace a plan on matching subscriptions."""
        for sub in self.subscriptions:
            if sub.get('plan').get('id') == plan_old:
                sub.plan = plan_new
                sub.prorate = prorate
                sub.save()

    @property
    def stripe(self):
        return stripe.Customer.retrieve(self.stripe_id)

    @property
    def subscriptions(self):
        """Fetch all subscriptions associated with this customer."""
        return self.stripe.subscriptions.auto_paging_iter()

    @property
    def plans(self):
        """All plans related to this customer's subscriptions."""
        return [Plan.augment(s.plan) for s in self.subscriptions]


# compatibility
deleteCustomersByEmailAddress = CustomerModel.deleteCustomersByEmailAddress
