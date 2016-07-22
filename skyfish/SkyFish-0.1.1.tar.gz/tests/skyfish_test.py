import unittest
from mocks import RequestMock
from mocks import requests

from skyfish import SkyFishSDK


class SkyFishSDKTest(unittest.TestCase):

    def test_initialization(self):
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        self.assertIsInstance(
            sky, SkyFishSDK)
        self.assertEqual(
            sky.email, 'somerandomemail@somerandomemail.com')
        self.assertEqual(
            sky.passport_id, 'somepassportid')
        self.assertEqual(
            sky.password, 'somepassword')
        self.assertIsInstance(
            sky.request_module, RequestMock)
        self.assertFalse(sky.is_production)
        self.assertEqual(
            sky.base_product_url, 'https://product-stg.coralshop.top')
        self.assertEqual(
            sky.base_auth_url, 'https://bluefin-stg.coralshop.top')

    def test_initialization_email_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email=None,
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

    def test_initialization_passport_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id=None,
                password='somepassword',
                request_module=requests)

    def test_initialization_password_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password=None,
                request_module=requests)

    def test_initialization_request_module_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=None)

    def test__generate_product_headers(self):
        expected_keys = ['Content-Type',
                         'Accept',
                         'X-Passport-ID',
                         'X-Passport-Email']
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        headers = sky._generate_product_headers()
        for header in headers.keys():
            self.assertIn(header, expected_keys)
            self.assertIsInstance(headers.get(header), str)

    def test__generate_normal_headers(self):
        expected_keys = ['Content-Type']
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        headers = sky._generate_normal_headers()
        for header in headers.keys():
            print "header is " + header
            self.assertIn(header, expected_keys)
            self.assertIsInstance(headers.get(header), str)

    def test__get_token(self):
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        token = sky._get_token()
        self.assertIsNotNone(token)
        self.assertEqual(len(token), 108)

    def test__do_login(self):
        expected_jsend = ['status', 'message', 'data']
        expected_core = ['token', 'email']
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        login_data = sky._do_login()
        self.assertIsInstance(login_data, dict)
        for key in login_data.keys():
            self.assertIn(key, expected_jsend)

        core_data = login_data.get('data')
        self.assertIsInstance(core_data, dict)

        for key in core_data.keys():
            self.assertIn(key, expected_core)

        self.assertEqual(
            core_data.get('email'),
            'somerandomemail@somerandomemail.com')

    def test_create_product(self):
        product_info = dict(
            name='A test product',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BANK_TRANSFER', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        new_product = sky.create_product(
                        sku='1234',
                        product_details=product_info)
        self.assertIsNotNone(new_product)
        self.assertEqual(new_product.get('status'), 'success')

    def test_get_product_success(self):
        expected_root = ['status', 'data']
        expected_product = ['id',
                            'limitless',
                            'price',
                            'quantity',
                            'need_address',
                            'name',
                            'sku',
                            'weight',
                            'description',
                            'merchant_id',
                            'payment_types',
                            'image_url',
                            'discount',
                            'insurance_type',
                            'product_variant',
                            'environment_type',
                            'short_url'
                           ]
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)
        raw_product = sky.get_product(sku='1234')
        self.assertIsNotNone(raw_product)

        for key in raw_product.keys():
            self.assertIn(key, expected_root)

        product = raw_product.get('data')

        for key in product.keys():
            self.assertIn(key, expected_product)

    def test_get_product_not_found(self):
        expected_root = ['status', 'message']

        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        raw_product = sky.get_product(sku='4321')

        for key in raw_product.keys():
            self.assertIn(key, expected_root)

        self.assertEqual(
            raw_product.get('message'),
            'ProductNotAvailableException')

    def test_update_product_success(self):
        expected_root = ['status', 'data']
        expected_product = ['id',
                            'limitless',
                            'price',
                            'quantity',
                            'need_address',
                            'name',
                            'sku',
                            'weight',
                            'description',
                            'merchant_id',
                            'payment_types',
                            'image_url',
                            'discount',
                            'insurance_type',
                            'product_variant',
                            'environment_type',
                            'short_url'
                           ]
        product_info = dict(
            name='An updated test product',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BANK_TRANSFER', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        updated_product = sky.update_product(
                    sku='1234',
                    product_details=product_info)
        self.assertIsNotNone(updated_product)

        for key in updated_product.keys():
            self.assertIn(key, expected_root)

        product = updated_product.get('data')

        for key in product.keys():
            self.assertIn(key, expected_product)

    def test_update_product_not_found(self):
        expected_root = ['status', 'message']
        product_info = dict(
            name='An updated test product',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BANK_TRANSFER', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        updated_product = sky.update_product(
                    sku='4321',
                    product_details=product_info)
        self.assertIsNotNone(updated_product)

        for key in updated_product.keys():
            self.assertIn(key, expected_root)

        self.assertEqual(
            updated_product.get('message'),
            'ProductNotAvailableException')

    def test_delete_product_success(self):

        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        product = sky.delete_product(sku='1234')
        self.assertIsNotNone(product)
        self.assertEqual(
            product.get('status'),
            'success')

    def test_delete_product_not_found(self):
        expected_root = ['status', 'message']

        sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                password='somepassword',
                request_module=requests)

        raw_product = sky.delete_product(sku='4321')

        for key in raw_product.keys():
            self.assertIn(key, expected_root)

        self.assertEqual(
            raw_product.get('message'),
            'ProductNotAvailableException')
