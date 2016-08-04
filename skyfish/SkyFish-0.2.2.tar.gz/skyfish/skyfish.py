# -*- coding: utf-8 -*-
"""
    Skyfish
    ~~~~~

    Official python SDK for skyfish chat to buy inventory integration

    :copyright: (c) 2016 by PT Koneksi Integrasi.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.2.2'

import json


class SkyFishSDK(object):
    base_staging_product_url = 'https://product-stg.coralshop.top'
    base_production_product_url = 'https://product.skyfish.id'

    def __init__(
            self,
            email,
            passport_id,
            token,
            client_key,
            request_module,
            is_production=False):
        
        if not email:
            raise Exception('`email` parameter is required')
        self.email = email

        if not passport_id:
            raise Exception('`passport_id` parameter is required')
        self.passport_id = passport_id

        if not token:
            raise Exception('`token` parameter is required')
        self.token = token

        if not client_key:
            raise Exception('`client_key` parameter is required')
        self.client_key = client_key

        self.is_production = is_production
        self.base_product_url = self.base_staging_product_url

        if self.is_production:
            self.base_product_url = self.base_production_product_url

        if not request_module:
            raise Exception('`request_module` parameter is required')
        self.request_module = request_module

    def _generate_product_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Passport-ID': self.passport_id,
            'X-Passport-Email': self.email}

    def create_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
            self.base_product_url, sku, self.token, self.client_key)
        
        new_product = self.request_module.post(
            url,
            headers=self._generate_product_headers(),
            json=product_details)
        
        return new_product.json()

    def get_product(self, sku):
        url = '%s/v1/products/%s/merchant?token=%s' % (
            self.base_product_url, sku, self.token)
        
        product = self.request_module.get(
            url,
            headers=self._generate_product_headers())
        return product.json()

    def update_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
            self.base_product_url, sku, self.token, self.client_key)
        
        updated_product = self.request_module.put(
            url,
            headers=self._generate_product_headers,
            json=product_details)
        
        return updated_product.json()

    def delete_product(self, sku):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
            self.base_product_url, sku, self.token, self.client_key)
        
        product = self.request_module.delete(
            url,
            headers=self._generate_product_headers())
        
        return product.json()
