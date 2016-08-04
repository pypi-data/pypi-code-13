import unittest
from mocks import RequestMock
from mocks import requests

from skyfish import SkyFishSDK


class SkyFishSDKTest(unittest.TestCase):

    def test_initialization(self):
        sky = SkyFishSDK(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            request_module=requests)
        self.assertIsInstance(
            sky, SkyFishSDK)
        self.assertEqual(
            sky.email, 'somerandomemail@somerandomemail.com')
        self.assertEqual(
            sky.passport_id, 'somepassportid')
        self.assertEqual(
            sky.token, 'ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=')
        self.assertIsInstance(
            sky.request_module, RequestMock)
        self.assertEqual(
            sky.client_key, 'aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla')
        self.assertFalse(sky.is_production)
        self.assertEqual(
            sky.base_product_url, 'https://product-stg.coralshop.top')

    def test_initialization_email_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email=None,
                passport_id='somepassportid',
                token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
                client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
                request_module=requests)

    def test_initialization_passport_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id=None,
                token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
                client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
                request_module=requests)

    def test_initialization_token_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                token=None,
                client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
                request_module=requests)

    def test_initialization_request_module_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
                client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
                request_module=None)

    def test_initialization_client_key_error(self):
        with self.assertRaises(Exception):
            sky = SkyFishSDK(
                email='somerandomemail@somerandomemail.com',
                passport_id='somepassportid',
                token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
                client_key=None,
                request_module=requests)

    def test__generate_product_headers(self):
        expected_keys = ['Content-Type',
                         'Accept',
                         'X-Passport-ID',
                         'X-Passport-Email']
        sky = SkyFishSDK(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            request_module=requests)
        headers = sky._generate_product_headers()
        for header in headers.keys():
            self.assertIn(header, expected_keys)
            self.assertIsInstance(headers.get(header), str)

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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
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
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            request_module=requests)

        raw_product = sky.delete_product(sku='4321')

        for key in raw_product.keys():
            self.assertIn(key, expected_root)

        self.assertEqual(
            raw_product.get('message'),
            'ProductNotAvailableException')
