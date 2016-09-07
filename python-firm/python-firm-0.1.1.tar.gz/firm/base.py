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
import sys
from _python_firm import lib as libfirm, ffi
libfirm.ir_init()

def ident(name, pattern=None):
    if name is not None:
        return libfirm.new_id_from_str(name)
    return libfirm.id_unique(pattern)


def deident(idnt):
    return ffi.string(libfirm.get_id_str(idnt))


class FirmException(Exception):
    """Generic exception from the FIRM library.
    """


class BaseSequence(object):
    def __init__(self, ir_val):
        self._ir_val = ir_val

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return [self.getitem(i) for i in xrange(*indices)]
        if 0 <= index < len(self):
            return self.getitem(index)
        raise IndexError("%s index out of range" % (type(self).__name__,))

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            if slice.start is None and slice.stop is None and\
                    hasattr(self, 'setall'):
                return self.setall(value)
            return NotImplemented
        if 0 <= index < len(self):
            return self.setitem(index, value)
        raise IndexError("%s index out of range" % (type(self).__name__,))

    def setitem(self, index, value):
        raise TypeError('%r object does not support item assignment' %
                        (type(self).__name__,))

WRAPPABLES = []

class Wrappable(object):
    _ffi_handle = None
    _ffi_keep = True
    def _get_ffi_handle(self):
        if self._ffi_handle is not None:
            return self._ffi_handle
        self._ffi_handle = ffi.from_handle(self)

        if self._ffi_keep:
            WRAPPABLES.append(self)
        return self._ffi_handle


class W(Wrappable):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'w[%r]' % (self.value,)

if sys.version_info.major > 2:
    def ffi_to_repr(s):
        return s.decode('latin1')
else:
    def ffi_to_repr(s):
        return s
