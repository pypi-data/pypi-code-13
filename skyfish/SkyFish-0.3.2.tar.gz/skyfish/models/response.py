# -*- coding: utf-8 -*-
"""
    Response
    ~~~~~~~~

    Response modelling for CRUD used within skyfish

    :copyright: (c) 2016 by PT Koneksi Integrasi.
    :license: MIT, see LICENSE for more details.
"""

from skyfish.models import ProductData

__version__ = '0.1.0'

class Response(object):
    status_code = None
    status = None
    message = None
    data = None

    def __init__(self, json_dictionary=None, status_code=None, status=None, message=None):
        if json_dictionary:
            self.data = Response.build_from_json(json_dictionary)

        if status_code:
            self.status_code = status_code

        if status:
            self.status = status

        if message:
            self.message = message

    @staticmethod
    def build_from_json(json_dictionary=None):
        if not json_dictionary:
            raise ValueError('`json_dictionary` should not be empty')
        if not type(json_dictionary) is dict:
            raise TypeError('`json_dictionary` should be dict')
        product = ProductData(json_dictionary)
        return product
