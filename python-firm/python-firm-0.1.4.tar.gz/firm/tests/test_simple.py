import sys
from firm import types, function
from firm.base import libfirm, ffi
from firm.types import Method, INT_32, MODE_IS
from firm.function import Function, IRGraph
from firm.bitfields import Relation

def test_simple():
    sig = Method.new([INT_32] * 3, [INT_32])
    func = Function.new(sig, b"simple")
    graph = IRGraph.new(func, 3)
    block = graph.current_block
    tarval_7 = libfirm.new_integer_tarval_from_str(b"7", 1, 0, 10, MODE_IS)
    v0 = block.op_Add(graph.arg(0, MODE_IS), graph.arg(1, MODE_IS))
    v1 = block.op_Add(graph.arg(1, MODE_IS), graph.arg(2, MODE_IS))
    v3 = block.op_Mul(v0, v1)
    v4 = block.op_Sub(v3, block.op_Const(tarval_7))
    block.op_return(v4)
    block.mature()
    graph.finalise()
    graph.verify()


def test_diamond_control():
    sig = Method.new([INT_32] * 3, [INT_32])
    func = Function.new(sig, b"diamond")
    graph = IRGraph.new(func, 3)

    block = graph.current_block
    tarval_7 = libfirm.new_integer_tarval_from_str(b"7", 1, 0, 10, MODE_IS)
    v0 = block.op_Add(graph.arg(0, MODE_IS), graph.arg(1, MODE_IS))
    v1 = block.op_Cmp(v0, graph.arg(2, MODE_IS), Relation.LESS)
    v2 = block.op_Cond(v1)

    b_true = graph.op_Block([v2.pn_true])
    b_false = graph.op_Block([v2.pn_false])

    v3 = b_true.op_Mul(v0, graph.arg(2, MODE_IS))
    tj = b_true.op_Jmp()

    v4 = b_false.op_Sub(v0, block.op_Const(tarval_7))
    fj = b_false.op_Jmp()

    ret_block = graph.op_Block([tj, fj])
    v5 = ret_block.op_Phi([v3, v4], MODE_IS)
    ret_block.op_return(v5)

    block.mature()
    b_true.mature()
    b_false.mature()
    ret_block.mature()

    graph.finalise()
    graph.verify()


def test_asm():
    sig = Method.new([INT_32] * 3, [INT_32])
    func = Function.new(sig, b"asm")
    graph = IRGraph.new(func, 3)

    block = graph.current_block
    register = libfirm.new_id_from_str(b'r')
    in_constraint0 = [0, register, MODE_IS]
    in_constraint1 = [1, register, MODE_IS]
    out_constraint1 =[0, register, MODE_IS]
    asm = block.op_ASM([graph.arg(0, MODE_IS), graph.arg(2, MODE_IS)],
                       [in_constraint0, in_constraint1], [out_constraint1],
                       [b'memory'],
                       b"firm %0, %1 /* do a thing */")

    block.op_return(block.op_Proj(asm, MODE_IS, 0))
    block.mature()

    graph.finalise()
    graph.verify() # TODO:  check the comment got inserted into the .S
