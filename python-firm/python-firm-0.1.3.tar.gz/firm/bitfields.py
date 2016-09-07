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
import collections
from firm.base import libfirm

class Enum(object):
    fields = None

    @property
    def _ir_val(self):
        return self.value

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__,
                          self.name)

    def __index__(self):
        return self.value

    __int__ = __index__

    def __nonzero__(self):
        return bool(self.value)

    @classmethod
    def add_field(cls, name, value):
        instance = cls(value, name)
        if cls.fields is None:
            cls.fields = {}
        cls.fields[value] = instance
        setattr(cls, name, instance)

    @classmethod
    def from_int(cls, value):
        if int(value) in cls.fields:
            return cls.fields[value]
        return cls(value, '[undefined]')

    def __eq__(self, other):
        return self.value == other


class BitField(object):
    zero = None

    @property
    def _ir_val(self):
        return self.value

    def __init__(self, value):
        self.value = value

    def decompose(self):
        result = []
        value = self.value
        for name, mask in self.fields.iteritems():
            if value & mask == mask:
                result.append(name)
        tmp_value = 0
        for name in result:
            tmp_value |= self.fields[name]
        if not result:
            result.append(self.zero)
        remainder = value & ~tmp_value
        return result, remainder

    def __and__(self, other):
        if isinstance(other, BitField):
            return self.__class__(self.value & other.value)
        if isinstance(other, int):
            return self.__class__(self.value & other)
        return NotImplemented

    __rand__ = __and__

    def __or__(self, other):
        if isinstance(other, BitField):
            return self.__class__(self.value | other.value)
        if isinstance(other, int):
            return self.__class__(self.value | other)
        return NotImplemented

    __ror__ = __or__

    def __xor__(self, other):
        if isinstance(other, BitField):
            return self.__class__(self.value ^ other.value)
        if isinstance(other, int):
            return self.__class__(self.value ^ other)
        return NotImplemented

    __rxor__ = __xor__

    def __sub__(self, other):
        if isinstance(other, BitField):
            return self.__class__(self.value - other.value)
        if isinstance(other, int):
            return self.__class__(self.value - other)
        return NotImplemented
    
    def __rsub__(self, other):
        if isinstance(other, int):
            return self.__class__(other - self.value)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, BitField):
            return self.__class__(self.value | other.value)
        if isinstance(other, int):
            return self.__class__(self.value | other)
        return NotImplemented

    __radd__ = __add__

    def __repr__(self):
        components, remainder = self.decompose()
        return '%s(%s)' % (self.__class__.__name__, str(self))

    def __str__(self):
        components, remainder = self.decompose()
        if not remainder:
            return ' | '.join(components)
        return '%s + %s' % (' | '.join(components), remainder)

    def __nonzero__(self):
        return bool(self.value)

    def __index__(self):
        return self.value

    @classmethod
    def add_field(cls, name, value):
        field = cls(value)
        setattr(cls, name, field)
        cls.fields[name] = value
        if not value:
            cls.zero = name

    def __eq__(self, other):
        return self.value == other


class Kind(Enum): pass
Kind.add_field('BAD', libfirm.k_BAD)
Kind.add_field('ENTITY', libfirm.k_entity)
Kind.add_field('TYPE', libfirm.k_type)
Kind.add_field('IR_GRAPH', libfirm.k_ir_graph)
Kind.add_field('IR_NODE', libfirm.k_ir_node)
Kind.add_field('IR_MODE', libfirm.k_ir_mode)
Kind.add_field('TARVAL', libfirm.k_tarval)
Kind.add_field('IR_LOOP', libfirm.k_ir_loop)
Kind.add_field('IR_MAX', libfirm.k_ir_max)

