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
from firm.base import libfirm, FirmException, BaseSequence, ident
from firm.bitfields import InitializerKind, Visibility, Linkage
from firm.tarval import Tarval
from firm.entity import Entity
from firm import wrap

import firm.types


try:
    basestring
except NameError:
    basestring = str


def initializer(value, ty):
    """Create statically-allocated literal values.

    Types of initialisation supported include:
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
    if isinstance(value, bytes) and isinstance(ty, firm.types.Array):
        # char foo[] = "hello"
        ir_initializer = libfirm.create_initializer_compound(len(value))
        for index, el in enumerate(value):
            if isinstance(el, str):
                el = ord(el)
            tarval = Tarval.from_int(el, ty.element_type.mode)
            sub_init = libfirm.create_initializer_tarval(tarval._ir_val)
            libfirm.set_initializer_compound_value(ir_initializer, index,
                                                   sub_init)
        return CompoundInitializer(ir_initializer)
    elif isinstance(value, bytes) and isinstance(ty, firm.types.Primitive):
        tarval = Tarval.from_str(value, ty.mode)
        ir_initializer = libfirm.create_initializer_tarval(tarval._ir_val)
        return TarvalInitializer(ir_initializer)
    elif isinstance(value, basestring):
        raise FirmException("Can't initialise a string that isn't bytes")
    elif isinstance(value, Entity):
        ir_initializer = libfirm.create_initializer_const(
            value.address_of()._ir_node)
        return ConstInitializer(ir_initializer)
    elif isinstance(value, Tarval):
        ir_initializer = libfirm.create_initializer_tarval(value._ir_val)
        return TarvalInitializer(ir_initializer)
    elif isinstance(value, (int, float)):
        tarval = Tarval.from_str(b"%r" % value, ty.mode)
        ir_initializer = libfirm.create_initializer_tarval(tarval._ir_val)
        return TarvalInitializer(ir_initializer)
    elif value is None:
        return NULL
    ir_initializer = libfirm.create_initializer_compound(len(value))
    for index, el in enumerate(value):
        sub_init = initializer(el, ty.descend(index))
        libfirm.set_initializer_compound_value(ir_initializer, index,
                                               sub_init._ir_val)
    return CompoundInitializer(ir_initializer)


def prebuilt_constant(name, value, ty, visibility=None, linkage=None):
    return initializer(value, ty).to_entity(name, ty, visibility, linkage)


class Initializer(object):
    def __init__(self, value):
        self._ir_val = value

    @property
    def kind(self):
        return InitializerKind.from_int(
            libfirm.get_initializer_kind(self._ir_val))


NULL = Initializer(libfirm.get_initializer_null())


class ConstInitializer(Initializer):
    @property
    def value(self):
        return wrap.node(libfirm.get_initializer_const_value(self._ir_val))


class TarvalInitializer(Initializer):
    @property
    def value(self):
        return wrap.tarval(libfirm.get_initializer_tarval_value(self._ir_val))


class CompoundInitializer(Initializer, BaseSequence):
    def __len__(self):
        return libfirm.get_initializer_compound_n_entries(self._ir_val)

    def getitem(self, index):
        return wrap.initializer(
            libfirm.get_initializer_compound_value(self._ir_val, index))

    def to_entity(self, name, ty, visibility=None, linkage=None):
        if visibility is None:
            visibility = Visibility.EXTERNAL
        if linkage is None:
            linkage = Linkage.DEFAULT
        ir_entity = libfirm.new_global_entity(libfirm.get_glob_type(),
                                              ident(name),
                                              ty._ir_type,
                                              visibility.value,
                                              linkage.value)
        libfirm.set_entity_initializer(ir_entity, self._ir_val)
        return wrap.entity(ir_entity)



