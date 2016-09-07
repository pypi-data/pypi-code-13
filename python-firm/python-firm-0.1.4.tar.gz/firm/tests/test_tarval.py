from __future__ import division
from firm.base import libfirm
from firm.tarval import Tarval, BAD, UNKNOWN, FALSE_B, TRUE_B
from firm import types
import math


# coverage is fairly lacking - we need to test statics, operations on
# tarvals, and probably rip out comparable.  Also NaNs.

def test_eq():
    tv = Tarval(libfirm.new_integer_tarval_from_str(b"nope", 4, False, 10,
                                                    types.MODE_HS))
    assert tv == BAD

    x = Tarval.from_int(7, types.MODE_HS)
    y = Tarval.from_int(7, types.MODE_IS)
    assert x != y

    z = Tarval.from_int(7, types.MODE_IS)
    assert y == z


def test_int_7():
    x = Tarval.from_int(7, types.MODE_IS)
    assert x.as_long() == 7
    assert x.highest_bit == 2
    assert x.lowest_bit == 0
    assert x.mode == types.MODE_IS
    assert x.popcount == 3
    assert x.get_sub_bits(0) == 7
    assert x.get_sub_bits(1) == 0

    assert not x.is_all_one
    assert x.is_constant
    assert not x.is_double
    assert x.is_finite
    assert x.is_long
    assert not x.is_nan
    assert not x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x) == 'Tarval<Is, i, 7>'
    assert x.size == 4
    assert hash(x) is not None
    assert list(x.to_bytes()) == [7, 0, 0, 0]
    

def test_int_neg():
    x = Tarval.from_int(-17, types.MODE_IS)
    assert x.as_long() == -17
    assert x.highest_bit == 31
    assert x.lowest_bit == 0
    assert x.mode == types.MODE_IS
    assert x.popcount == 31
    assert x.get_sub_bits(0) == 0xef
    assert x.get_sub_bits(1) == 0xff

    assert not x.is_all_one
    assert x.is_constant
    assert not x.is_double
    assert x.is_finite
    assert x.is_long
    assert not x.is_nan
    assert x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x) == 'Tarval<Is, i, -17>'
    assert x.size == 4
    assert hash(x) is not None
    assert list(x.to_bytes()) == [0xef, 0xff, 0xff, 0xff]


def test_int_maxuint():
    x = Tarval.from_int((1 << 32) - 1, types.MODE_IU)
    assert x.as_long() == 0xffffffff
    assert x.highest_bit == 31
    assert x.lowest_bit == 0
    assert x.mode == types.MODE_IU
    assert x.popcount == 32
    assert x.get_sub_bits(0) == 0xff
    assert x.get_sub_bits(1) == 0xff

    assert x.is_all_one
    assert x.is_constant
    assert not x.is_double
    assert x.is_finite
    assert x.is_long
    assert not x.is_nan
    assert not x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x) == 'Tarval<Iu, i, 4294967295>'
    assert x.size == 4
    assert hash(x) is not None
    assert list(x.to_bytes()) == [0xff, 0xff, 0xff, 0xff]


def test_double():
    x = Tarval.from_double(-math.pi, types.MODE_D)
    assert x.as_double() == -math.pi
    assert x.mode == types.MODE_D
    assert x.get_sub_bits(0) == 0x18
    assert x.get_sub_bits(1) == 0x2d

    assert not x.is_all_one
    assert x.is_constant
    assert x.is_double
    assert x.is_finite
    assert not x.is_long
    assert not x.is_nan
    assert x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x) == 'Tarval<D, f, -3.141592653589793>'
    assert x.size == 8
    assert hash(x) is not None
    assert list(x.to_bytes()) == [0x18, 0x2d, 0x44, 0x54,
                                  0xfb, 0x21, 0x9, 0xc0]


def test_float():
    x = Tarval.from_double(math.pi, types.MODE_F)
    assert (x.as_double() - math.pi) / math.pi < (0.5 ** 22)
    assert x.mode == types.MODE_F
    assert x.get_sub_bits(0) == 0xdb
    assert x.get_sub_bits(1) == 0x0f

    assert not x.is_all_one
    assert x.is_constant
    assert x.is_double
    assert x.is_finite
    assert not x.is_long
    assert not x.is_nan
    assert not x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x).startswith('Tarval<F, f, 3.141592')
    assert x.size == 4
    assert hash(x) is not None
    assert list(x.to_bytes()) == [0xdb, 0xf, 0x49, 0x40]


def test_inf():
    x = Tarval.from_double(float('-inf'), types.MODE_D)
    assert x.as_double() == float('-inf')
    assert x.mode == types.MODE_D
    assert x.get_sub_bits(0) == 0
    assert x.get_sub_bits(7) == 0xff

    assert not x.is_all_one
    assert x.is_constant
    assert x.is_double
    assert not x.is_finite
    assert not x.is_long
    assert not x.is_nan
    assert x.is_negative
    assert not x.is_null
    assert not x.is_one
    assert not x.is_quiet_nan
    assert not x.is_signaling_nan

    assert repr(x) == 'Tarval<D, inf, -inf>'
    assert x.size == 8
    assert hash(x) is not None
    assert list(x.to_bytes()) == [0, 0, 0, 0, 0, 0, 0xf0, 0xff]
