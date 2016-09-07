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
from firm.base import libfirm
# imports at the bottom, because these functions are sometimes
# obtained early

def entity(ir_entity):
    from firm import entity, function, types
    if libfirm.is_compound_entity(ir_entity):
        if libfirm.entity_has_definition(ir_entity):
            return entity.NormalCompoundEntity(ir_entity)
        return entity.CompoundEntity(ir_entity) # a struct? a union?
    elif libfirm.is_method_entity(ir_entity):
        return function.Function(ir_entity)
    elif libfirm.is_parameter_entity(ir_entity):
        return entity.Parameter(ir_entity)
    elif libfirm.is_unknown_entity(ir_entity):
        return entity.UNKNOWN
    elif libfirm.is_alias_entity(ir_entity):
        return entity.AliasEntity(ir_entity)
    return entity.NormalEntity(ir_entity)


def node(value):
    from firm.operations import by_opcode
    opcode = libfirm.get_irn_opcode(value)
    return by_opcode[opcode](value)


def type(value):
    from firm import types
    if libfirm.is_Method_type(value):
        return types.Method(value)
    if libfirm.is_Array_type(value):
        return types.Array(value)
    if libfirm.is_Pointer_type(value):
        return types.Pointer(value)
    if libfirm.is_Struct_type(value):
        return types.Struct(value)
    if libfirm.is_Union_type(value):
        return types.Union(value)
    if libfirm.is_unknown_type(value):
        return types.UNKNOWN
    if libfirm.is_Class_type(value):
        return types.Class(value)
    if libfirm.is_Primitive_type(value):
        return types.Primitive(value)


def initializer(value):
    from firm.bitfields import InitializerKind
    from firm import initializer
    raw_kind = libfirm.get_initializer_kind(value)
    kind = InitializerKind.from_int(raw_kind)
    if kind == InitializerKind.CONST:
        return initializer.ConstInitializer(value)
    if kind == InitializerKind.NULL:
        return initializer.NULL
    if kind == InitializerKind.TARVAL:
        return initializer.TarvalInitializer(value)
    if kind == InitializerKind.COMPOUND:
        return initializer.CompoundInitializer(value)


def tarval(value):
    from firm import tarval
    try:
        return tarval.singletons[value]
    except KeyError:
        return tarval.Tarval(value)

