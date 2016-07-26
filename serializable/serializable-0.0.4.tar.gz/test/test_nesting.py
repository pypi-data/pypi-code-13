from serializable import to_serializable_repr, from_serializable_repr, Serializable
from nose.tools import eq_

class A(Serializable):
    def __init__(self, a_val):
        self.a = a_val

    def to_dict(self):
        return {"a_val": self.a}

def test_list_of_lists():
    x = [[1, 2], ["hello", "wookies"], [A(1), A(2)]]
    eq_(x, from_serializable_repr(to_serializable_repr(x)))

def test_dict_of_lists():
    x = {"a": [1, 2, 3], "b": ["hello", "goodbye"], "1": [A(1), A(2)]}
    eq_(x, from_serializable_repr(to_serializable_repr(x)))

def test_dict_with_tuple_keys():
    x = {(1, 2): "hello"}
    eq_(x, from_serializable_repr(to_serializable_repr(x)))

def test_object_with_dict_values():
    x = A(dict(snooze=5))
    eq_(x, from_serializable_repr(to_serializable_repr(x)))
