# -*- coding: utf-8 -*-
"""
    ProductData
    ~~~~~~~~~~~

    Data modelling for product data used within skyfish

    :copyright: (c) 2016 by PT Koneksi Integrasi.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1.0'

class ProductData(object):
    id=None
    limitless=None
    price=None
    quantity=None
    need_address=None
    name=None
    sku=None
    weight=None
    description=None
    merchant_id=None
    payment_types=None
    image_url=None
    discount=None
    insurance_type=None
    product_variant=None
    environment_type=None

    def __init__(self, json_dictionary):
        if not type(json_dictionary) is dict:
            raise TypeError('`json_dictionary` should be a dictionary')

        for key, value in json_dictionary.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if not type(self.limitless) is bool:
            raise TypeError('`limitless` property should be bool')

        if not self.price:
            raise AttributeError('`price` property is required')

        if not type(self.price) is int and not type(self.price) is long:
            raise TypeError('`price` property should either be long or int')

        if not self.quantity:
            raise AttributeError('`quantity` property is required')

        if not type(self.quantity) is int:
            raise TypeError('`quantity` property should be int')

        if not type(self.need_address) is bool:
            raise TypeError('`need_address` property should be bool')

        if not self.name:
            raise AttributeError('`name` property is required')

        if not type(self.name) is str and not type(self.name) is unicode:
            raise TypeError('`name` property should be either str or unicode')

        if not self.sku:
            raise AttributeError('`sku` property is required')

        if not type(self.sku) is str and not type(self.sku) is unicode:
            raise TypeError('`sku` property should be str or unicode')

        if not self.weight:
            raise AttributeError('`weight` property is required')

        if not type(self.weight) is int:
            raise TypeError('`weight` property should be int')

        if self.description is None:
            raise AttributeError('`description` property is required')

        if not type(self.description) is str and not type(self.description) is unicode:
            raise TypeError('`description` property should either be str or unicode ')

        if not self.payment_types:
            raise AttributeError('`payment_types` property is required')

        if not type(self.payment_types) is list:
            raise TypeError('`sku` property should be list')

        expected_payment_types = ["BANK_TRANSFER","CREDIT_CARD","PERMATA","BCA","ECHANNEL"]

        for item in self.payment_types:
            if not type(item) is str and not type(item) is unicode:
                raise TypeError('payment type should be str or unicode')

            if item not in expected_payment_types:
                raise ValueError('Payment types shoud be in `BANK_TRANSFER`,`CREDIT_CARD`,`PERMATA`,`BCA`,`ECHANNEL`')

        if not self.image_url:
            raise AttributeError('`image_url` property is required')

        if not type(self.image_url) is list:
            raise TypeError('`image_url` property should be list')

        for item in self.image_url:
            if not type(item) is str and not type(item) is unicode:
                raise TypeError('image url location should be str or unicode')

        if not self.discount:
            raise AttributeError('`discount` property is required')

        if not type(self.discount) is dict:
            raise TypeError('`discount` property should be dict')

        expected_discount_keys = ['discount_type','amount']
        expected_discount_types = ['NOMINAL', 'PERCENTAGE']

        for item in self.discount.keys():
            if item not in expected_discount_keys:
                raise AttributeError('`%s` is not a part of discount dictionary' % (item))

        if self.discount.get('discount_type') not in expected_discount_types:
            raise ValueError('Discount types are `NOMINAL` and `PERCENTAGE`')

        if not self.insurance_type:
            raise AttributeError('`insurance_type` property is required')

        if not type(self.insurance_type) is str and not type(item) is unicode:
            raise TypeError('`insurance_type` property should be str or unicode')

        expected_insurance_type = ['NEEDED','NOT_NEEDED']

        if self.insurance_type not in expected_insurance_type:
            raise ValueError('Insurance types are `NEEDED` and `NOT_NEEDED`')

        if not type(self.product_variant) is dict:
            raise TypeError('`product_variant` property should be dict')

        if not self.environment_type:
            raise AttributeError('`environment_type` property is required')

        if not type(self.environment_type) is str and not type(item) is unicode:
            raise TypeError('`environment_type` property should be str or unicode')

        expected_environment_types = ['HIDDEN', 'DEVELOPMENT', 'PRODUCTION']

        if self.environment_type not in expected_environment_types:
            raise ValueError('Environment types are `HIDDEN`, `DEVELOPMENT`, `PRODUCTION`')

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            limitless=self.limitless,
            price=self.price,
            quantity=self.quantity,
            need_address=self.need_address,
            image_url=self.image_url,
            description=self.description,
            environment_type=self.environment_type,
            weight=self.weight,
            insurance_type=self.insurance_type,
            payment_types=self.payment_types,
            sku=self.sku,
            discount=self.discount,
            product_variant=self.product_variant
        )

