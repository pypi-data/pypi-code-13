import json

class SkyFishSDK(object):
    base_staging_product_url = 'https://product-stg.coralshop.top'
    base_production_product_url = 'https://product.skyfish.id'
    base_staging_auth_url = 'https://bluefin-stg.coralshop.top'
    base_production_auth_url = 'https://bluefin.skyfish.id'

    def __init__(
        self,
        email,
        passport_id,
        password,
        request_module,
        is_production=False):
        if not email:
            raise Exception('`email` parameter is required')
        self.email = email

        if not passport_id:
            raise Exception('`passport_id` parameter is required')
        self.passport_id = passport_id

        if not password:
            raise Exception('`password` parameter is required')
        self.password = password

        self.is_production=is_production
        self.base_product_url = self.base_staging_product_url
        self.base_auth_url = self.base_staging_auth_url

        if self.is_production:
            self.base_product_url = self.base_production_product_url
            self.base_auth_url = self.base_production_auth_url

        if not request_module:
            raise Exception('`request_module` parameter is required')
        self.request_module = request_module

    def _generate_product_headers(self):
        return {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-Passport-ID': self.passport_id,
                    'X-Passport-Email': self.email}

    def _generate_normal_headers(self):
        return {'Content-Type': 'application/json'}

    def _get_token(self):
        login_data = self._do_login()
        return login_data.get('data').get('token')

    def _do_login(self):
        login = self.request_module.post(
                    self.base_auth_url + '/v1/merchant/login',
                    headers=self._generate_normal_headers(),
                    data=dict(
                        email=self.email,
                        password=self.password,
                        passport=self.passport_id
                    ))
        return login.json()

    def create_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s' % (
            self.base_product_url, sku, self._get_token())
        new_product = self.request_module.post(
                        url,
                        headers=self._generate_product_headers(),
                        data=product_details)
        return new_product.json()

    def get_product(self, sku):
        url = '%s/v1/products/%s?token=%s' % (
            self.base_product_url, sku, self._get_token())
        product = self.request_module.get(
                    url,
                    headers=self._generate_product_headers())
        return product.json()

    def update_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s' % (
            self.base_product_url, sku, self._get_token())
        updated_product = self.request_module.put(
                    url,
                    headers=self._generate_product_headers,
                    data=product_details)
        return updated_product.json()

    def delete_product(self, sku):
        url = '%s/v1/products/%s?token=%s' % (
            self.base_product_url, sku, self._get_token())
        product = self.request_module.delete(
                    url,
                    headers=self._generate_product_headers())
        return product.json()
