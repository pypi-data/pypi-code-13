from serializable import (
    class_to_serializable_representation,
    class_from_serializable_representation,
)
from nose.tools import eq_

class A(object):
    pass

def test_serialize_custom_class():
    A_reconstructed = class_from_serializable_representation(
        class_to_serializable_representation(A))
    eq_(A, A_reconstructed)


def test_serialize_builtin_class():
    int_reconstructed = class_from_serializable_representation(
        class_to_serializable_representation(int))
    eq_(int, int_reconstructed)
