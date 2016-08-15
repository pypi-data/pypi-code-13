# -*- coding: utf-8 -*-
"""
    Config
    ~~~~~~~~~~~

    Data modelling for skyfish configuration

    :copyright: (c) 2016 by PT Koneksi Integrasi.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1.0'

class Config(object):
    email=None
    passport_id=None
    token=None
    client_key=None
    base_url=None

    def __init__(self, config_dictionary):

        if not type(config_dictionary) is dict:
            raise TypeError('`config_dictionary` should be a dictionary')

        for key, value in config_dictionary.items():
            if hasattr(self, key):
                setattr(self, key, value)

        if not self.email:
            raise AttributeError('`email` property is required')

        if not type(self.email) is str:
            raise TypeError('`email` property should be str')

        if not self.passport_id:
            raise AttributeError('`passport_id` property is required')

        if not type(self.passport_id) is str:
            raise TypeError('`passport_id` property should be str')

        if not self.token:
            raise AttributeError('`token` property is required')

        if not type(self.token) is str:
            raise TypeError('`token` property should be str')

        if not self.client_key:
            raise AttributeError('`client_key` property is required')

        if not type(self.client_key) is str:
            raise TypeError('`client_key` property should be str')

        if not self.base_url:
            raise AttributeError('`base_url` property is required')

        if not type(self.base_url) is str:
            raise TypeError('`base_url` property should be str')
