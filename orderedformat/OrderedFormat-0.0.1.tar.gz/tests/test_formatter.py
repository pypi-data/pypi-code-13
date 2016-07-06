from unittest import TestCase
from nose.tools import ok_, eq_
from OrderedFormat.formatter import *

class TestOrderedFormat(TestCase):

    def test_iter_depth_zero(self):
        eq_(iter_depth([]), 0)
        eq_(iter_depth(()), 0)

    def test_iter_depth_one(self):
        eq_(iter_depth([1]), 1)
        eq_(iter_depth((1, )), 1)

    def test_iter_depth_for_list(self):
        list_array = [0, "1", ["2", [3, 4]], [5, "6"], [7, 8], [9, 10, [11, [12, 13]]]]
        eq_(iter_depth(list_array), 4)

    def test_iter_depth_for_dic(self):
        dict_value = {"a": 1, "b": {"c": 2, "d": {"f": 3, "g": {"h": 4}}}}
        eq_(iter_depth(dict_value), 4)

    def test_kflatten_simple(self):
        yml_data = """
        human:
          name: John
          age: 22
        """

        key_data = """
        human:
        - name
        - name
        """

        ordered_keys = load_ordered_keys(key_data=key_data, ext="yml")
        data = kflatten(yml_data, ordered_keys, type="yaml")

        eq_(data[0], "John")
        eq_(data[1], "John")