class Relation(BitField): fields = collections.OrderedDict()
Relation.add_field('FALSE', libfirm.ir_relation_false)
Relation.add_field('EQUAL', libfirm.ir_relation_equal)
Relation.add_field('LESS', libfirm.ir_relation_less)
Relation.add_field('GREATER', libfirm.ir_relation_greater)
Relation.add_field('UNORDERED', libfirm.ir_relation_unordered)
Relation.add_field('LESS_EQUAL', libfirm.ir_relation_less_equal)
Relation.add_field('GREATER_EQUAL', libfirm.ir_relation_greater_equal)
Relation.add_field('LESS_GREATER', libfirm.ir_relation_less_greater)
Relation.add_field('LESS_EQUAL_GREATER', libfirm.ir_relation_less_equal_greater)
Relation.add_field('UNORDERED_EQUAL', libfirm.ir_relation_unordered_equal)
Relation.add_field('UNORDERED_LESS', libfirm.ir_relation_unordered_less)
Relation.add_field('UNORDERED_LESS_EQUAL', libfirm.ir_relation_unordered_less_equal)
Relation.add_field('UNORDERED_GREATER', libfirm.ir_relation_unordered_greater)
Relation.add_field('UNORDERED_GREATER_EQUAL', libfirm.ir_relation_unordered_greater_equal)
Relation.add_field('UNORDERED_LESS_GREATER', libfirm.ir_relation_unordered_less_greater)
Relation.add_field('TRUE', libfirm.ir_relation_true)

class Cons(BitField): fields = collections.OrderedDict()
Cons.add_field('NONE', libfirm.cons_none)
Cons.add_field('VOLATILE', libfirm.cons_volatile)
Cons.add_field('UNALIGNED', libfirm.cons_unaligned)
Cons.add_field('FLOATS', libfirm.cons_floats)
Cons.add_field('THROWS_EXCEPTION', libfirm.cons_throws_exception)

class PinState(BitField): fields = collections.OrderedDict()
PinState.add_field('FLOATS', libfirm.op_pin_state_floats)
PinState.add_field('PINNED', libfirm.op_pin_state_pinned)
PinState.add_field('EXC_PINNED', libfirm.op_pin_state_exc_pinned)

class CondJmpPredicate(BitField): fields = collections.OrderedDict()
CondJmpPredicate.add_field('NONE', libfirm.COND_JMP_PRED_NONE)
CondJmpPredicate.add_field('TRUE', libfirm.COND_JMP_PRED_TRUE)
CondJmpPredicate.add_field('FALSE', libfirm.COND_JMP_PRED_FALSE)

class MTPAdditionalProperties(BitField): fields = collections.OrderedDict()
MTPAdditionalProperties.add_field('NO_PROPERTY', libfirm.mtp_no_property)
MTPAdditionalProperties.add_field('PROPERTY_NO_WRITE', libfirm.mtp_property_no_write)
MTPAdditionalProperties.add_field('PROPERTY_PURE', libfirm.mtp_property_pure)
MTPAdditionalProperties.add_field('PROPERTY_NORETURN', libfirm.mtp_property_noreturn)
MTPAdditionalProperties.add_field('PROPERTY_TERMINATES', libfirm.mtp_property_terminates)
MTPAdditionalProperties.add_field('PROPERTY_NOTHROW', libfirm.mtp_property_nothrow)
MTPAdditionalProperties.add_field('PROPERTY_NAKED', libfirm.mtp_property_naked)
MTPAdditionalProperties.add_field('PROPERTY_MALLOC', libfirm.mtp_property_malloc)
MTPAdditionalProperties.add_field('PROPERTY_RETURNS_TWICE', libfirm.mtp_property_returns_twice)
MTPAdditionalProperties.add_field('PROPERTY_PRIVATE', libfirm.mtp_property_private)
MTPAdditionalProperties.add_field('PROPERTY_ALWAYS_INLINE', libfirm.mtp_property_always_inline)
MTPAdditionalProperties.add_field('PROPERTY_NOINLINE', libfirm.mtp_property_noinline)
MTPAdditionalProperties.add_field('PROPERTY_INLINE_RECOMMENDED', libfirm.mtp_property_inline_recommended)
MTPAdditionalProperties.add_field('TEMPORARY', libfirm.mtp_temporary)

