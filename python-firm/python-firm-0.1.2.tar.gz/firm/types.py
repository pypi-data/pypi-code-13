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

from firm.base import libfirm, ffi, BaseSequence, ident, deident, ffi_to_repr
from firm import bitfields
import firm.wrap as wrap


class Type(object):
    @property
    def _ir_val(self):
        return self._ir_type

    def __init__(self, ir_type):
        self._ir_type = ir_type

    def new_entity(self, name, parent=None):
        if parent is None:
            parent_ir = libfirm.get_glob_type()
        else:
            parent_ir = parent._ir_type
        return wrap.entity(libfirm.new_entity(parent_ir, ident(name),
                                              self._ir_type))

    def __eq__(self, other):
        if isinstance(other, Type):
            return self._ir_type == other._ir_type
        return NotImplemented

    def __hash__(self):
        return hash(self._ir_type)

    @property
    def mode(self):
        return libfirm.get_type_mode(self._ir_type)

    def __repr__(self):
        return self._repr(set())

    def get_alignment(self):
        return libfirm.get_type_alignment(self._ir_type)

    def set_alignment(self, value):
        assert self.state == bitfields.TypeState.UNDEFINED
        libfirm.set_type_alignment(self._ir_type, value)

    alignment = property(get_alignment, set_alignment)

    def get_dbg_info(self):
        return libfirm.get_type_dbg_info(self._ir_type)

    def get_size(self):
        return libfirm.get_type_size(self._ir_type)

    def set_size(self, value):
        assert self.state == bitfields.TypeState.UNDEFINED
        libfirm.set_type_size(self._ir_type, value)

    size = property(get_size, set_size)

    def get_state(self):
        return bitfields.TypeState.from_int(
            libfirm.get_type_state(self._ir_type))

    def set_state(self, value):
        libfirm.set_type_state(self._ir_type, value.value)

    state = property(get_state, set_state)

    def get_state_name(self):
        return ffi.string(libfirm.get_type_state_name())

    def get_print_type(self):
        buf = ffi.new('char[200]')
        libfirm.ir_print_type(buf, 200, self._ir_type)
        return ffi.string(buf)


class Array(Type):
    @classmethod
    def new(cls, element_type, size=0):
        """Create a new array type.

        @param element_type The firm.types.Type of the elements.
        @param size         The int of the constant size, or 0 if unknown.
        """
        assert element_type.state == bitfields.TypeState.FIXED
        ir_type = libfirm.new_type_array(element_type._ir_type, size)
        return cls(ir_type)

    @property
    def size(self):
        return libfirm.get_array_size(self._ir_type)

    @property
    def element_type(self):
        return wrap.type(libfirm.get_array_element_type(self._ir_type))

    def descend(self, index):
        return self.element_type

    def _repr(self, cache):
        if self in cache:
            return '...'
        cache.add(self)
        return 'Array(%s, %d)' % (self.element_type._repr(cache), self.size)


class Params(BaseSequence):
    def __len__(self):
        return libfirm.get_method_n_params(self._ir_val)

    def getitem(self, index):
        return wrap.type(libfirm.get_method_param_type(self._ir_val, index))

    def setitem(self, index, value):
        libfirm.set_method_param_type(self._ir_val, index, value._ir_type)


class Results(BaseSequence):
    def __len__(self):
        return libfirm.get_method_n_ress(self._ir_val)

    def getitem(self, index):
        return wrap.type(libfirm.get_method_res_type(self._ir_val, index))

    def setitem(self, index, value):
        libfirm.set_method_res_type(self._ir_val, index, value._ir_type)


class Method(Type):
    @classmethod
    def new(cls, args, results, is_variadic=None, cconv=None,
            property_mask=None):
        # define cc_cdecl_set (0)
        ir_type = libfirm.new_type_method(len(args), len(results), 0, 0, 0)
        method = cls(ir_type)
        for index, arg in enumerate(args):
            method.params[index] = arg
        for index, res in enumerate(results):
            method.results[index] = res
        return method

    @property
    def params(self):
        return Params(self._ir_type)

    @property
    def results(self):
        return Results(self._ir_type)

    @property
    def reg_params(self):
        return libfirm.get_method_n_regparams(self._ir_type)

    def get_variadic(self):
        return libfirm.is_method_variadic(self._ir_type)

    def set_variadic(self, value):
        libfirm.set_method_variadic(self._ir_type, value)

    is_variadic = property(get_variadic, set_variadic)

    def get_properties(self):
        return bitfields.MTPAdditionalProperties(
            libfirm.get_method_additional_properties(self._ir_type))

    def set_properties(self, property_mask):
        libfirm.set_method_additional_properties(self._ir_type, int(property_mask))

    def add_properties(self, flag):
        libfirm.add_method_additional_properties(self._ir_type, int(flag))

    @property
    def calling_convention(self):
        return libfirm.get_method_calling_convention(self._ir_type)

    def _repr(self, cache):
        if self in cache:
            return '...'
        cache.add(self)
        return 'Method([%s] -> [%s])' % (
            ', '.join(p._repr(cache) for p in self.params),
            ', '.join(r._repr(cache) for r in self.results))


class Pointer(Type):
    @classmethod
    def new(cls, points_to=None):
        if points_to is None:
            return cls(libfirm.new_type_pointer(ffi.NULL))
        return cls(libfirm.new_type_pointer(points_to._ir_type))

    def get_target(self):
        return wrap.type(libfirm.get_pointer_points_to_type(self._ir_type))

    def set_target(self, value):
        libfirm.set_pointer_points_to_type(self._ir_type, value._ir_type)

    target = property(get_target, set_target)

    def _repr(self, cache):
        if self in cache:
            return '...'
        cache.add(self)
        return 'Pointer(%s)' % (self.target._repr(cache),)


