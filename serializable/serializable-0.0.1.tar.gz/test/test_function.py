from serializable import (
    function_to_serializable_representation,
    function_from_serializable_representation,
)
from nose.tools import eq_

def global_fn():
    pass

def test_serialize_custom_function():
    fn_reconstructed = function_from_serializable_representation(
        function_to_serializable_representation(global_fn))
    eq_(global_fn, fn_reconstructed)


def test_serialize_builtin_function():
    fn_reconstructed = function_from_serializable_representation(
        function_to_serializable_representation(sum))
    eq_(sum, fn_reconstructed)
