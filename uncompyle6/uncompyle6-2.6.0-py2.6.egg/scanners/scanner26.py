#  Copyright (c) 2015, 2016 by Rocky Bernstein
#  Copyright (c) 2005 by Dan Pascu <dan@windowmaker.org>
#  Copyright (c) 2000-2002 by hartmut Goebel <h.goebel@crazy-compilers.com>
#  Copyright (c) 1999 John Aycock
"""
Python 2.6 bytecode scanner

This overlaps Python's 2.6's dis module, but it can be run from Python 3 and
other versions of Python. Also, we save token information for later
use in deparsing.
"""

import sys
from uncompyle6 import PYTHON3
if PYTHON3:
    intern = sys.intern

from xdis.bytecode import findlinestarts
import uncompyle6.scanners.scanner2 as scan

# bytecode verification, verify(), uses JUMP_OPs from here
from xdis.opcodes import opcode_26
JUMP_OPs = opcode_26.JUMP_OPs

class Scanner26(scan.Scanner2):
    def __init__(self, show_asm=False):
        super(Scanner26, self).__init__(2.6, show_asm)
        self.stmt_opcodes = frozenset([
            self.opc.SETUP_LOOP,       self.opc.BREAK_LOOP,
            self.opc.SETUP_FINALLY,    self.opc.END_FINALLY,
            self.opc.SETUP_EXCEPT,     self.opc.POP_BLOCK,
            self.opc.STORE_FAST,       self.opc.DELETE_FAST,
            self.opc.STORE_DEREF,      self.opc.STORE_GLOBAL,
            self.opc.DELETE_GLOBAL,    self.opc.STORE_NAME,
            self.opc.DELETE_NAME,      self.opc.STORE_ATTR,
            self.opc.DELETE_ATTR,      self.opc.STORE_SUBSCR,
            self.opc.DELETE_SUBSCR,    self.opc.RETURN_VALUE,
            self.opc.RAISE_VARARGS,    self.opc.POP_TOP,
            self.opc.PRINT_EXPR,       self.opc.PRINT_ITEM,
            self.opc.PRINT_NEWLINE,    self.opc.PRINT_ITEM_TO,
            self.opc.PRINT_NEWLINE_TO, self.opc.CONTINUE_LOOP,
            self.opc.JUMP_ABSOLUTE,    self.opc.EXEC_STMT,
        ])

        # "setup" opcodes
        self.setup_ops = frozenset([
            self.opc.SETUP_EXCEPT, self.opc.SETUP_FINALLY,
            ])

        # opcodes with expect a variable number pushed values whose
        # count is in the opcode. For parsing we generally change the
        # opcode name to include that number.
        self.varargs_ops = frozenset([
            self.opc.BUILD_LIST,           self.opc.BUILD_TUPLE,
            self.opc.BUILD_SLICE,          self.opc.UNPACK_SEQUENCE,
            self.opc.MAKE_FUNCTION,        self.opc.CALL_FUNCTION,
            self.opc.MAKE_CLOSURE,         self.opc.CALL_FUNCTION_VAR,
            self.opc.CALL_FUNCTION_KW,     self.opc.CALL_FUNCTION_VAR_KW,
            self.opc.DUP_TOPX,             self.opc.RAISE_VARARGS])

        # opcodes that store values into a variable
        self.designator_ops = frozenset([
            self.opc.STORE_FAST,    self.opc.STORE_NAME,
            self.opc.STORE_GLOBAL,  self.opc.STORE_DEREF,   self.opc.STORE_ATTR,
            self.opc.STORE_SLICE_0, self.opc.STORE_SLICE_1, self.opc.STORE_SLICE_2,
            self.opc.STORE_SLICE_3, self.opc.STORE_SUBSCR,  self.opc.UNPACK_SEQUENCE,
            self.opc.JA
        ])

        # Python 2.7 has POP_JUMP_IF_{TRUE,FALSE}_OR_POP but < 2.7 doesn't
        # Add an empty set make processing more uniform.
        self.pop_jump_if_or_pop = frozenset([])
        return

    def disassemble(self, co, classname=None, code_objects={}, show_asm=None):
        '''
        Disassemble a code object, returning a list of 'Token'.

        The main part of this procedure is modelled after
        dis.disassemble().
        '''

        show_asm = self.show_asm if not show_asm else show_asm
        if show_asm in ('both', 'before'):
            from xdis.bytecode import Bytecode
            bytecode = Bytecode(co, self.opc)
            for instr in bytecode.get_instructions(co):
                print(instr._disassemble())

        # from xdis.bytecode import Bytecode
        # bytecode = Bytecode(co, self.opc)
        # for instr in bytecode.get_instructions(co):
        #     print(instr._disassemble())

        # Container for tokens
        tokens = []

        customize = {}
        Token = self.Token # shortcut

        n = self.setup_code(co)

        self.build_lines_data(co, n-1)

        # linestarts contains block code adresses (addr,block)
        self.linestarts = list(findlinestarts(co))

        # class and names
        if classname:
            classname = '_' + classname.lstrip('_') + '__'

            def unmangle(name):
                if name.startswith(classname) and name[-2:] != '__':
                    return name[len(classname) - 2:]
                return name

            free = [ unmangle(name) for name in (co.co_cellvars + co.co_freevars) ]
            names = [ unmangle(name) for name in co.co_names ]
            varnames = [ unmangle(name) for name in co.co_varnames ]
        else:
            free = co.co_cellvars + co.co_freevars
            names = co.co_names
            varnames = co.co_varnames
        self.names = names

        # list of instruction to remove/add or change to match with bytecode 2.7
        self.toChange = []
        # Rocky: the restructure code isn't adjusting linestarts
        # and this causes problems
        # self.restructBytecode()
        codelen = len(self.code)

        self.build_prev_op(codelen)

        self.load_asserts = set()
        for i in self.op_range(0, codelen):
            if (self.code[i] == self.opc.JUMP_IF_TRUE and
                i + 4 < codelen and
                self.code[i+3] == self.opc.POP_TOP and
                self.code[i+4] == self.opc.LOAD_GLOBAL):
                if names[self.get_argument(i+4)] == 'AssertionError':
                    self.load_asserts.add(i+4)

        cf = self.find_jump_targets()
        # contains (code, [addrRefToCode])

        last_stmt = self.next_stmt[0]
        i = self.next_stmt[last_stmt]
        replace = {}
        while i < codelen - 1:
            if self.lines[last_stmt].next > i:
                if self.code[last_stmt] == self.opc.PRINT_ITEM:
                    if self.code[i] == self.opc.PRINT_ITEM:
                        replace[i] = 'PRINT_ITEM_CONT'
                    elif self.code[i] == self.opc.PRINT_NEWLINE:
                        replace[i] = 'PRINT_NEWLINE_CONT'
            last_stmt = i
            i = self.next_stmt[i]

        imports = self.all_instr(0, codelen,
                                (self.opc.IMPORT_NAME, self.opc.IMPORT_FROM,
                                 self.opc.IMPORT_STAR))
        if len(imports) > 1:
            last_import = imports[0]
            for i in imports[1:]:
                if self.lines[last_import].next > i:
                    if self.code[last_import] == self.opc.IMPORT_NAME == self.code[i]:
                        replace[i] = 'IMPORT_NAME_CONT'
                last_import = i

        extended_arg = 0
        for offset in self.op_range(0, codelen):
            op = self.code[offset]
            op_name = self.opname[op]
            oparg = None; pattr = None

            if offset in cf:
                k = 0
                for j in cf[offset]:
                    tokens.append(Token('COME_FROM', None, repr(j),
                                    offset="%s_%d" % (offset, k) ))
                    k += 1

            if self.op_hasArgument(op):
                oparg = self.get_argument(offset) + extended_arg
                extended_arg = 0
                if op == self.opc.EXTENDED_ARG:
                    raise NotImplementedError
                    extended_arg = oparg * scan.L65536
                    continue
                if op in self.opc.hasconst:
                    const = co.co_consts[oparg]
                    # We can't use inspect.iscode() because we may be
                    # using a different version of Python than the
                    # one that this was byte-compiled on. So the code
                    # types may mismatch.
                    if hasattr(const, 'co_name'):
                        oparg = const
                        if const.co_name == '<lambda>':
                            assert op_name == 'LOAD_CONST'
                            op_name = 'LOAD_LAMBDA'
                        elif const.co_name == '<genexpr>':
                            op_name = 'LOAD_GENEXPR'
                        elif const.co_name == '<dictcomp>':
                            op_name = 'LOAD_DICTCOMP'
                        elif const.co_name == '<setcomp>':
                            op_name = 'LOAD_SETCOMP'
                        # verify uses 'pattr' for comparison, since 'attr'
                        # now holds Code(const) and thus can not be used
                        # for comparison (todo: think about changing this)
                        # pattr = 'code_object @ 0x%x %s->%s' % \
                        # (id(const), const.co_filename, const.co_name)
                        pattr = '<code_object ' + const.co_name + '>'
                    else:
                        pattr = const
                elif op in self.opc.hasname:
                    pattr = names[oparg]
                elif op in self.opc.hasjrel:
                    pattr = repr(offset + 3 + oparg)
                    if op == self.opc.JUMP_FORWARD:
                        target = self.get_target(offset)
                        if target > offset and self.code[target] == self.opc.RETURN_VALUE:
                            # Python 2.5 sometimes has this
                            op_name = 'JUMP_RETURN'
                        # FIXME: this is a hack to catch stuff like:
                        #   if x: continue
                        # the "continue" is not on a new line.
                        if tokens[-1].type == 'JUMP_BACK':
                            tokens[-1].type = intern('CONTINUE')

                elif op in self.opc.hasjabs:
                    pattr = repr(oparg)
                elif op in self.opc.haslocal:
                    pattr = varnames[oparg]
                elif op in self.opc.hascompare:
                    pattr = self.opc.cmp_op[oparg]
                elif op in self.opc.hasfree:
                    pattr = free[oparg]
            if offset in self.toChange:
                if (self.code[offset] == self.opc.JA and
                    self.code[oparg] == self.opc.WITH_CLEANUP):
                    op_name = 'SETUP_WITH'
                    cf[oparg] = cf.get(oparg, []) + [offset]
            if op in self.varargs_ops:
                # CE - Hack for >= 2.5
                #      Now all values loaded via LOAD_CLOSURE are packed into
                #      a tuple before calling MAKE_CLOSURE.
                if (op == self.opc.BUILD_TUPLE and
                    self.code[self.prev[offset]] == self.opc.LOAD_CLOSURE):
                    continue
                else:
                    op_name = '%s_%d' % (op_name, oparg)
                    if op != self.opc.BUILD_SLICE:
                        customize[op_name] = oparg
            elif op == self.opc.JA:
                target = self.get_target(offset)
                if target < offset:
                    if (offset in self.stmts
                        and self.code[offset+3] not in (self.opc.END_FINALLY,
                                                          self.opc.POP_BLOCK)
                        and offset not in self.not_continue):
                        op_name = 'CONTINUE'
                    else:
                        op_name = 'JUMP_BACK'
                        # FIXME: this is a hack to catch stuff like:
                        #   if x: continue
                        # the "continue" is not on a new line.
                        if tokens[-1].type == 'JUMP_BACK':
                            tokens[-1].type = intern('CONTINUE')

            elif op == self.opc.LOAD_GLOBAL:
                if offset in self.load_asserts:
                    op_name = 'LOAD_ASSERT'
            elif op == self.opc.RETURN_VALUE:
                if offset in self.return_end_ifs:
                    op_name = 'RETURN_END_IF'

            if offset in self.linestartoffsets:
                linestart = self.linestartoffsets[offset]
            else:
                linestart = None

            if offset not in replace:
                tokens.append(Token(op_name, oparg, pattr, offset, linestart))
            else:
                tokens.append(Token(replace[offset], oparg, pattr, offset, linestart))
                pass
            pass

        if show_asm:
            for t in tokens:
                print(t)
            print()
        return tokens, customize

if __name__ == "__main__":
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 2.6:
        import inspect
        co = inspect.currentframe().f_code
        tokens, customize = Scanner26(show_asm=True).disassemble(co)
    else:
        print("Need to be Python 2.6 to demo; I am %s." %
              PYTHON_VERSION)