class BuiltinKind(Enum): pass
BuiltinKind.add_field('TRAP', libfirm.ir_bk_trap)
BuiltinKind.add_field('DEBUGBREAK', libfirm.ir_bk_debugbreak)
BuiltinKind.add_field('RETURN_ADDRESS', libfirm.ir_bk_return_address)
BuiltinKind.add_field('FRAME_ADDRESS', libfirm.ir_bk_frame_address)
BuiltinKind.add_field('PREFETCH', libfirm.ir_bk_prefetch)
BuiltinKind.add_field('FFS', libfirm.ir_bk_ffs)
BuiltinKind.add_field('CLZ', libfirm.ir_bk_clz)
BuiltinKind.add_field('CTZ', libfirm.ir_bk_ctz)
BuiltinKind.add_field('POPCOUNT', libfirm.ir_bk_popcount)
BuiltinKind.add_field('PARITY', libfirm.ir_bk_parity)
BuiltinKind.add_field('BSWAP', libfirm.ir_bk_bswap)
BuiltinKind.add_field('INPORT', libfirm.ir_bk_inport)
BuiltinKind.add_field('OUTPORT', libfirm.ir_bk_outport)
BuiltinKind.add_field('SATURATING_INCREMENT', libfirm.ir_bk_saturating_increment)
BuiltinKind.add_field('COMPARE_SWAP', libfirm.ir_bk_compare_swap)
BuiltinKind.add_field('MAY_ALIAS', libfirm.ir_bk_may_alias)
BuiltinKind.add_field('VA_START', libfirm.ir_bk_va_start)
BuiltinKind.add_field('VA_ARG', libfirm.ir_bk_va_arg)
BuiltinKind.add_field('LAST', libfirm.ir_bk_last)

class Volatility(BitField): fields = collections.OrderedDict()
Volatility.add_field('NON_VOLATILE', libfirm.volatility_non_volatile)
Volatility.add_field('IS_VOLATILE', libfirm.volatility_is_volatile)

class Align(Enum): pass
Align.add_field('IS_ALIGNED', libfirm.align_is_aligned)
Align.add_field('NON_ALIGNED', libfirm.align_non_aligned)

class EdgeKind(Enum): pass
EdgeKind.add_field('NORMAL', libfirm.EDGE_KIND_NORMAL)
EdgeKind.add_field('FIRST', libfirm.EDGE_KIND_FIRST)
EdgeKind.add_field('BLOCK', libfirm.EDGE_KIND_BLOCK)
EdgeKind.add_field('LAST', libfirm.EDGE_KIND_LAST)

class Verbosity(BitField): fields = collections.OrderedDict()
Verbosity.add_field('ONLYNAMES', libfirm.dump_verbosity_onlynames)
Verbosity.add_field('FIELDS', libfirm.dump_verbosity_fields)
Verbosity.add_field('METHODS', libfirm.dump_verbosity_methods)
Verbosity.add_field('NOSTATIC', libfirm.dump_verbosity_nostatic)
Verbosity.add_field('TYPEATTRS', libfirm.dump_verbosity_typeattrs)
Verbosity.add_field('ENTATTRS', libfirm.dump_verbosity_entattrs)
Verbosity.add_field('ENTCONSTS', libfirm.dump_verbosity_entconsts)
Verbosity.add_field('ACCESSSTATS', libfirm.dump_verbosity_accessStats)
Verbosity.add_field('MAX', libfirm.dump_verbosity_max)

class DumpFlag(BitField): fields = collections.OrderedDict()
DumpFlag.add_field('BLOCKS_AS_SUBGRAPHS', libfirm.ir_dump_flag_blocks_as_subgraphs)
DumpFlag.add_field('WITH_TYPEGRAPH', libfirm.ir_dump_flag_with_typegraph)
DumpFlag.add_field('DISABLE_EDGE_LABELS', libfirm.ir_dump_flag_disable_edge_labels)
DumpFlag.add_field('CONSTS_LOCAL', libfirm.ir_dump_flag_consts_local)
DumpFlag.add_field('IDX_LABEL', libfirm.ir_dump_flag_idx_label)
DumpFlag.add_field('NUMBER_LABEL', libfirm.ir_dump_flag_number_label)
DumpFlag.add_field('KEEPALIVE_EDGES', libfirm.ir_dump_flag_keepalive_edges)
DumpFlag.add_field('OUT_EDGES', libfirm.ir_dump_flag_out_edges)
DumpFlag.add_field('DOMINANCE', libfirm.ir_dump_flag_dominance)
DumpFlag.add_field('LOOPS', libfirm.ir_dump_flag_loops)
DumpFlag.add_field('BACK_EDGES', libfirm.ir_dump_flag_back_edges)
DumpFlag.add_field('IREDGES', libfirm.ir_dump_flag_iredges)
DumpFlag.add_field('ALL_ANCHORS', libfirm.ir_dump_flag_all_anchors)
DumpFlag.add_field('SHOW_MARKS', libfirm.ir_dump_flag_show_marks)
DumpFlag.add_field('NO_ENTITY_VALUES', libfirm.ir_dump_flag_no_entity_values)
DumpFlag.add_field('LD_NAMES', libfirm.ir_dump_flag_ld_names)
DumpFlag.add_field('ENTITIES_IN_HIERARCHY', libfirm.ir_dump_flag_entities_in_hierarchy)

