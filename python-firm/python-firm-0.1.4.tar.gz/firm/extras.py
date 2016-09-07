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
from firm.base import libfirm, ffi, BaseSequence
from firm.operations import ASM

class _Clobbers(BaseSequence):
    def __len__(self):
        return libfirm.get_ASM_n_clobbers(self._ir_val)

    def getitem(self, index):
        clobber_array = libfirm.get_ASM_clobbers(self._ir_val)
        return ffi.string(libfirm.get_id_str(clobber_array[index]))


class _InputConstraints(BaseSequence):
    def __len__(self):
        return libfirm.get_ASM_n_input_(self._ir_val)

    def getitem(self, index):
        constraint_array = libfirm.get_ASM_input_constraints(self._ir_val)
        return constraint_array[index]


class _OutputConstraints(BaseSequence):
    def __len__(self):
        return libfirm.get_ASM_n_output_constraints(self._ir_val)

    def getitem(self, index):
        constraint_array = libfirm.get_ASM_output_constraints(self._ir_val)
        return constraint_array[index]


def clobbers(self):
    return _Clobbers(self._ir_node)

def output_constraints(self):
    return _OutputConstraints(self._ir_node)

def input_constraints(self):
    return _InputConstraints(self._ir_node)

def text(self):
    return ffi.string(libfirm.get_id_str(libfirm.get_ASM_text(self._ir_node)))


ASM.clobbers = property(clobbers)
ASM.output_constraints = property(output_constraints)
ASM.input_constraints = property(input_constraints)
ASM.text = property(text)


