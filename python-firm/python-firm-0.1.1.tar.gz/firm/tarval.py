#   python-firm:  CFFI wrapper for the libFirm compiler backend.
#   Copyright (C) 2016  William ML Leslie
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
from firm.base import libfirm, ffi, FirmException, ffi_to_repr
from firm.bitfields import Relation

get_wrap_on_overflow = libfirm.tarval_get_wrap_on_overflow
set_wrap_on_overflow = libfirm.tarval_set_wrap_on_overflow


def binary_op(name, cls=None):
    fn = getattr(libfirm, 'tarval_%s' % name)
    if cls is None:
        def op(self, other):
            return Tarval(fn(self._ir_val, other._ir_val))
    else:
        def op(self, other):
            return cls(fn(self._ir_val, other._ir_val))
    return op


def unary_op(name, cls=None):
    fn = getattr(libfirm, 'tarval_%s' % name)
    if cls is None:
        def op(self):
            return Tarval(fn(self._ir_val))
    else:
        def op(self):
            return cls(fn(self._ir_val))
    return op


def predicate(name):
    return simple('tarval_is_%s' % name, True)


def simple(name, prop=False):
    fn = getattr(libfirm, name)
    def op(self):
        return fn(self._ir_val)
    if prop:
        return property(op, doc=name)
    return op


class Tarval(object):
    def __init__(self, value):
        self._ir_val = value

    @classmethod
    def from_int(cls, i, mode):
        assert isinstance(i, int)
        rep = u"%s" % (-i if i < 0 else i)
        rep = rep.encode('latin1')
        return cls(libfirm.new_integer_tarval_from_str(rep, len(rep), i < 0,
                                                       10, mode))

    @classmethod
    def from_bytes(cls, buf, mode):
        return cls(libfirm.new_tarval_from_bytes(buf, mode))

    @classmethod
    def from_double(cls, doub, mode):
        return cls(libfirm.new_tarval_from_double(doub, mode))

    @classmethod
    def from_str(cls, buf, mode):
        return cls(libfirm.new_tarval_from_str(buf, len(buf), mode))

    @classmethod
    def new_nan(cls, mode, signalling, payload):
        return cls(libfirm.new_tarval_nan(mode, signalling, payload._ir_val))

    def as_double(self):
        assert self.is_double
        return libfirm.get_tarval_double(self._ir_val)

    def as_long(self):
        assert self.is_long
        return libfirm.get_tarval_long(self._ir_val)

    as_long_double = simple('get_tarval_long_double')
    highest_bit = simple('get_tarval_highest_bit', True)
    lowest_bit = simple('get_tarval_lowest_bit', True)
    mode = simple('get_tarval_mode', True)
    popcount = simple('get_tarval_popcount', True)

    def get_sub_bits(self, offset):
        return libfirm.get_tarval_sub_bits(self._ir_val, offset)

    __abs__ = abs = unary_op('abs')
    add = binary_op('add')
    and_ = binary_op('and')
    andnot = binary_op('andnot')

    def bitcast(self, mode):
        return Tarval(libfirm.tarval_bitcast(self._ir_val, mode))

    def convert(self, mode):
        # TODO: check this
        if libfirm.mode_is_smaller(mode, self.mode):
            raise FirmException('Cannot convert %s to %s' % (mode, self.mode))
        return Tarval(libfirm.tarval_bitcast(self._ir_val, mode))

    tcmp = binary_op('cmp', Relation)

    def relation(self, other, rel):
        return self.tcmp(other) & rel == rel

    @property
    def comparable(self):
        """Get a version of this tarval that supports native comparisons.
        """
        return Comparable(self._ir_val)

    div = binary_op('div')

    def divmod(self, other):
        mod = ffi.new('ir_tarval**')
        div = libfirm.tarval_divmod(self._ir_val, other._ir_val, mod)
        return Tarval(div), Tarval(mod[0])

    __xor__ = xor = binary_op('eor')
    __mod__ = mod = binary_op('mod')
    __mul__ = mul = binary_op('mul')
    shl = binary_op('shl')
    shr = binary_op('shr')
    shrs = binary_op('shrs')
    __sub__ = sub = binary_op('sub')

    neg = unary_op('neg')
    not_ = unary_op('not')
    __or__ = or_ = unary_op('or')
    ornot = unary_op('ornot')

    is_all_one = predicate('all_one')
    is_constant = predicate('constant')
    is_double = predicate('double')
    is_finite = predicate('finite')
    is_long = predicate('long')
    is_nan = predicate('nan')
    is_negative = predicate('negative')
    is_null = predicate('null')
    is_one = predicate('one')
    is_quiet_nan = predicate('quiet_nan')
    is_signaling_nan = predicate('signaling_nan')

    def representation(self):
        if self.is_null:
            return 'null', None
        if not self.is_finite:
            return 'inf', self.as_double()
        if self.is_nan:
            if self.is_signaling_nan:
                return 'snan', self.as_double()
            return 'qnan', self.as_double()
        elif self.is_double:
            return 'f', self.as_double()
        elif self.is_long:
            return 'i', self.as_long()
        elif self == BAD:
            return '_', 'bad'
        elif self == UNKNOWN:
            return '_', 'unknown'
        elif self == TRUE_B:
            return 'b', 'true'
        elif self == FALSE_B:
            return 'b', 'false'

    def shl_unsigned(self, val):
        return Tarval(libfirm.tarval_shl_unsigned(self._ir_val, val))

    def shr_unsigned(self, val):
        return Tarval(libfirm.tarval_shr_unsigned(self._ir_val, val))

    def shrs_unsigned(self, val):
        return Tarval(libfirm.tarval_shrs_unsigned(self._ir_val, val))

    def to_bytes(self):
        buf = ffi.new('unsigned char[]', self.size)
        libfirm.tarval_to_bytes(buf, self._ir_val)
        return buf

    @property
    def size(self):
        return libfirm.get_mode_size_bytes(self.mode)

    exponent = simple('tarval_get_exponent', True)
    has_zero_mantissa = simple('tarval_zero_mantissa', True)

    def can_convert_lossless(self, mode):
        return libfirm.tarval_ieee754_can_conv_lossless(self._ir_val, mode)

    def __eq__(self, other):
        return self._ir_val == other

    def __hash__(self):
        return hash(self._ir_val)

    def __repr__(self):
        rt, val = self.representation()
        modename = ffi_to_repr(ffi.string(libfirm.get_mode_name(self.mode)))
        return 'Tarval<%s, %s, %r>' % (modename, rt, val)


class Comparable(Tarval):
    def __eq__(self, other):
        return self.relation(other, Relation.EQUAL)

    def __ne__(self, other):
        return self.relation(other, Relation.LESS_GREATER)

    def __lt__(self, other):
        return self.relation(other, Relation.LESS_THAN)

    def __le__(self, other):
        return self.relation(other, Relation.LESS_EQUAL)

    def __gt__(self, other):
        return self.relation(other, Relation.GREATER_THAN)

    def __ge__(self, other):
        return self.relation(other, Relation.GREATER_EQUAL)

    __hash__ = None


FALSE_B = Tarval(libfirm.get_tarval_b_false())
TRUE_B = Tarval(libfirm.get_tarval_b_true())
BAD = Tarval(libfirm.get_tarval_bad())
UNKNOWN = Tarval(libfirm.get_tarval_unknown())

del binary_op, unary_op, predicate, simple

singletons = {
    FALSE_B : FALSE_B,
    TRUE_B : TRUE_B,
    BAD : BAD,
    UNKNOWN : UNKNOWN
}