class IROPFlag(BitField): fields = collections.OrderedDict()
IROPFlag.add_field('NONE', libfirm.irop_flag_none)
IROPFlag.add_field('COMMUTATIVE', libfirm.irop_flag_commutative)
IROPFlag.add_field('CFOPCODE', libfirm.irop_flag_cfopcode)
IROPFlag.add_field('FRAGILE', libfirm.irop_flag_fragile)
IROPFlag.add_field('FORKING', libfirm.irop_flag_forking)
IROPFlag.add_field('CONSTLIKE', libfirm.irop_flag_constlike)
IROPFlag.add_field('KEEP', libfirm.irop_flag_keep)
IROPFlag.add_field('START_BLOCK', libfirm.irop_flag_start_block)
IROPFlag.add_field('USES_MEMORY', libfirm.irop_flag_uses_memory)
IROPFlag.add_field('DUMP_NOBLOCK', libfirm.irop_flag_dump_noblock)
IROPFlag.add_field('UNKNOWN_JUMP', libfirm.irop_flag_unknown_jump)
IROPFlag.add_field('CONST_MEMORY', libfirm.irop_flag_const_memory)

class Arity(Enum): pass
Arity.add_field('INVALID', libfirm.oparity_invalid)
Arity.add_field('BINARY', libfirm.oparity_binary)
Arity.add_field('VARIABLE', libfirm.oparity_variable)
Arity.add_field('DYNAMIC', libfirm.oparity_dynamic)
Arity.add_field('ANY', libfirm.oparity_any)

class Resources(BitField): fields = collections.OrderedDict()
Resources.add_field('NONE', libfirm.IR_RESOURCE_NONE)
Resources.add_field('BLOCK_VISITED', libfirm.IR_RESOURCE_BLOCK_VISITED)
Resources.add_field('BLOCK_MARK', libfirm.IR_RESOURCE_BLOCK_MARK)
Resources.add_field('IRN_VISITED', libfirm.IR_RESOURCE_IRN_VISITED)
Resources.add_field('IRN_LINK', libfirm.IR_RESOURCE_IRN_LINK)
Resources.add_field('LOOP_LINK', libfirm.IR_RESOURCE_LOOP_LINK)
Resources.add_field('PHI_LIST', libfirm.IR_RESOURCE_PHI_LIST)

class AliasRelation(BitField): fields = collections.OrderedDict()
AliasRelation.add_field('NO_ALIAS', libfirm.ir_no_alias)
AliasRelation.add_field('MAY_ALIAS', libfirm.ir_may_alias)
AliasRelation.add_field('SURE_ALIAS', libfirm.ir_sure_alias)

class UsageComputed(Enum): pass
UsageComputed.add_field('NOT_COMPUTED', libfirm.ir_entity_usage_not_computed)
UsageComputed.add_field('COMPUTED', libfirm.ir_entity_usage_computed)

class DisambiguatorOptions(BitField): fields = collections.OrderedDict()
DisambiguatorOptions.add_field('NONE', libfirm.aa_opt_none)
DisambiguatorOptions.add_field('ALWAYS_ALIAS', libfirm.aa_opt_always_alias)
DisambiguatorOptions.add_field('TYPE_BASED', libfirm.aa_opt_type_based)
DisambiguatorOptions.add_field('BYTE_TYPE_MAY_ALIAS', libfirm.aa_opt_byte_type_may_alias)
DisambiguatorOptions.add_field('NO_ALIAS', libfirm.aa_opt_no_alias)
DisambiguatorOptions.add_field('INHERITED', libfirm.aa_opt_inherited)

