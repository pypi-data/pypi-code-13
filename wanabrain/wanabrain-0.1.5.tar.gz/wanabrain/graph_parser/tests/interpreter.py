import unittest
from wanabrain.graph_parser.factory import ObjectFactory
from wanabrain.graph_parser.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.interpreter = ObjectFactory.createObject(Interpreter.__name__)

    def test_is_hypernym(self):

        self.assertTrue(self.interpreter.is_hypernym('person', 'indian'))
        self.assertFalse(self.interpreter.is_hypernym('peanut', 'dog'))

    def test_translate(self):

        self.assertEqual('dog', self.interpreter.translate('chien'))

if __name__ == '__main__':
    # unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestInterpreter)
    unittest.TextTestRunner(verbosity=2).run(suite)