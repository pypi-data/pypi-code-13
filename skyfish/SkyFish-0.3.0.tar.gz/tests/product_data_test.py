import unittest
from skyfish.models import ProductData

class ProductDataTest(unittest.TestCase):

    def test_initializtion(self):
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

        product = ProductData(json_dict)
        self.assertIsInstance(product, ProductData)
        self.assertEqual(product.name, 'A test product')

    def test_input_not_dict(self):
        input_data = ["one", "you're like a dream come true"]
        with self.assertRaises(TypeError):
            prod = ProductData(input_data)

    def test_initialization_error(self):
        with self.assertRaises(TypeError):
            prod = ProductData()

    def test_limitless_wrong_type(self):
        json_dict = dict(
            name='A test product',
            limitless=1,
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
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_price_empty(self):
        json_dict = dict(
            name='A test product',
            limitless=False,
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
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_price_wrong_type(self):
        json_dict = dict(
            name='A test product',
            limitless=False,
            price="1000",
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
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_quantity_empty(self):
        json_dict = dict(
            name='A test product',
            limitless=False,
            price=10000,
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
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_quantity_wrong_type(self):
        json_dict = dict(
            name='A test product',
            limitless=False,
            price=10000,
            quantity='100',
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
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)


    def test_need_address_wrong_type(self):
        json_dict = dict(
            name='A test product',
            limitless=False,
            price=10000,
            quantity=100,
            need_address='True',
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

        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_name_empty(self):
        json_dict = dict(
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

        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_name_wrong_type(self):
        json_dict = dict(
            name=10 ,
            limitless=False,
            price=10000,
            quantity=100,
            need_address='True',
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
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_sku_empty(self):
        json_dict = dict(
            name='Some name' ,
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
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_sku_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            sku=1,
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_weight_empty(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            insurance_type='NEEDED',
            payment_types=['BANK_TRANSFER', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_weight_wrong_type(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight='100',
            insurance_type='NEEDED',
            payment_types=['BANK_TRANSFER', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_descrtiption_empty(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
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
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_description_wrong_type(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description=True,
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
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_payment_types_empty(self):
        json_dict = dict(
            name='Some name',
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
            sku='somesu',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_payment_types_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            payment_types='BANK_TRANSFER',
            sku=1,
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_payment_types_not_expected(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['WRONG', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(ValueError):
            product = ProductData(json_dict)

    def test_payment_types_detail_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=[0, 1],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_image_url_empty(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_image_url_wrong_type(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url='http://someimage.com/pic1.jpg',
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_image_url_detail_wrong_type(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[1,2],
            description='This is an example product post for creation testing',
            environment_type='DEVELOPMENT',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_discount_empty(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_discount_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=1000,
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_discount_field_not_expected(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        extra='extra',
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_discount_type_not_expected(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOTHING',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(ValueError):
            product = ProductData(json_dict)

    def test_insurance_type_empty(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_insurance_type_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            insurance_type=1,
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_insurance_type_unexpected_type(self):
        json_dict = dict(
            name='Some name',
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
            insurance_type='DONT_KNOW',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(ValueError):
            product = ProductData(json_dict)

    def test_product_varian_wrong_type(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant='test'
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_environment_type_empty(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(AttributeError):
            product = ProductData(json_dict)

    def test_environment_type_wrong_type(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type=1,
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(TypeError):
            product = ProductData(json_dict)

    def test_environment_type_not_expected(self):
        json_dict = dict(
            name='Some name',
            limitless=False,
            price=10000,
            quantity=100,
            need_address=True,
            image_url=[
                'http://someimage.com/pic1.jpg',
                'http://someimage.com/pic2.jpg'],
            description='This is an example product post for creation testing',
            environment_type='COMMON',
            weight=100,
            insurance_type='NEEDED',
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )
        with self.assertRaises(ValueError):
            product = ProductData(json_dict)

    def test_to_dict(self):
        json_dict = dict(
            name='Some name',
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
            payment_types=['BCA', 'CREDIT_CARD'],
            sku='somesku',
            discount=dict(
                        discount_type='NOMINAL',
                        amount=1000),
            product_variant=dict()
        )

        product = ProductData(json_dict)
        product_dict = product.to_dict()
        expected_fields = [
            'id',
            'name',
            'limitless',
            'price',
            'quantity',
            'need_address',
            'image_url',
            'description',
            'environment_type',
            'weight',
            'insurance_type',
            'payment_types',
            'sku',
            'discount',
            'product_variant']
        for item in product_dict.keys():
            self.assertIn(item, expected_fields)
