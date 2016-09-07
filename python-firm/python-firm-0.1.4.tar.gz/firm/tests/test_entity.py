from firm.bitfields import Volatility
from firm.entity import UNKNOWN, NormalEntity, CompoundEntity
from firm.types import UNKNOWN as UNKNOWN_TYPE, Method, INT_32, Struct, DOUBLE
from firm.function import Function, IRGraph
from firm.initializer import prebuilt_constant
import firm.bitfields as bf

class NonsenseDbgInfo(object): pass

def test_unknown():
    assert UNKNOWN.name == b'unknown_entity'
    assert UNKNOWN.ld_name == b'unknown_entity'
    assert UNKNOWN.volatility == Volatility.NON_VOLATILE


def test_method_names():
    mty = Method.new([INT_32], [INT_32])
    function = Function.new(mty, b"test_method_names")

    assert function.name == b'test_method_names'
    assert function.ld_name == b'test_method_names'

    function.name = b'test_method_names_2'
    assert function.name == b'test_method_names_2'
    assert function.ld_name == b'test_method_names'

    function.ld_name = b'test_method_names_4'
    assert function.name == b'test_method_names_2'
    assert function.ld_name == b'test_method_names_4'

    function.name = b'test_method_names_3'
    assert function.name == b'test_method_names_3'
    assert function.ld_name == b'test_method_names_4'


def test_method_entity():
    mty = Method.new([INT_32], [INT_32])
    function = Function.new(mty, b"test_function_entity")
    # method-specific properties
    assert function.type == mty
    #assert function.vtable_number == 0
    assert not function.has_definition
    assert isinstance(function.graph, IRGraph)

    # the dbg_info field is for attaching arbitrary data to the function.
    dbg = NonsenseDbgInfo()
    function.dbg_info = dbg
    assert function.dbg_info is dbg

    assert function.linkage == bf.Linkage.CONSTANT
    assert function.aligned == bf.Align.IS_ALIGNED
    assert function.alignment == 0
    # usage is unknown because we haven't computed it yet.
    assert function.usage == bf.EntityUsage.UNKNOWN
    assert function.visibility == bf.Visibility.EXTERNAL
    assert function.volatility == bf.Volatility.NON_VOLATILE
    assert function.is_method
    #assert not function.is_atomic
    assert not function.is_alias
    assert not function.is_compound
    assert not function.is_parameter
    assert not function.is_unknown

    function.linkage = bf.Linkage.WEAK
    function.aligned = bf.Align.NON_ALIGNED
    function.alignment = 8
    function.usage = bf.EntityUsage.NONE
    function.visibility = bf.Visibility.PRIVATE
    function.volatility = bf.Volatility.IS_VOLATILE

    assert function.linkage == bf.Linkage.WEAK
    assert function.aligned == bf.Align.NON_ALIGNED
    assert function.alignment == 8
    # usage is unknown because we haven't computed it yet.
    assert function.usage == bf.EntityUsage.NONE
    assert function.visibility == bf.Visibility.PRIVATE
    assert function.volatility == bf.Volatility.IS_VOLATILE


def test_parameter_entity():
    """uh, we currently don't produce these from within python-firm.

    if/when we do, we should test them.
    """
    mty = Method.new([INT_32, INT_32], [INT_32])
    function = Function.new(mty, b"test_parameter_entity")


def test_global_entity():
    struct = Struct.new(b"entity_global")
    struct.add_field(b"foo", INT_32)
    struct.add_field(b"bar", DOUBLE)
    struct.layout_default()
    global_struct = prebuilt_constant(b"entity_global_instance", [-1000, 7.5],
                                      struct)

    assert global_struct.linkage == bf.Linkage.DEFAULT
    assert global_struct.aligned == bf.Align.IS_ALIGNED
    assert global_struct.alignment == 0
    # usage is unknown because we haven't computed it yet.
    assert global_struct.usage == bf.EntityUsage.UNKNOWN
    assert global_struct.visibility == bf.Visibility.EXTERNAL
    assert global_struct.volatility == bf.Volatility.NON_VOLATILE
    assert not global_struct.is_method
    assert not global_struct.is_alias
    assert global_struct.is_compound
    assert not global_struct.is_parameter
    assert not global_struct.is_unknown
    assert isinstance(global_struct, CompoundEntity)
    assert isinstance(global_struct, NormalEntity)
    assert global_struct.initializer
