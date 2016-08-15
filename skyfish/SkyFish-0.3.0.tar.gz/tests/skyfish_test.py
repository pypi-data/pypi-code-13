import unittest
from mocks import RequestMock
from mocks import requests

from skyfish import SkyFishSDK
from skyfish.models import Config


class SkyFishSDKTest(unittest.TestCase):

    def test_initialization(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

        self.assertIsInstance(
            sky, SkyFishSDK)

        self.assertIsInstance(
            sky.config, Config)

        self.assertEqual(
            sky.config.email, 'somerandomemail@somerandomemail.com')

        self.assertEqual(
            sky.config.passport_id, 'somepassportid')

        self.assertEqual(
            sky.config.token, 'ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=')

        self.assertEqual(
            sky.config.client_key, 'aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla')

        self.assertEqual(
            sky.config.base_url, 'https://product-sandbox.skyfish.id')

    def test_initialization_config_error(self):
        config='config'
        with self.assertRaises(TypeError):
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test_configuration_parameter_error(self):
        with self.assertRaises(AttributeError):
            sky = SkyFishSDK(configuration=None, request_module=requests)

    def test_initialization_email_error(self):
        config_dict = dict(
            email=None,
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id'
        )
        with self.assertRaises(AttributeError):
            config=Config(config_dict)
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test_initialization_passport_error(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id=None,
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id'
        )
        with self.assertRaises(AttributeError):
            config=Config(config_dict)
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test_initialization_token_error(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='sompassportid',
            token=None,
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id'
        )

        with self.assertRaises(AttributeError):
            config=Config(config_dict)
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test_initialization_client_key_error(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key=None,
            base_url='https://product-sandbox.skyfish.id',
        )

        with self.assertRaises(AttributeError):
            config=Config(config_dict)
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test_initialization_base_url_error(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url=None,
        )

        with self.assertRaises(AttributeError):
            config=Config(config_dict)
            sky = SkyFishSDK(
                    configuration=config,
                    request_module=requests)

    def test__generate_product_headers(self):
        expected_keys = [
                         'User-Agent',
                         'Content-Type',
                         'Accept',
                         'X-Passport-ID',
                         'X-Passport-Email']

        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
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

        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        new_product = sky.create_product(
            sku='1234',
            product_details=product_info)
        self.assertIsNotNone(new_product)
        self.assertEqual(new_product.status_code, 201)

    def test_get_product_success(self):
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
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        raw_product = sky.get_product(sku='1234')
        self.assertIsNotNone(raw_product)

        product = raw_product.data.to_dict()

        for key in product.keys():
            self.assertIn(key, expected_product)

    def test_get_product_not_found(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        raw_product = sky.get_product(sku='4321')

        self.assertEqual(
            raw_product.status_code, 404)

    def test_update_product_success(self):
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

        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        updated_product = sky.update_product(
            sku='1234',
            product_details=product_info)
        self.assertIsNotNone(updated_product)

        product = updated_product.data.to_dict()

        for key in product.keys():
            self.assertIn(key, expected_product)

    def test_update_product_not_found(self):
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

        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        updated_product = sky.update_product(
            sku='4321',
            product_details=product_info)
        self.assertIsNotNone(updated_product)

        self.assertEqual(
            updated_product.status_code, 404)

    def test_delete_product_success(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        product = sky.delete_product(sku='1234')
        self.assertIsNotNone(product)
        self.assertEqual(
            product.status_code, 200)

    def test_delete_product_not_found(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        sky = SkyFishSDK(
            configuration=config,
            request_module=requests)

        raw_product = sky.delete_product(sku='4321')

        self.assertEqual(
            raw_product.status_code, 404)

    def test_user_response_valid(self):
        response = dict(
            status='success',
            message='',
            data=dict(
                user_id='122'
            )
        )

        self.assertTrue(SkyFishSDK.user_response_is_valid(response))

    def test_user_response_wrong_type(self):
        response = ["woo","hoo"]
        with self.assertRaises(TypeError):
            SkyFishSDK.user_response_is_valid(response)

    def test_user_response_unexpected_field(self):
        response = dict(
            status='success',
            message='',
            data=dict(
                user_id='122'
            ),
            extra='extra'
        )

        with self.assertRaises(KeyError):
            SkyFishSDK.user_response_is_valid(response)

    def test_user_response_data_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data="data"
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.user_response_is_valid(response)

    def test_user_response_data_user_id_not_exist(self):
        response = dict(
            status='success',
            message='',
            data=dict(
                user=122
            )
        )

        with self.assertRaises(KeyError):
            SkyFishSDK.user_response_is_valid(response)

    def test_user_response_data_user_id_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=dict(
                user_id=122
            )
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.user_response_is_valid(response)

    def test_stock_response_valid(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku="somesku",
                    current_stock=3,
                    is_available=True
                )
            ]
        )

        self.assertTrue(SkyFishSDK.stock_response_is_valid(response))

    def test_stock_response_wrong_type(self):
        response = ["woo","hoo"]
        with self.assertRaises(TypeError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_unexpected_field(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku="somesku",
                    current_stock=3,
                    is_available=True
                )
            ],
            extra='extra'
        )

        with self.assertRaises(KeyError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_data_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=dict(
                    product_sku="somesku",
                    current_stock=3,
                    is_available=True
                )
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_data_item_unexpected_fields(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku="somesku",
                    current_stock=3,
                    is_available=True,
                    extra='extra'
                )
            ]
        )

        with self.assertRaises(KeyError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_data_product_sku_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku=3,
                    current_stock=3,
                    is_available=True                )
            ]
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_data_current_stock_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku='somesku',
                    current_stock='3',
                    is_available=True                )
            ]
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_stock_response_data_is_available_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=[
                dict(
                    product_sku='somesku',
                    current_stock=3,
                    is_available='True'
                )
            ]
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.stock_response_is_valid(response)

    def test_transaction_response_valid(self):
        response = dict(
            status='success',
            message='',
            data=dict()
        )

        self.assertTrue(SkyFishSDK.transaction_response_is_valid(response))

    def test_transaction_response_wrong_type(self):
        response = ["woo","hoo"]
        with self.assertRaises(TypeError):
            SkyFishSDK.transaction_response_is_valid(response)

    def test_transaction_response_unexpected_value(self):
        response = dict(
            status='success',
            message='',
            data=dict(),
            extra='extra'
        )

        with self.assertRaises(KeyError):
            SkyFishSDK.transaction_response_is_valid(response)

    def test_transaction_response_data_wrong_type(self):
        response = dict(
            status='success',
            message='',
            data=list()
        )

        with self.assertRaises(TypeError):
            SkyFishSDK.transaction_response_is_valid(response)