class EntityUsage(BitField): fields = collections.OrderedDict()
EntityUsage.add_field('NONE', libfirm.ir_usage_none)
EntityUsage.add_field('ADDRESS_TAKEN', libfirm.ir_usage_address_taken)
EntityUsage.add_field('WRITE', libfirm.ir_usage_write)
EntityUsage.add_field('READ', libfirm.ir_usage_read)
EntityUsage.add_field('REINTERPRET_CAST', libfirm.ir_usage_reinterpret_cast)
EntityUsage.add_field('UNKNOWN', libfirm.ir_usage_unknown)

class PtrAccessKind(BitField): fields = collections.OrderedDict()
PtrAccessKind.add_field('NONE', libfirm.ptr_access_none)
PtrAccessKind.add_field('READ', libfirm.ptr_access_read)
PtrAccessKind.add_field('WRITE', libfirm.ptr_access_write)
PtrAccessKind.add_field('RW', libfirm.ptr_access_rw)
PtrAccessKind.add_field('STORE', libfirm.ptr_access_store)
PtrAccessKind.add_field('ALL', libfirm.ptr_access_all)

class GraphConstraints(BitField): fields = collections.OrderedDict()
GraphConstraints.add_field('ARCH_DEP', libfirm.IR_GRAPH_CONSTRAINT_ARCH_DEP)
GraphConstraints.add_field('MODEB_LOWERED', libfirm.IR_GRAPH_CONSTRAINT_MODEB_LOWERED)
GraphConstraints.add_field('NORMALISATION2', libfirm.IR_GRAPH_CONSTRAINT_NORMALISATION2)
GraphConstraints.add_field('OPTIMIZE_UNREACHABLE_CODE', libfirm.IR_GRAPH_CONSTRAINT_OPTIMIZE_UNREACHABLE_CODE)
GraphConstraints.add_field('CONSTRUCTION', libfirm.IR_GRAPH_CONSTRAINT_CONSTRUCTION)
GraphConstraints.add_field('TARGET_LOWERED', libfirm.IR_GRAPH_CONSTRAINT_TARGET_LOWERED)
GraphConstraints.add_field('BACKEND', libfirm.IR_GRAPH_CONSTRAINT_BACKEND)

class GraphProperties(BitField): fields = collections.OrderedDict()
GraphProperties.add_field('NONE', libfirm.IR_GRAPH_PROPERTIES_NONE)
GraphProperties.add_field('NO_CRITICAL_EDGES', libfirm.IR_GRAPH_PROPERTY_NO_CRITICAL_EDGES)
GraphProperties.add_field('NO_BADS', libfirm.IR_GRAPH_PROPERTY_NO_BADS)
GraphProperties.add_field('NO_TUPLES', libfirm.IR_GRAPH_PROPERTY_NO_TUPLES)
GraphProperties.add_field('NO_UNREACHABLE_CODE', libfirm.IR_GRAPH_PROPERTY_NO_UNREACHABLE_CODE)
GraphProperties.add_field('ONE_RETURN', libfirm.IR_GRAPH_PROPERTY_ONE_RETURN)
GraphProperties.add_field('CONSISTENT_DOMINANCE', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_DOMINANCE)
GraphProperties.add_field('CONSISTENT_POSTDOMINANCE', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_POSTDOMINANCE)
GraphProperties.add_field('CONSISTENT_DOMINANCE_FRONTIERS', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_DOMINANCE_FRONTIERS)
GraphProperties.add_field('CONSISTENT_OUT_EDGES', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_OUT_EDGES)
GraphProperties.add_field('CONSISTENT_OUTS', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_OUTS)
GraphProperties.add_field('CONSISTENT_LOOPINFO', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_LOOPINFO)
GraphProperties.add_field('CONSISTENT_ENTITY_USAGE', libfirm.IR_GRAPH_PROPERTY_CONSISTENT_ENTITY_USAGE)
GraphProperties.add_field('MANY_RETURNS', libfirm.IR_GRAPH_PROPERTY_MANY_RETURNS)
GraphProperties.add_field('CONTROL_FLOW', libfirm.IR_GRAPH_PROPERTIES_CONTROL_FLOW)
GraphProperties.add_field('ALL', libfirm.IR_GRAPH_PROPERTIES_ALL)