class Primitive(Type):
    @classmethod
    def new(cls, mode=None):
        if mode is None:
            mode = MODE_IS
        return cls(libfirm.new_type_primitive(mode))

    def _repr(self, cache):
        return 'Primitive(%s)' % (
            ffi_to_repr(ffi.string(libfirm.get_mode_name(self.mode))),)

    @property
    def size(self):
        return libfirm.get_mode_size_bytes(self.mode)


MODE_BS = libfirm.get_modeBs()
MODE_BU = libfirm.get_modeBu()
MODE_D = libfirm.get_modeD()
MODE_F = libfirm.get_modeF()
MODE_HS = libfirm.get_modeHs()
MODE_HU = libfirm.get_modeHu()
MODE_IS = libfirm.get_modeIs()
MODE_IU = libfirm.get_modeIu()
MODE_LS = libfirm.get_modeLs()
MODE_LU = libfirm.get_modeLu()

MODE_M = libfirm.get_modeM() # Memory
MODE_P = libfirm.get_modeP() # Pointer
MODE_T = libfirm.get_modeT() # Tuple
MODE_X = libfirm.get_modeX() # Control Flow

INT_8 = Primitive.new(MODE_BS)
UINT_8 = Primitive.new(MODE_BU)
FLOAT_64 = Primitive.new(MODE_D)
FLOAT_32 = Primitive.new(MODE_F)
INT_16 = Primitive.new(MODE_HS)
UINT_16 = Primitive.new(MODE_HU)
INT_32 = Primitive.new(MODE_IS)
UINT_32 = Primitive.new(MODE_IU)
INT_64 = Primitive.new(MODE_LS)
UINT_64 = Primitive.new(MODE_LU)
FLOAT = Primitive.new(MODE_F)
DOUBLE = Primitive.new(MODE_D)


class _CompoundType(Type, BaseSequence):
    def __init__(self, ir_type):
        super(_CompoundType, self).__init__(ir_type)

    @property
    def name(self):
        return deident(libfirm.get_compound_name(self._ir_type))

    def add_field(self, name, ty, offset=None, alignment=None):
        entity = libfirm.new_entity(self._ir_type,
                                    ident(name, b'%s.%%u' % (self.name,)),
                                    ty._ir_type)
        if offset is not None:
            libfirm.set_entity_offset(entity, offset)
        if alignment is not None:
            libfirm.set_entity_alignment(entity, alignment)

    def getitem(self, index):
        return wrap.entity(libfirm.get_compound_member(self._ir_type, index))

    def descend(self, index):
        return self[index].type

    def layout_default(self):
        libfirm.default_layout_compound_type(self._ir_type)


class Struct(_CompoundType):
    @classmethod
    def new(cls, name, fields=()):
        ir_type = libfirm.new_type_struct(ident(name))
        return cls(ir_type)

    def __len__(self):
        return libfirm.get_struct_n_members(self._ir_type)

    def getitem(self, index):
        return wrap.entity(libfirm.get_struct_member(self._ir_type, index))

    def _repr(self, cache):
        return 'Struct(%r)' % (ffi_to_repr(self.name),)


class Union(_CompoundType):
    @classmethod
    def new(cls, name, fields=()):
        ir_type = libfirm.new_type_union(ident(name))
        return cls(ir_type)

    def __len__(self):
        return libfirm.get_union_n_members(self._ir_type)

    def getitem(self, index):
        return wrap.entity(libfirm.get_union_member(self._ir_type, index))

    def _repr(self, cache):
        return 'Union(%r)' % (ffi_to_repr(self.name),)


class _Unknown(Type):
    def __init__(self):
        super(_Unknown, self).__init__(libfirm.get_unknown_type())

    def _repr(self, cache):
        return 'UNKNOWN'

UNKNOWN = _Unknown()


class Subtypes(BaseSequence):
    def __len__(self):
        return libfirm.get_class_n_subtypes(self._ir_val)

    def getitem(self, index):
        return Class(libfirm.get_class_subtype(self._ir_val, index))

    def remove(self, value):
        libfirm.remove_class_subtype(self._ir_val, value._ir_type)


class Supertypes(BaseSequence):
    def __len__(self):
        return libfirm.get_class_n_supertypes(self._ir_val)

    def getitem(self, index):
        return Class(libfirm.get_class_supertype(self._ir_val, index))

    def remove(self, value):
        libfirm.remove_class_supertype(self._ir_val, value._ir_type)


class Class(_CompoundType):
    @classmethod
    def new(cls, name, bases=(), fields=()):
        ir_type = libfirm.new_type_class(ident(name))
        for base in bases:
            libfirm.add_class_supertype(ir_type, base._ir_type)
        py_type = cls(ir_type)
        for name, typ in fields:
            py_type.add_field(name, typ)
        return py_type

    @property
    def subtypes(self):
        return Subtypes(self._ir_type)

    @property
    def supertypes(self):
        return Supertypes(self._ir_type)

    def __len__(self):
        return libfirm.get_class_n_members(self._ir_type)

    def getitem(self, index):
        return Class(libfirm.get_class_member(self._ir_type, index))

    def setitem(self, index, value):
        libfirm.set_method_res_type(self._ir_type, index, value._ir_type)

    def _repr(self, cache):
        return 'Class(%r)' % (ffi_to_repr(self.name),)

