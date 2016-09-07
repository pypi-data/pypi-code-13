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
class Policy(object):
    def asm(self, input_constraints, output_constraints, clobbers):
        """Get memory node required for an ASM block.
        """

    def post_asm(self, op):
        """Record memory effect of an ASM block.
        """

    def alloc(self, alignment):
        """Get memory node required for a stack alloc.
        """

    def post_alloc(self, op):
        """Record memory effect of a stack alloc.
        """

    def builtin(self, args):
        """Get memory node required for a builtin.
        """

    def post_builtin(self, op):
        """Record memory effect of a builtin.
        """

    def call(self, target, args):
        """Get memory node required for call of target with these args.
        """

    def post_call(self, op):
        """Record memory effect of a call.
        """

    def copyb(self, dest, source, typ, volatility):
        """Get memory node required for a block copy.
        """

    def post_copyb(self, op):
        """Record memory effect of a block copy.
        """

    def div(self, left, right, mode):
        """Get memory node required for division.
        """

    def post_div(self, op):
        """Record memory effect of a division.
        """

    def free(self, ptr):
        """Get memory node required for a stack free.
        """

    def post_free(self, op):
        """Record memory effect of a stack free.
        """

    def load(self, target):
        """Get memory node required for a load of target.
        """

    def post_load(self, op):
        """Record memory effect of a load.
        """

    def mod(self, left, right, mode):
        """Get memory node required for a mod operation.
        """

    def post_mod(self, op):
        """Record memory effect of a mod operation.
        """

    def raise_(self, exception):
        """Get memory node required to raise.
        """

    def post_raise(self, op):
        """Record memory effect of a raise.
        """

    def return_(self, args):
        """Get memory node required for a return.
        """

    def post_return(self, op):
        """Record memory effect of a return.
        """

    def store(self, target):
        """Get memory node required for a store of target.
        """

    def post_store(self, op):
        """Record memory effect of a store.
        """


class CarefulPolicyFactory(object):
    def policy_for(self, block):
        return CarefulPolicy(block)

class CarefulPolicy(Policy):
    def __init__(self, block):
        self.block = block

    def asm(self, input_constraints, output_constraints, clobbers):
        """Get memory node required for an ASM block.
        """
        if 'memory' in clobbers:
            return self.block.store
        else:
            return self.block.op_NoMem()

    def post_asm(self, op):
        """Record memory effect of an ASM block.
        """
        if 'memory' in op.clobbers:
            from firm import types
            self.block.store = self.block.op_Proj(op, types.MODE_M,
                                                  len(op.output_constraints))

    def alloc(self, alignment):
        """Get memory node required for a stack alloc.
        """
        return self.block.store

    def post_alloc(self, op):
        """Record memory effect of a stack alloc.
        """
        self.block.store = op.pn_M

    def builtin(self, args):
        """Get memory node required for a builtin.
        """
        return self.block.store

    def post_builtin(self, op):
        """Record memory effect of a builtin.
        """
        self.block.store = op.pn_M

    def call(self, target, args):
        """Get memory node required for call of target with these args.
        """
        return self.block.store

    def post_call(self, op):
        """Record memory effect of a call.
        """
        self.block.store = op.pn_M

    def copyb(self, dest, source, typ, volatility):
        """Get memory node required for a block copy.
        """
        return self.block.store

    def post_copyb(self, op):
        """Record memory effect of a block copy.
        """
        self.block.store = op

    def div(self, left, right, mode):
        """Get memory node required for division.
        """
        return self.block.store

    def post_div(self, op):
        """Record memory effect of a division.
        """
        self.block.store = op.pn_M

    def free(self, ptr):
        """Get memory node required for a stack free.
        """
        return self.block.store

    def post_free(self, op):
        """Record memory effect of a stack free.
        """
        self.block.store = op

    def load(self, target):
        """Get memory node required for a load of target.
        """
        return self.block.store

    def post_load(self, op):
        """Record memory effect of a load.
        """
        self.block.store = op.pn_M

    def mod(self, left, right, mode):
        """Get memory node required for a mod operation.
        """
        return self.block.store

    def post_mod(self, op):
        """Record memory effect of a mod operation.
        """
        self.block.store = op.pn_M

    def raise_(self, exception):
        """Get memory node required to raise.
        """
        return self.block.store

    def post_raise(self, op):
        """Record memory effect of a raise.
        """
        self.block.store = op.pn_M

    def return_(self, args):
        """Get memory node required for a return.
        """
        return self.block.store

    def post_return(self, op):
        """Record memory effect of a return.
        """
        self.block.store = self.block.op_Bad()

    def store(self, target):
        """Get memory node required for a store of target.
        """
        return self.block.store

    def post_store(self, op):
        """Record memory effect of a store.
        """
        self.block.store = op.pn_M

