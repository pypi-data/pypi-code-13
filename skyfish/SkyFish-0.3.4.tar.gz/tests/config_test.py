import unittest
from skyfish.models import Config

class ConfigTest(unittest.TestCase):

    def test_initialize(self):

        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        config = Config(config_dict)

        self.assertIsInstance(config, Config)

    def test_initialize_not_dict(self):
        config_dict = "config"

        with self.assertRaises(TypeError):
            config = Config(config_dict)

    def test_initialize_email_not_exist(self):
        config_dict = dict(
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(AttributeError):
            config = Config(config_dict)

    def test_initialize_email_wrong_type(self):
        config_dict = dict(
            email=1,
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(TypeError):
            config = Config(config_dict)

    def test_initialize_passport_not_exist(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(AttributeError):
            config = Config(config_dict)

    def test_initialize_passport_wrong_type(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id=1,
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(TypeError):
            config = Config(config_dict)

    def test_initialize_token_not_exist(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(AttributeError):
            config = Config(config_dict)

    def test_initialize_token_wrong_type(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token=1,
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(TypeError):
            config = Config(config_dict)

    def test_initialize_client_key_not_exist(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(AttributeError):
            config = Config(config_dict)

    def test_initialize_client_key_wrong_type(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key=1,
            base_url='https://product-sandbox.skyfish.id')

        with self.assertRaises(TypeError):
            config = Config(config_dict)

    def test_initialize_base_url_not_exist(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla')

        with self.assertRaises(AttributeError):
            config = Config(config_dict)

    def test_initialize_base_url_wrong_type(self):
        config_dict = dict(
            email='somerandomemail@somerandomemail.com',
            passport_id='somepassportid',
            token='ZU9YYUxsQUQ1RWpjd1RYdk9HSTFaVFJsTkdFdFl6SXdZUzAwWW1ZeExXSmhNRE10TlRkbVltUmxNak0zWTJNdzUyNTZ5NWxlcGt0NTQ1Zm8=',
            client_key='aalkdalkdnalkdnlakndlakdnlakdnlakndlakndlkanldkanldknakla',
            base_url=1)

        with self.assertRaises(TypeError):
            config = Config(config_dict)
