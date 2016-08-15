import unittest
from skyfish.models import Response
from skyfish.models import ProductData

class ResponseTest(unittest.TestCase):

    def test_initialization(self):
        json_dict = dict(
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

        response = Response(
                    json_dictionary=json_dict,
                    status_code=200,
                    status='Success',
                    message='Counter Terrorist Wins')
        self.assertIsInstance(response, Response)

    def test_build_from_json(self):
        json_dict = dict(
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

        product = Response.build_from_json(json_dict)
        self.assertIsInstance(product, ProductData)

    def test_from_json_json_empty(self):
        with self.assertRaises(ValueError):
            product = Response.build_from_json()

    def test_from_json_wrong_type(self):
        input_data = ["oh girl", "you drive me wild"]
        with self.assertRaises(TypeError):
            product = Response.build_from_json(input_data)
