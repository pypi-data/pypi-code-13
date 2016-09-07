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
from firm.base import libfirm, ffi, FirmException, ident, deident
from firm.bitfields import (Align,
                            EntityUsage,
                            Linkage,
                            MTPAdditionalProperties,
                            Visibility,
                            Volatility)
from firm import wrap, types


def _passthrough(name, fname=None):
    if fname is None:
        fname = 'entity_%s' % (name,)
    f = getattr(libfirm, fname)

    def wrapped(self, *args):
        return f(self._ir_entity, *args)
    wrapped.__name__ = name
    return wrapped


class Entity(object):
    """Entity: represent source objects.

    Entities are 'things that have addresses'.

    This includes compound entities like structs and unions, methods,
    parameters, and unknown entities, as well as atomic entities such
    as blah blah.
    """

    @property
    def _ir_val(self):
        return self._ir_entity

    def __init__(self, ir_entity):
        self._ir_entity = ir_entity

    def check(self):
        if not libfirm.check_entity(self._ir_entity):
            raise FirmException('Entity failed to check')

    def clone(self, name, owner=None):
        if owner is None:
            owner = GLOBAL
        return self.__class__(
            libfirm.clone_entity(self._ir_entity, ident(name),
                                 owner._ir_entity))

    def address_of(self, graph=None):
        if graph is None:
            from firm.function import IRGraph
            graph = IRGraph.const_graph()
        return graph.op_Address(self)

    # offset_bits_remainder
    # overwrites
    # overwrittenby
    # link (user *void)
    # irg (method)
    # visited

    has_definition = property(_passthrough('has_definition'))
    has_ld_ident = property(_passthrough('has_ld_ident'))
    is_externally_visible = property(_passthrough('is_externally_visible'))
    free = _passthrough('free_entity', 'free_entity')

    # def get_visited(self):
    #     return libfirm.get_entity_visited(self._ir_entity)

    # def set_visited(self, visited):
    #     libfirm.set_entity_visited(self._ir_entity, visited)

    # visited = property(get_visited, set_visited)

    def get_ident(self):
        return ffi.string(libfirm.get_entity_ident(self._ir_entity))

    def set_ident(self, value):
        libfirm.set_entity_ident(self._ir_entity,
                                 libfirm.new_id_from_str(value))

    ident = name = property(get_ident, set_ident)

    def get_ld_ident(self):
        return ffi.string(libfirm.get_entity_ld_ident(self._ir_entity))

    def set_ld_ident(self, ident):
        libfirm.set_entity_ld_ident(self._ir_entity,
                                    libfirm.new_id_from_str(ident))

    ld_ident = ld_name = property(get_ld_ident, set_ld_ident)

    def get_linkage(self):
        return Linkage(libfirm.get_entity_linkage(self._ir_entity))

    def set_linkage(self, value):
        libfirm.set_entity_linkage(self._ir_entity, value.value)

    linkage = property(get_linkage, set_linkage)

    def get_alias(self):
        return AliasEntity(libfirm.get_entity_alias(self._ir_entity))

    def set_alias(self, value):
        libfirm.set_entity_alias(self._ir_entity, value._ir_entity)

    alias = property(get_alias, set_alias)

    def get_aligned(self):
        return Align.from_int(libfirm.get_entity_aligned(self._ir_entity))
    
    def set_aligned(self, value):
        libfirm.set_entity_aligned(self._ir_entity, value.value)

    aligned = property(get_aligned, set_aligned)

    def get_alignment(self):
        return libfirm.get_entity_alignment(self._ir_entity)

    def set_alignment(self, alignment):
        libfirm.set_entity_alignment(self._ir_entity, alignment)

    alignment = property(get_alignment, set_alignment)

    # TODO: move bitfield methods to atomic
    def get_bitfield_size(self):
        return libfirm.get_entity_bitfield_size(self._ir_entity)
    
    def set_bitfield_size(self, value):
        libfirm.get_entity_bitfield_size(self._ir_entity, value)

    bitfield_size = property(get_bitfield_size, set_bitfield_size)

    def get_bitfield_offset(self):
        return libfirm.get_entity_bitfield_offset(self._ir_entity)

    def set_bitfield_offset(self, value):
        libfirm.set_entity_bitfield_offset(self._ir_entity, value)

    bitfield_offset = property(get_bitfield_offset, set_bitfield_offset)

    def get_debug_info(self):
        raw = libfirm.get_entity_dbg_info(self._ir_entity)
        if raw:
            return ffi.from_handle(raw)

    def set_debug_info(self, value):
        libfirm.set_entity_dbg_info(self._ir_entity, ffi.new_handle(value))

    debug_info = property(get_debug_info, set_debug_info)

    def get_usage(self):
        return EntityUsage(libfirm.get_entity_usage(self._ir_entity))

    def set_usage(self, value):
        libfirm.set_entity_usage(self._ir_entity, value.value)

    usage = property(get_usage, set_usage)

    def get_visibility(self):
        return Visibility.from_int(
            libfirm.get_entity_visibility(self._ir_entity))

    def set_visibility(self, value):
        libfirm.set_entity_visibility(self._ir_entity, value.value)

    visibility = property(get_visibility, set_visibility)

    def get_volatility(self):
        return Volatility(libfirm.get_entity_volatility(self._ir_entity))

    def set_volatility(self, value):
        libfirm.set_entity_volatility(self._ir_entity, value.value)

    volatility = property(get_volatility, set_volatility)

    def get_vtable_number(self):
        return libfirm.get_entity_vtable_number(self._ir_entity)

    def set_vtable_number(self, value):
        return libfirm.set_entity_vtable_number(self._ir_entity, value)

    vtable_number = property(get_vtable_number, set_vtable_number)

    @property
    def is_atomic(self):
        return libfirm.is_atomic_entity(self._ir_entity)

    @property
    def is_alias(self):
        return libfirm.is_alias_entity(self._ir_entity)

    @property
    def is_compound(self):
        return libfirm.is_compound_entity(self._ir_entity)

    @property
    def is_method(self):
        return libfirm.is_method_entity(self._ir_entity)

    @property
    def is_parameter(self):
        return libfirm.is_parameter_entity(self._ir_entity)

    @property
    def is_unknown(self):
        return libfirm.is_unknown_entity(self._ir_entity)

    def __repr__(self):
        if self is UNKNOWN:
            return "UNKNOWN_ENTITY"
        return "%s(%r)" % (self.__class__.__name__, self.name)

    def __eq__(self, other):
        return self._ir_entity == other

    def __hash__(self):
        return hash(self._ir_entity)

