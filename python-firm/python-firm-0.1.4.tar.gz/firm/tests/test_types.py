from firm.types import (Array, Method, Pointer, Struct, Union, Class,
                        INT_8, INT_32, UINT_32, FLOAT_64)

def test_fixed_array():
    xs = Array.new(INT_32, 7)
    assert xs.element_type == INT_32
    assert xs.size == 7
    assert repr(xs) == 'Array(Primitive(Is), 7)'

def test_varying_array():
    xs = Array.new(INT_32)
    assert xs.element_type == INT_32
    assert xs.size == 0
    assert repr(xs) == 'Array(Primitive(Is), 0)'

def test_byte_array():
    xs = Array.new(INT_8, 7)
    assert xs.element_type == INT_8
    assert xs.size == 7
    assert repr(xs) == 'Array(Primitive(Bs), 7)'

def test_method():
    method = Method.new([INT_32, INT_8], [UINT_32, FLOAT_64])
    assert list(method.params) == [INT_32, INT_8]
    assert list(method.results) == [UINT_32, FLOAT_64]
    method.regparams = 1
    assert method.regparams == 1
    assert not method.is_variadic
    #assert method.calling_convention
    assert repr(method) == ('Method([Primitive(Is), Primitive(Bs)] -> '
                            '[Primitive(Iu), Primitive(D)])')

def test_variadic_method():
    method = Method.new([INT_32], [INT_32])
    method.variadic = 1
    assert method.variadic
    #assert method.calling_convention

def test_pointer():
    pointer = Pointer.new(INT_32)
    assert pointer.target == INT_32
    assert repr(pointer) == 'Pointer(Primitive(Is))'

def test_cyclic_pointer():
    pointer = Pointer.new()
    pointer.target = pointer
    assert pointer.target == pointer
    assert repr(pointer) == 'Pointer(...)'

def test_struct():
    struct = Struct.new(b"hello")
    struct.add_field(b"world", INT_32, 5, 8)
    # todo: add methods for listing and getting fields.
    assert struct[0].type == INT_32 # is this actually an entity?
    assert repr(struct) == "Struct('hello')"

def test_union():
    cls = Struct.new(b"class_attr")
    cls.add_field(b"n_methods", INT_32)
    meth = Struct.new(b"method_attr")
    meth.add_field(b"n_params", UINT_32)

    union = Union.new(b"attr")
    union.add_field(b"cls", cls, 0)
    union.add_field(b"meth", meth, 0)

    assert union[0].type == cls
    assert union[1].type == meth
    assert repr(union) == "Union('attr')"

def test_types_hashable():
    pointer = Pointer.new(INT_32)
    first_hash = hash(pointer)
    pointer.target = UINT_32
    assert first_hash == hash(pointer)
