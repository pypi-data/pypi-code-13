"""
Give examples of all the following:

    initializer(b"hello\0", Array.new(UINT_8))
    initializer("7", UINT_8)
    initializer(7, UINT_8)
    initializer(7.0, DOUBLE)
    initializer(entity, Pointer(...))
    initializer(tarval, primitive)
    initializer([...], Array)
    initializer([...], Struct)
    initializer([...], Union)
"""
from __future__ import division
from firm.initializer import initializer
from firm.types import (Array, Pointer, Struct, Union, Method,
                        UINT_8, DOUBLE, INT_32, MODE_IS)
from firm.function import Function
from firm.tarval import Tarval, TRUE_B, BAD

def test_string():
    x = initializer(b"hello\0", Array.new(UINT_8))
    assert len(x) == 6
    expected = [ord(char) for char in "hello\0"]
    assert [char.value.as_long() for char in x] == expected

def test_float():
    x = initializer(3000., DOUBLE)
    assert x.value.as_double() == 3000.
    assert x.value.size == 8

def test_int_from_string():
    x = initializer(b"7", UINT_8)
    assert x.value.as_long() == 7
    assert x.value.size == 1

def test_int():
    x = initializer(3000, INT_32)
    assert x.value.as_long() == 3000
    assert x.value.size == 4

def test_entity():
    sig = Method.new([INT_32] * 3, [INT_32])
    func = Function.new(sig, b"entity_initializer")
    x = initializer(func, sig)
    assert x.value.entity == func

def test_tarval():
    tar = Tarval.from_int(7, MODE_IS)
    x = initializer(tar, INT_32)
    assert x.value.as_long() == 7
    assert x.value.size == 4

def test_tarval_bad():
    x = initializer(BAD, INT_32)
    assert x.value == BAD

def test_array():
    xs = initializer([7, 5, 10], Array.new(INT_32))
    assert [x.value.as_long() for x in xs] == [7, 5, 10]

def test_struct():
    struct = Struct.new(b"initializer_struct")
    struct.add_field(b"foo", INT_32)
    struct.add_field(b"bar", DOUBLE)
    xs = initializer([-1000, 7.5], struct)
    assert len(xs) == 2
    assert xs[0].value.as_long() == -1000
    assert xs[1].value.as_double() == 7.5

def test_array_of_struct():
    struct = Struct.new(b"initializer_aos")
    struct.add_field(b"foo", INT_32)
    struct.add_field(b"bar", DOUBLE)
    struct.layout_default()

    array = Array.new(struct, 2)
    xs = initializer([[-1000, 7.5], [2000000, 0.59]], array)
    assert len(xs) == 2
    [[i0, d0], [i1, d1]] = xs
    assert i0.value.as_long() == -1000
    assert d0.value.as_double() == 7.5
    assert i1.value.as_long() == 2000000
    assert d1.value.as_double() == 0.59

def test_struct_of_array():
    int_array = Array.new(INT_32, 2)
    double_array = Array.new(DOUBLE, 2)
    struct = Struct.new(b"initializer_soa")
    struct.add_field(b"foo", int_array)
    struct.add_field(b"bar", double_array)
    xs = initializer([[-1000, 9001], [7.5, 0.59]], struct)
    assert len(xs) == 2
    s0, s1 = xs
    assert s0[0].value.as_long() == -1000
    assert s0[1].value.as_long() == 9001
    assert s1[0].value.as_double() == 7.5
    assert s1[1].value.as_double() == 0.59
