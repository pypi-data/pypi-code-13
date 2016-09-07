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
"""Callbacks for merging and printing debug info.

During its optimisation passes, firm may replace any number of
instructions.  The MergeHandler interface that this module provides
allows you to implement language-specific rules for what should happen
to your dbg_info.

To set up a custom MergeHandler, implement the merge_pair and
merge_sets methods, and then set firm.debug_info.TLS.merge_handler
to an object that implements that interface.

A BaseDbgInfo object is provided that constructs a source location,
which firm uses.  Your dbg_info objects could be a subclass of
BaseDbgInfo; if not, they should be a firm.base.Wrappable that also
has a src_loc attribute of the required C type.
"""

from firm.base import libfirm, ffi, Wrappable
from firm.bitfields import DbgAction
from firm import wrap
import threading

TLS = threading.local()

@ffi.def_extern()
def plf_merge_pair(left, right, dbg_action):
    """Static hook for handling dbg_info when merging pairs of instructions.

    Do not call directly.
    """
    result = merge_handler().merge_pair(left, right,
                                        DbgAction.from_int(dbg_action))
                                      
    if result is None:
        return ffi.NULL
    return result._get_ffi_handle()


@ffi.def_extern()
def plf_merge_sets(new_nodes, n_new_nodes, old_nodes, n_old_nodes, dbg_action):
    """Static hook for handling dbg_info changes when updating subgraphs.

    Do not call directly.
    """
    new_nodes = [wrap.node(new_nodes[i]) for i in xrange(n_new_nodes)]
    old_nodes = [wrap.node(old_nodes[i]) for i in xrange(n_old_nodes)]
    merge_handler().merge_sets(new_nodes, old_nodes,
                               bitfields.DbgAction.from_int(dbg_action))


@ffi.def_extern()
def plf_retrieve_dbg(debug_info):
    """Static hook for getting src_loc from a dbg_info.
    """
    return ffi.from_handle(debug_info).src_loc


@ffi.def_extern()
def plf_retrieve_type_dbg(buf, buf_s, debug_info):
    """Static hook for showing a type.
    """
    try:
        rep = debug_info.show_type
    except AttributeError:
        value = "%*r" % (buf_s - 1, debug_info)
    else:
        value = "%*s" % (buf_s - 1, rep())
    buf[:len(value)] = value
    buf[len(value)] = '\0'


libfirm.dbg_init(libfirm.plf_merge_pair, libfirm.plf_merge_sets)
libfirm.ir_set_debug_retrieve(libfirm.plf_retrieve_dbg)
libfirm.ir_set_type_debug_retrieve(libfirm.plf_retrieve_type_dbg)


def merge_handler():
    try:
        return TLS.merge_handler
    except AttributeError:
        return MergeHandler.default


def BaseDBGInfo(Wrappable):
    def __init__(self, filename, line_no, col_no):
        self.src_loc = ffi.new('src_loc_t')
        self.src_loc.file = filename
        self.src_loc.line_no = line_no
        self.src_loc.col_no = col_no


class MergeHandler(object):
    def merge_pair(self, left, right, dbg_action):
        return left

    def merge_sets(self, new_nodes, old_nodes):
        pass


MergeHandler.default = MergeHandler()