class CallgraphState(BitField): fields = collections.OrderedDict()
CallgraphState.add_field('NONE', libfirm.irp_callgraph_none)
CallgraphState.add_field('CONSISTENT', libfirm.irp_callgraph_consistent)
CallgraphState.add_field('INCONSISTENT', libfirm.irp_callgraph_inconsistent)
CallgraphState.add_field('AND_CALLTREE_CONSISTENT', libfirm.irp_callgraph_and_calltree_consistent)

class Visibility(Enum): pass
Visibility.add_field('EXTERNAL', libfirm.ir_visibility_external)
Visibility.add_field('EXTERNAL_PRIVATE', libfirm.ir_visibility_external_private)
Visibility.add_field('EXTERNAL_PROTECTED', libfirm.ir_visibility_external_protected)
Visibility.add_field('LOCAL', libfirm.ir_visibility_local)
Visibility.add_field('PRIVATE', libfirm.ir_visibility_private)

class Linkage(BitField): fields = collections.OrderedDict()
Linkage.add_field('DEFAULT', libfirm.IR_LINKAGE_DEFAULT)
Linkage.add_field('CONSTANT', libfirm.IR_LINKAGE_CONSTANT)
Linkage.add_field('WEAK', libfirm.IR_LINKAGE_WEAK)
Linkage.add_field('GARBAGE_COLLECT', libfirm.IR_LINKAGE_GARBAGE_COLLECT)
Linkage.add_field('MERGE', libfirm.IR_LINKAGE_MERGE)
Linkage.add_field('HIDDEN_USER', libfirm.IR_LINKAGE_HIDDEN_USER)
Linkage.add_field('NO_CODEGEN', libfirm.IR_LINKAGE_NO_CODEGEN)
Linkage.add_field('NO_IDENTITY', libfirm.IR_LINKAGE_NO_IDENTITY)

class InitializerKind(Enum): pass
InitializerKind.add_field('CONST', libfirm.IR_INITIALIZER_CONST)
InitializerKind.add_field('TARVAL', libfirm.IR_INITIALIZER_TARVAL)
InitializerKind.add_field('NULL', libfirm.IR_INITIALIZER_NULL)
InitializerKind.add_field('COMPOUND', libfirm.IR_INITIALIZER_COMPOUND)

class TypeState(Enum): pass
TypeState.add_field('UNDEFINED', libfirm.layout_undefined)
TypeState.add_field('FIXED', libfirm.layout_fixed)

class DbgAction(Enum): pass
DbgAction.add_field('ERROR,', libfirm.dbg_error,)
DbgAction.add_field('OPT_SSA,', libfirm.dbg_opt_ssa,)
DbgAction.add_field('OPT_AUXNODE,', libfirm.dbg_opt_auxnode,)
DbgAction.add_field('CONST_EVAL,', libfirm.dbg_const_eval,)
DbgAction.add_field('OPT_CSE,', libfirm.dbg_opt_cse,)
DbgAction.add_field('STRAIGHTENING,', libfirm.dbg_straightening,)
DbgAction.add_field('IF_SIMPLIFICATION,', libfirm.dbg_if_simplification,)
DbgAction.add_field('ALGEBRAIC_SIMPLIFICATION,', libfirm.dbg_algebraic_simplification,)
DbgAction.add_field('WRITE_AFTER_WRITE,', libfirm.dbg_write_after_write,)
DbgAction.add_field('WRITE_AFTER_READ,', libfirm.dbg_write_after_read,)
DbgAction.add_field('READ_AFTER_WRITE,', libfirm.dbg_read_after_write,)
DbgAction.add_field('READ_AFTER_READ,', libfirm.dbg_read_after_read,)
DbgAction.add_field('READ_A_CONST,', libfirm.dbg_read_a_const,)
DbgAction.add_field('DEAD_CODE,', libfirm.dbg_dead_code,)
DbgAction.add_field('OPT_CONFIRM,', libfirm.dbg_opt_confirm,)
DbgAction.add_field('GVN_PRE,', libfirm.dbg_gvn_pre,)
DbgAction.add_field('COMBO,', libfirm.dbg_combo,)
DbgAction.add_field('JUMPTHREADING,', libfirm.dbg_jumpthreading,)
DbgAction.add_field('BACKEND,', libfirm.dbg_backend,)
DbgAction.add_field('MAX', libfirm.dbg_max)
