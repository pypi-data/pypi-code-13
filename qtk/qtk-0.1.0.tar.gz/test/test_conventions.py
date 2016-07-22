from qtk.conventions import Convention
from unittest import TestCase


class TestConventions(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conventions_exist(self):
        self.assertGreater(len(Convention._conventions), 0)