#    def mark_visited(self):
#        libfirm.mark_entity_visited(self._ir_entity)


UNKNOWN = Entity(libfirm.get_unknown_entity())


class _HasAdditionalProperties(object):
    def get_additional_properties(self):
        return MTPAdditionalProperties(
            libfirm.get_entity_additional_properties(self._ir_entity))

    def set_additional_properties(self, value):
        libfirm.set_entity_additional_properties(self._ir_entity, value.value)

    additional_properties = property(get_additional_properties,
                                     set_additional_properties)


class _CompoundMember(object):
    def get_owner(self):
        return wrap.type(libfirm.get_entity_owner(self._ir_entity))

    def set_owner(self, value):
        assert isinstance(value, types._CompoundType)
        libfirm.set_entity_owner(self._ir_entity, value._ir_type)

    owner = property(get_owner, set_owner)

    def get_offset(self):
        return libfirm.get_entity_offset(self._ir_entity)

    def set_offset(self, value):
        libfirm.set_entity_offset(self._ir_entity, value)

    offset = property(get_offset, set_offset)


class _HasType(object):
    def get_type(self):
        return wrap.type(libfirm.get_entity_type(self._ir_entity))

    def set_type(self, value):
        assert not isinstance(value, types.Method)
        libfirm.set_entity_type(self._ir_entity, value._ir_type)

    type = property(get_type, set_type)


class NormalEntity(_HasType, Entity):
    def get_initializer(self):
        return wrap.initializer(
            libfirm.get_entity_initializer(self._ir_entity))

    def set_initializer(self, initializer):
        libfirm.set_entity_initializer(self._ir_entity, initializer._ir_val)

    initializer = property(get_initializer, set_initializer)


class Parameter(_CompoundMember, Entity):
    def get_parameter_number(self):
        return libfirm.get_entity_parameter_number(self._ir_entity)

    def set_parameter_number(self, value):
        libfirm.set_entity_parameter_number(self._ir_entity, value)

    parameter_number = property(get_parameter_number, set_parameter_number)


class AliasEntity(_HasAdditionalProperties, Entity):
    pass


class CompoundEntity(_CompoundMember, _HasType, Entity):
    pass

class NormalCompoundEntity(NormalEntity, CompoundEntity):
    pass

class LabelEntity(Entity):
    @property
    def type(self):
        return wrap.type(libfirm.get_entity_type(self._ir_entity))

    def get_label(self):
        return libfirm.get_entity_label(self._ir_entity)

    def set_label(self, value):
        libfirm.set_entity_label(self._ir_entity, value)

    label = property(get_label, set_label)


class MethodEntity(_HasAdditionalProperties, Entity):
    def get_type(self):
        return wrap.type(libfirm.get_entity_type(self._ir_entity))

    def set_type(self, value):
        assert isinstance(value, types.Method)
        libfirm.set_entity_type(self._ir_entity, value._ir_type)

    type = property(get_type, set_type)

    def get_graph(self):
        import firm.function
        return firm.function.IRGraph(libfirm.get_entity_irg(self._ir_entity))

    def set_graph(self, value):
        libfirm.set_entity_irg(self._ir_entity, value._ir_graph)

    graph = property(get_graph, set_graph)

    def get_vtable_number(self):
        return libfirm.get_entity_vtable_number(self._ir_entity)

    def set_vtable_number(self, value):
        libfirm.set_entity_vtable_number(self._ir_entity, value)

    vtable_number = property(get_vtable_number, set_vtable_number)
