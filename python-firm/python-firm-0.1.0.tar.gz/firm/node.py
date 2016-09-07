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
from firm.base import libfirm, BaseSequence
import firm.wrap as wrap

class _Predecessors(BaseSequence):
    def __len__(self):
        return libfirm.get_irn_arity(self._ir_val)

    def getitem(self, index):
        return wrap.node(libfirm.get_irn_n(self._ir_val, index))
        
    def setitem(self, index, value):
        libfirm.set_irn_n(self._ir_val, index, value._ir_node)

    def setall(self, value):
        libfirm.set_irn_in(self._ir_val, len(value), value)


class BaseNode(object):
    @property
    def _ir_val(self):
        return self._ir_node

    def __init__(self, ir_node):
        self._ir_node = ir_node

    @property
    def predecessors(self):
        return _Predecessors(self._ir_node)

    def get_mode(self):
        return libfirm.get_irn_mode(self._ir_node)

    def set_mode(self, mode):
        libfirm.set_irn_mode(self._ir_node, mode)

    # note that there is no 'mode' property, as it could cause
    # confusion when the class defines the mode.

    @property
    def op(self):
        return libfirm.get_irn_op(self._ir_node)

    def get_visited(self):
        return Visited(libfirm.get_irn_visited(self._ir_node))

    def set_visited(self, value):
        libfirm.set_irn_visited(value._ir_visited)

    visited = property(get_visited, set_visited)

    def get_link(self):
        return libfirm.get_irn_link(self._ir_node)

    def set_link(self, value):
        libfirm.set_irn_link(self._ir_node, value)

    link = property(get_link, set_link)

    @property
    def graph(self):
        # TODO: push graphs through the initialiser for customisation
        from firm.function import IRGraph
        return IRGraph(libfirm.get_irn_irg(self._ir_node))

    @property
    def node_nr(self):
        return libfirm.get_irn_node_nr(self._ir_node)

    def get_pinned(self):
        return libfirm.get_irn_pinned(self._ir_node)

    def set_pinned(self, value):
        libfirm.set_irn_pinned(self._ir_node, value)

    pinned = property(get_pinned, set_pinned)

    def get_block(self):
        # TODO: push graphs through the initialiser for customisation
        from firm.function import Block
        if isinstance(self, Block):
            return self
        return Block(libfirm.get_nodes_block(self._ir_node))

    def set_block(self, block):
        libfirm.set_nodes_block(self._ir_node, block._ir_block)

    block = property(get_block, set_block)

    def keep_alive(self):
        libfirm.keep_alive(self._ir_node)


class Binop(BaseNode): pass
class EntConst(BaseNode): pass
class TypeConst(BaseNode): pass

"""
class Fragile(BaseNode):
    @property
    def is_x_except_Proj(self):
        return libfirm.is_x_except_Proj(self._ir_node)

    @property
    def is_x_regular_Proj(self):
        return libfirm.is_x_regular_Proj(self._ir_node)


class BinOp(BaseNode):
    def get_binop_left(self):
        return wrap.node(libfirm.get_binop_left(self._ir_node))

    def set_binop_left(self, node):
        libfirm.set_binop_left(self._ir_node, node._ir_node)

    left = property(get_binop_left, set_binop_left)

    def get_binop_right(self):
        return wrap.node(libfirm.get_binop_right(self._ir_node))

    def set_binop_right(self, node):
        libfirm.set_binop_right(self._ir_node, node._ir_node)

    right = property(get_binop_right, set_binop_right)
"""
