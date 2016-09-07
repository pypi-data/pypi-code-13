# Warning: this module is generated code.

from firm.base import libfirm, ffi, BaseSequence
from firm.node import BaseNode, Binop, EntConst, TypeConst
from firm import types, wrap


class NodeBuilder(object):

    def op_ASM(self, args, input_constraints, output_constraints, clobbers, text):
        """executes assembler fragments of the target machine.

	The node contains a template for an assembler snippet. The compiler will
	replace occurences of %0 to %9 with input/output registers,
	%% with a single % char. Some backends allow additional specifiers (for
	example %w3, %l3, %h3 on x86 to get a 16bit, 8hit low, 8bit high part
	of a register).
	After the replacements the text is emitted into the final assembly.

	The clobber list contains names of registers which have an undefined value
	after the assembler instruction is executed; it may also contain 'memory'
	or 'cc' if global state/memory changes or the condition code registers
	(some backends implicitely set cc, memory clobbers on all ASM statements).

	Example (an i386 instruction)::

		ASM(text="btsl %1, %0",
			input_constraints = ["=m", "r"],
			clobbers = ["cc"])

	As there are no output, the %0 references the first input which is just an
	address which the asm operation writes to. %1 references to an input which
	is passed as a register. The condition code register has an unknown value
	after the instruction.

	(This format is inspired by the gcc extended asm syntax)
	
    
        @param irn_mem mem
        @param arity size of additional inputs array
        @param in additional inputs
        @param input_constraints input constraints
        @param n_output_constraints number of output constraints
        @param output_constraints output constraints
        @param n_clobbers number of clobbered registers/memory
        @param clobbers list of clobbered registers/memory
        @param text assembler text
        """
        irn_mem = self.memory_policy.asm(input_constraints, output_constraints, clobbers)
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_ASM(self._debug,
            self.block._ir_block, irn_mem._ir_node, len(args), arg_array, input_constraints, len(output_constraints), output_constraints, len(clobbers), ffi.new("ident*[]", list(map(libfirm.new_id_from_str, clobbers))), libfirm.new_id_from_str(text))

        op = ASM(res)
        self.memory_policy.post_asm(op)
        return op

    def op_Add(self, irn_left, irn_right):
        """returns the sum of its operands
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Add(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Add(res)

    def op_Address(self, entity):
        """Symbolic constant that represents the address of an entity (variable or method)
    
        @param entity entity to operate on
        """
        res = libfirm.new_rd_Address(self._debug,
            self.graph._ir_graph, entity._ir_entity)

        return Address(res)

    def op_Align(self, mode, type):
        """A symbolic constant that represents the alignment of a type
    
        @param mode mode of the operations result
        @param type type to operate on
        """
        res = libfirm.new_rd_Align(self._debug,
            self.graph._ir_graph, mode, type._ir_type)

        return Align(res)

    def op_Alloc(self, irn_size, alignment, irn_mem=None):
        """Allocates a block of memory on the stack.
    
        @param irn_mem mem
        @param irn_size size
        @param alignment alignment of the memory block (must be a power of 2)
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.alloc(alignment)
        res = libfirm.new_rd_Alloc(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_size._ir_node, alignment)

        op = Alloc(res)
        self.memory_policy.post_alloc(op)
        return op

    def op_Anchor(self, irn_end_block, irn_start_block, irn_end, irn_start, irn_frame, irn_initial_mem, irn_args, irn_no_mem):
        """Utility node used to "hold" nodes in a graph that might possibly not be
	reachable by other means or which should be reachable immediately without
	searching through the graph.
	Each firm-graph contains exactly one anchor node whose address is always
	known. All other well-known graph-nodes like Start, End, NoMem, ...
	are found by looking at the respective Anchor operand.
    
        @param irn_end_block end_block
        @param irn_start_block start_block
        @param irn_end end
        @param irn_start start
        @param irn_frame frame
        @param irn_initial_mem initial_mem
        @param irn_args args
        @param irn_no_mem no_mem
        """
        res = libfirm.new_rd_Anchor(self._debug,
            self.block._ir_block, irn_end_block._ir_node, irn_start_block._ir_node, irn_end._ir_node, irn_start._ir_node, irn_frame._ir_node, irn_initial_mem._ir_node, irn_args._ir_node, irn_no_mem._ir_node)

        return Anchor(res)

    def op_And(self, irn_left, irn_right):
        """returns the result of a bitwise and operation of its operands
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_And(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return And(res)

    def op_Bad(self, mode):
        """Bad nodes indicate invalid input, which is values which should never be
	computed.

	The typical use case for the Bad node is removing unreachable code.
	Frontends should set the current_block to Bad when it is clear that
	following code must be unreachable (ie. after a goto or return statement).
	Optimizations also set block predecessors to Bad when it becomes clear,
	that a control flow edge can never be executed.

	The gigo optimizations ensures that nodes with Bad as their block, get
	replaced by Bad themselves. Nodes with at least 1 Bad input get exchanged
	with Bad too. Exception to this rule are Block, Phi, Tuple and End node;
	This is because removing inputs from a Block is hairy operation (requiring,
	Phis to be shortened too for example). So instead of removing block inputs
	they are set to Bad, and the actual removal is left to the control flow
	optimization phase. Block, Phi, Tuple with only Bad inputs however are
	replaced by Bad right away.

	In the future we may use the Bad node to model poison values that arise
	from undefined behaviour like reading uninitialized local variables in C.
    
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Bad(self._debug,
            self.graph._ir_graph, mode)

        return Bad(res)

    def op_Bitcast(self, irn_op, mode):
        """Converts a value between modes with different arithmetics but same
	number of bits by reinterpreting the bits in the new mode
    
        @param irn_op op
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Bitcast(self._debug,
            self.block._ir_block, irn_op._ir_node, mode)

        return Bitcast(res)

    def op_Block(self, args):
        """A basic block
    
        @param arity size of additional inputs array
        @param in additional inputs
        """
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Block(self._debug,
            self.graph._ir_graph, len(args), arg_array)

        return Block(res)

    def op_Builtin(self, args, kind, type):
        """performs a backend-specific builtin.
    
        @param irn_mem mem
        @param arity size of additional inputs array
        @param in additional inputs
        @param kind kind of builtin
        @param type method type for the builtin call
        """
        irn_mem = self.memory_policy.builtin(args)
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Builtin(self._debug,
            self.block._ir_block, irn_mem._ir_node, len(args), arg_array, kind.value, type._ir_type)

        op = Builtin(res)
        self.memory_policy.post_builtin(op)
        return op

    def op_Call(self, irn_ptr, args, type):
        """Calls other code. Control flow is transfered to ptr, additional
	operands are passed to the called code. Called code usually performs a
	return operation. The operands of this return operation are the result
	of the Call node.
    
        @param irn_mem mem
        @param irn_ptr ptr
        @param arity size of additional inputs array
        @param in additional inputs
        @param type type of the call (usually type of the called procedure)
        """
        irn_mem = self.memory_policy.call(irn_ptr, args)
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Call(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_ptr._ir_node, len(args), arg_array, type._ir_type)

        op = Call(res)
        self.memory_policy.post_call(op)
        return op

    def op_Cmp(self, irn_left, irn_right, relation):
        """Compares its two operands and checks whether a specified
	   relation (like less or equal) is fulfilled.
    
        @param irn_left left
        @param irn_right right
        @param relation Comparison relation
        """
        res = libfirm.new_rd_Cmp(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node, relation.value)

        return Cmp(res)

    def op_Cond(self, irn_selector):
        """Conditionally change control flow.
    
        @param irn_selector selector
        """
        res = libfirm.new_rd_Cond(self._debug,
            self.block._ir_block, irn_selector._ir_node)

        return Cond(res)

    def op_Confirm(self, irn_value, irn_bound, relation):
        """Specifies constraints for a value. This allows explicit representation
	of path-sensitive properties. (Example: This value is always >= 0 on 1
	if-branch then all users within that branch are rerouted to a confirm-node
	specifying this property).

	A constraint is specified for the relation between value and bound.
	value is always returned.
	Note that this node does NOT check or assert the constraint, it merely
	specifies it.
    
        @param irn_value value
        @param irn_bound bound
        @param relation relation of value to bound
        """
        res = libfirm.new_rd_Confirm(self._debug,
            self.block._ir_block, irn_value._ir_node, irn_bound._ir_node, relation.value)

        return Confirm(res)

    def op_Const(self, tarval):
        """Returns a constant value.
    
        @param tarval constant value (a tarval object)
        """
        res = libfirm.new_rd_Const(self._debug,
            self.graph._ir_graph, tarval)

        return Const(res)

    def op_Conv(self, irn_op, mode):
        """Converts values between modes
    
        @param irn_op op
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Conv(self._debug,
            self.block._ir_block, irn_op._ir_node, mode)

        return Conv(res)

    def op_CopyB(self, irn_dst, irn_src, type, flags, irn_mem=None):
        """Copies a block of memory with statically known size/type.
    
        @param irn_mem mem
        @param irn_dst dst
        @param irn_src src
        @param type type of copied data
        @param flags specifies volatility
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.copyb(irn_dst, irn_src, type, volatility)
        res = libfirm.new_rd_CopyB(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_dst._ir_node, irn_src._ir_node, type._ir_type, flags)

        op = CopyB(res)
        self.memory_policy.post_copyb(op)
        return op

    def op_Deleted(self, ):
        """Internal node which is temporary set to nodes which are already removed
	from the graph.
    
        """
        res = libfirm.new_rd_Deleted(self._debug,
            self.block._ir_block)

        return Deleted(res)

    def op_Div(self, irn_left, irn_right, pinned, irn_mem=None):
        """returns the quotient of its 2 operands
    
        @param irn_mem mem
        @param irn_left left
        @param irn_right right
        @param pinned pinned state
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.div(irn_left, irn_right, mode)
        res = libfirm.new_rd_Div(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_left._ir_node, irn_right._ir_node, pinned)

        op = Div(res)
        self.memory_policy.post_div(op)
        return op

    def op_Dummy(self, mode):
        """A placeholder value. This is used when constructing cyclic graphs where
	you have cases where not all predecessors of a phi-node are known. Dummy
	nodes are used for the unknown predecessors and replaced later.
    
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Dummy(self._debug,
            self.graph._ir_graph, mode)

        return Dummy(res)

    def op_End(self, args):
        """Last node of a graph. It references nodes in endless loops (so called
	keepalive edges)
    
        @param arity size of additional inputs array
        @param in additional inputs
        """
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_End(self._debug,
            self.graph._ir_graph, len(args), arg_array)

        return End(res)

    def op_Eor(self, irn_left, irn_right):
        """returns the result of a bitwise exclusive or operation of its operands.

	This is also known as the Xor operation.
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Eor(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Eor(res)

    def op_Free(self, irn_ptr, irn_mem=None):
        """Frees a block of memory previously allocated by an Alloc node
    
        @param irn_mem mem
        @param irn_ptr ptr
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.free(irn_ptr)
        res = libfirm.new_rd_Free(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_ptr._ir_node)

        op = Free(res)
        self.memory_policy.post_free(op)
        return op

    def op_IJmp(self, irn_target):
        """Jumps to the code in its argument. The code has to be in the same
	function and the destination must be one of the blocks reachable
	by the tuple results
    
        @param irn_target target
        """
        res = libfirm.new_rd_IJmp(self._debug,
            self.block._ir_block, irn_target._ir_node)

        return IJmp(res)

    def op_Id(self, irn_pred, mode):
        """Returns its operand unchanged.

	This is mainly used when exchanging nodes. Usually you shouldn't see Id
	nodes since the getters/setters for node inputs skip them automatically.
    
        @param irn_pred pred
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Id(self._debug,
            self.block._ir_block, irn_pred._ir_node, mode)

        return Id(res)

    def op_Jmp(self, ):
        """Jumps to the block connected through the out-value
    
        """
        res = libfirm.new_rd_Jmp(self._debug,
            self.block._ir_block)

        return Jmp(res)

    def op_Load(self, irn_ptr, mode, type, flags, irn_mem=None):
        """Loads a value from memory (heap or stack).
    
        @param irn_mem mem
        @param irn_ptr ptr
        @param mode mode of the value to be loaded
        @param type The type of the object which is stored at ptr (need not match with mode)
        @param flags specifies alignment, volatility and pin state
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.load(irn_ptr)
        res = libfirm.new_rd_Load(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_ptr._ir_node, mode, type._ir_type, flags)

        op = Load(res)
        self.memory_policy.post_load(op)
        return op

    def op_Member(self, irn_ptr, entity):
        """Computes the address of a compound type member given the base address
	of an instance of the compound type.

	A Member node must only produce a NULL pointer if the ptr input is NULL.
    
        @param irn_ptr ptr
        @param entity entity which is selected
        """
        res = libfirm.new_rd_Member(self._debug,
            self.block._ir_block, irn_ptr._ir_node, entity._ir_entity)

        return Member(res)

    def op_Minus(self, irn_op):
        """returns the additive inverse of its operand
    
        @param irn_op op
        """
        res = libfirm.new_rd_Minus(self._debug,
            self.block._ir_block, irn_op._ir_node)

        return Minus(res)

    def op_Mod(self, irn_left, irn_right, pinned, irn_mem=None):
        """returns the remainder of its operands from an implied division.

	Examples:

	* mod(5,3)   produces 2
	* mod(5,-3)  produces 2
	* mod(-5,3)  produces -2
	* mod(-5,-3) produces -2
	
    
        @param irn_mem mem
        @param irn_left left
        @param irn_right right
        @param pinned pinned state
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.mod(irn_left, irn_right, resmode)
        res = libfirm.new_rd_Mod(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_left._ir_node, irn_right._ir_node, pinned)

        op = Mod(res)
        self.memory_policy.post_mod(op)
        return op

    def op_Mul(self, irn_left, irn_right):
        """returns the product of its operands
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Mul(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Mul(res)

    def op_Mulh(self, irn_left, irn_right):
        """returns the upper word of the product of its operands (the part which
	would not fit into the result mode of a normal Mul anymore)
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Mulh(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Mulh(res)

    def op_Mux(self, irn_sel, irn_false, irn_true):
        """returns the false or true operand depending on the value of the sel
	operand
    
        @param irn_sel sel
        @param irn_false false
        @param irn_true true
        """
        res = libfirm.new_rd_Mux(self._debug,
            self.block._ir_block, irn_sel._ir_node, irn_false._ir_node, irn_true._ir_node)

        return Mux(res)

    def op_NoMem(self, ):
        """Placeholder node for cases where you don't need any memory input
    
        """
        res = libfirm.new_rd_NoMem(self._debug,
            self.graph._ir_graph)

        return NoMem(res)

    def op_Not(self, irn_op):
        """returns the bitwise complement of a value. Works for boolean values, too.
    
        @param irn_op op
        """
        res = libfirm.new_rd_Not(self._debug,
            self.block._ir_block, irn_op._ir_node)

        return Not(res)

    def op_Offset(self, mode, entity):
        """Symbolic constant that represents the offset of an entity in its owner type.
    
        @param mode mode of the operations result
        @param entity entity to operate on
        """
        res = libfirm.new_rd_Offset(self._debug,
            self.graph._ir_graph, mode, entity._ir_entity)

        return Offset(res)

    def op_Or(self, irn_left, irn_right):
        """returns the result of a bitwise or operation of its operands
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Or(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Or(res)

    def op_Phi(self, args, mode):
        """Choose a value based on control flow. A phi node has 1 input for each
	predecessor of its block. If a block is entered from its nth predecessor
	all phi nodes produce their nth input as result.
    
        @param arity size of additional inputs array
        @param in additional inputs
        @param mode mode of the operations result
        """
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Phi(self._debug,
            self.block._ir_block, len(args), arg_array, mode)

        return Phi(res)

    def op_Pin(self, irn_op):
        """Pin the value of the node node in the current block. No users of the Pin
	node can float above the Block of the Pin. The node cannot float behind
	this block. Often used to Pin the NoMem node.
    
        @param irn_op op
        """
        res = libfirm.new_rd_Pin(self._debug,
            self.block._ir_block, irn_op._ir_node)

        return Pin(res)

    def op_Proj(self, irn_pred, mode, num):
        """returns an entry of a tuple value
    
        @param irn_pred pred
        @param mode mode of the operations result
        @param num number of tuple component to be extracted
        """
        res = libfirm.new_rd_Proj(self._debug,
            irn_pred._ir_node, mode, num)

        return Proj(res)

    def op_Raise(self, irn_exo_ptr, irn_mem=None):
        """Raises an exception. Unconditional change of control flow. Writes an
	explicit Except variable to memory to pass it to the exception handler.
	Must be lowered to a Call to a runtime check function.
    
        @param irn_mem mem
        @param irn_exo_ptr exo_ptr
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.raise_(irn_exo_ptr)
        res = libfirm.new_rd_Raise(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_exo_ptr._ir_node)

        return Raise(res)

    def op_Return(self, args):
        """Returns from the current function. Takes memory and return values as
	operands.
    
        @param irn_mem mem
        @param arity size of additional inputs array
        @param in additional inputs
        """
        irn_mem = self.memory_policy.return_(args)
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Return(self._debug,
            self.block._ir_block, irn_mem._ir_node, len(args), arg_array)

        return Return(res)

    def op_Sel(self, irn_ptr, irn_index, type):
        """Computes the address of an array element from the array base pointer and
	an index.

	A Sel node must only produce a NULL pointer if the ptr input is NULL.
    
        @param irn_ptr ptr
        @param irn_index index
        @param type array type
        """
        res = libfirm.new_rd_Sel(self._debug,
            self.block._ir_block, irn_ptr._ir_node, irn_index._ir_node, type._ir_type)

        return Sel(res)

    def op_Shl(self, irn_left, irn_right):
        """Returns its first operands bits shifted left by the amount of the 2nd
	operand.
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Shl(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Shl(res)

    def op_Shr(self, irn_left, irn_right):
        """Returns its first operands bits shifted right by the amount of the 2nd
	operand. No special handling for the sign bit is performed (zero extension).
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Shr(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Shr(res)

    def op_Shrs(self, irn_left, irn_right):
        """Returns its first operands bits shifted right by the amount of the 2nd
	operand. The leftmost bit (usually the sign bit) stays the same
	(sign extension).
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Shrs(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Shrs(res)

    def op_Size(self, mode, type):
        """A symbolic constant that represents the size of a type
    
        @param mode mode of the operations result
        @param type type to operate on
        """
        res = libfirm.new_rd_Size(self._debug,
            self.graph._ir_graph, mode, type._ir_type)

        return Size(res)

    def op_Start(self, ):
        """The first node of a graph. Execution starts with this node.
    
        """
        res = libfirm.new_rd_Start(self._debug,
            self.graph._ir_graph)

        return Start(res)

    def op_Store(self, irn_ptr, irn_value, type, flags, irn_mem=None):
        """Stores a value into memory (heap or stack).
    
        @param irn_mem mem
        @param irn_ptr ptr
        @param irn_value value
        @param type The type of the object which is stored at ptr (need not match with value's type)
        @param flags specifies alignment, volatility and pin state
        """
        if irn_mem is None:
            irn_mem = self.memory_policy.store(irn_target)
        res = libfirm.new_rd_Store(self._debug,
            self.block._ir_block, irn_mem._ir_node, irn_ptr._ir_node, irn_value._ir_node, type._ir_type, flags)

        op = Store(res)
        self.memory_policy.post_store(op)
        return op

    def op_Sub(self, irn_left, irn_right):
        """returns the difference of its operands
    
        @param irn_left left
        @param irn_right right
        """
        res = libfirm.new_rd_Sub(self._debug,
            self.block._ir_block, irn_left._ir_node, irn_right._ir_node)

        return Sub(res)

    def op_Switch(self, irn_selector, n_outs, table):
        """Change control flow. The destination is choosen based on an integer input value which is looked up in a table.

	Backends can implement this efficiently using a jump table.
    
        @param irn_selector selector
        @param n_outs number of outputs (including pn_Switch_default)
        @param table table describing mapping from input values to Proj numbers
        """
        res = libfirm.new_rd_Switch(self._debug,
            self.block._ir_block, irn_selector._ir_node, n_outs, table)

        return Switch(res)

    def op_Sync(self, args):
        """The Sync operation unifies several partial memory blocks. These blocks
	have to be pairwise disjunct or the values in common locations have to
	be identical.  This operation allows to specify all operations that
	eventually need several partial memory blocks as input with a single
	entrance by unifying the memories with a preceding Sync operation.
    
        @param arity size of additional inputs array
        @param in additional inputs
        """
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Sync(self._debug,
            self.block._ir_block, len(args), arg_array)

        return Sync(res)

    def op_Tuple(self, args):
        """Builds a Tuple from single values.

	This is needed to implement optimizations that remove a node that produced
	a tuple.  The node can be replaced by the Tuple operation so that the
	following Proj nodes have not to be changed. (They are hard to find due to
	the implementation with pointers in only one direction.) The Tuple node is
	smaller than any other node, so that a node can be changed into a Tuple by
	just changing its opcode and giving it a new in array.
    
        @param arity size of additional inputs array
        @param in additional inputs
        """
        arg_array = ffi.new('ir_node *[]', [arg._ir_node for arg in args])
        res = libfirm.new_rd_Tuple(self._debug,
            self.block._ir_block, len(args), arg_array)

        return Tuple(res)

    def op_Unknown(self, mode):
        """Returns an unknown (at compile- and runtime) value. It is a valid
	optimization to replace an Unknown by any other constant value.

	Be careful when optimising Unknown values, you cannot simply replace
	Unknown+x or Unknown<x with a new Unknown node if there are multiple
	users of the original unknown node!
    
        @param mode mode of the operations result
        """
        res = libfirm.new_rd_Unknown(self._debug,
            self.graph._ir_graph, mode)

        return Unknown(res)

class _ASM_input(BaseSequence):
    def __len__(self):
        return libfirm.get_ASM_n_input_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_ASM_input(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_ASM_input_(
            self._ir_node, index, value)

class ASM(BaseNode):
    """executes assembler fragments of the target machine.

	The node contains a template for an assembler snippet. The compiler will
	replace occurences of %0 to %9 with input/output registers,
	%% with a single % char. Some backends allow additional specifiers (for
	example %w3, %l3, %h3 on x86 to get a 16bit, 8hit low, 8bit high part
	of a register).
	After the replacements the text is emitted into the final assembly.

	The clobber list contains names of registers which have an undefined value
	after the assembler instruction is executed; it may also contain 'memory'
	or 'cc' if global state/memory changes or the condition code registers
	(some backends implicitely set cc, memory clobbers on all ASM statements).

	Example (an i386 instruction)::

		ASM(text="btsl %1, %0",
			input_constraints = ["=m", "r"],
			clobbers = ["cc"])

	As there are no output, the %0 references the first input which is just an
	address which the asm operation writes to. %1 references to an input which
	is passed as a register. The condition code register has an unknown value
	after the instruction.

	(This format is inspired by the gcc extended asm syntax)
	
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_ASM())
    def getter(self):
        return libfirm.get_ASM_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_ASM_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    @property
    def input(self):
        return _ASM_input(self._ir_node)
    @property
    def input_constraints(self):
        # of type: ir_asm_constraint*
        return libfirm.get_ASM_input_constraints(self._ir_node)
    @property
    def output_constraints(self):
        # of type: ir_asm_constraint*
        return libfirm.get_ASM_output_constraints(self._ir_node)
    @property
    def clobbers(self):
        # of type: ident**
        return #(libfirm.get_ASM_clobbers(self._ir_node))
    @property
    def text(self):
        # of type: ident*
        return #(libfirm.get_ASM_text(self._ir_node))

class Add(Binop):
    """returns the sum of its operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Add())
    def getter(self):
        return libfirm.get_Add_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Add_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Add_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Add_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Address(EntConst):
    """Symbolic constant that represents the address of an entity (variable or method)
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Address())
    @property
    def entity(self):
        # of type: ir_entity*
        return wrap.entity(libfirm.get_Address_entity(self._ir_node))

class Align(TypeConst):
    """A symbolic constant that represents the alignment of a type
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Align())
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Align_type(self._ir_node))

class Alloc(BaseNode):
    """Allocates a block of memory on the stack.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Alloc())
    def getter(self):
        return libfirm.get_Alloc_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Alloc_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Alloc_size(self._ir_node)

    def setter(self, value):
        libfirm.get_Alloc_size(self._ir_node, value)

    size = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_res = 1

    def get_pn_res(self, mode):
        """pointer to newly allocated memory
        """
        return self.block.op_Proj(self, mode, 1)
    @property
    def alignment(self):
        # of type: unsigned
        return libfirm.get_Alloc_alignment(self._ir_node)

class Anchor(BaseNode):
    """Utility node used to "hold" nodes in a graph that might possibly not be
	reachable by other means or which should be reachable immediately without
	searching through the graph.
	Each firm-graph contains exactly one anchor node whose address is always
	known. All other well-known graph-nodes like Start, End, NoMem, ...
	are found by looking at the respective Anchor operand.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Anchor())
    def getter(self):
        return libfirm.get_Anchor_end_block(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_end_block(self._ir_node, value)

    end_block = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_start_block(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_start_block(self._ir_node, value)

    start_block = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_end(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_end(self._ir_node, value)

    end = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_start(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_start(self._ir_node, value)

    start = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_frame(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_frame(self._ir_node, value)

    frame = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_initial_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_initial_mem(self._ir_node, value)

    initial_mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_args(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_args(self._ir_node, value)

    args = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Anchor_no_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Anchor_no_mem(self._ir_node, value)

    no_mem = property(getter, setter)
    del getter, setter

class And(Binop):
    """returns the result of a bitwise and operation of its operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_And())
    def getter(self):
        return libfirm.get_And_left(self._ir_node)

    def setter(self, value):
        libfirm.get_And_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_And_right(self._ir_node)

    def setter(self, value):
        libfirm.get_And_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Bad(BaseNode):
    """Bad nodes indicate invalid input, which is values which should never be
	computed.

	The typical use case for the Bad node is removing unreachable code.
	Frontends should set the current_block to Bad when it is clear that
	following code must be unreachable (ie. after a goto or return statement).
	Optimizations also set block predecessors to Bad when it becomes clear,
	that a control flow edge can never be executed.

	The gigo optimizations ensures that nodes with Bad as their block, get
	replaced by Bad themselves. Nodes with at least 1 Bad input get exchanged
	with Bad too. Exception to this rule are Block, Phi, Tuple and End node;
	This is because removing inputs from a Block is hairy operation (requiring,
	Phis to be shortened too for example). So instead of removing block inputs
	they are set to Bad, and the actual removal is left to the control flow
	optimization phase. Block, Phi, Tuple with only Bad inputs however are
	replaced by Bad right away.

	In the future we may use the Bad node to model poison values that arise
	from undefined behaviour like reading uninitialized local variables in C.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Bad())

class Bitcast(BaseNode):
    """Converts a value between modes with different arithmetics but same
	number of bits by reinterpreting the bits in the new mode
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Bitcast())
    def getter(self):
        return libfirm.get_Bitcast_op(self._ir_node)

    def setter(self, value):
        libfirm.get_Bitcast_op(self._ir_node, value)

    op = property(getter, setter)
    del getter, setter

class _Block_cfgpred(BaseSequence):
    def __len__(self):
        return libfirm.get_Block_n_cfgpred_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Block_cfgpred(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Block_cfgpred_(
            self._ir_node, index, value)

class Block(BaseNode):
    """A basic block
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Block())
    @property
    def cfgpred(self):
        return _Block_cfgpred(self._ir_node)
    @property
    def entity(self):
        # of type: ir_entity*
        return wrap.entity(libfirm.get_Block_entity(self._ir_node))

class _Builtin_param(BaseSequence):
    def __len__(self):
        return libfirm.get_Builtin_n_param_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Builtin_param(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Builtin_param_(
            self._ir_node, index, value)

class Builtin(BaseNode):
    """performs a backend-specific builtin.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Builtin())
    def getter(self):
        return libfirm.get_Builtin_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Builtin_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    @property
    def param(self):
        return _Builtin_param(self._ir_node)

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)
    @property
    def kind(self):
        # of type: ir_builtin_kind
        return libfirm.get_Builtin_kind(self._ir_node)
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Builtin_type(self._ir_node))

class _Call_param(BaseSequence):
    def __len__(self):
        return libfirm.get_Call_n_param_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Call_param(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Call_param_(
            self._ir_node, index, value)

class Call(BaseNode):
    """Calls other code. Control flow is transfered to ptr, additional
	operands are passed to the called code. Called code usually performs a
	return operation. The operands of this return operation are the result
	of the Call node.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Call())
    def getter(self):
        return libfirm.get_Call_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Call_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Call_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Call_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter
    @property
    def param(self):
        return _Call_param(self._ir_node)

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_T_result = 1

    @property
    def pn_T_result(self):
        """tuple containing all results
        """
        return self.block.op_Proj(self, types.MODE_T, 1)

    PN_X_regular = 2

    @property
    def pn_X_regular(self):
        """control flow when no exception occurs
        """
        return self.block.op_Proj(self, types.MODE_X, 2)

    PN_X_except = 3

    @property
    def pn_X_except(self):
        """control flow when exception occured
        """
        return self.block.op_Proj(self, types.MODE_X, 3)
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Call_type(self._ir_node))

class Cmp(Binop):
    """Compares its two operands and checks whether a specified
	   relation (like less or equal) is fulfilled.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Cmp())
    def getter(self):
        return libfirm.get_Cmp_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Cmp_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Cmp_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Cmp_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter
    @property
    def relation(self):
        # of type: ir_relation
        return libfirm.get_Cmp_relation(self._ir_node)

class Cond(BaseNode):
    """Conditionally change control flow.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Cond())
    def getter(self):
        return libfirm.get_Cond_selector(self._ir_node)

    def setter(self, value):
        libfirm.get_Cond_selector(self._ir_node, value)

    selector = property(getter, setter)
    del getter, setter

    PN_false = 0

    @property
    def pn_false(self):
        """control flow if operand is "false"
        """
        return self.block.op_Proj(self, types.MODE_X, 0)

    PN_true = 1

    @property
    def pn_true(self):
        """control flow if operand is "true"
        """
        return self.block.op_Proj(self, types.MODE_X, 1)
    @property
    def jmp_pred(self):
        # of type: cond_jmp_predicate
        return libfirm.get_Cond_jmp_pred(self._ir_node)

class Confirm(BaseNode):
    """Specifies constraints for a value. This allows explicit representation
	of path-sensitive properties. (Example: This value is always >= 0 on 1
	if-branch then all users within that branch are rerouted to a confirm-node
	specifying this property).

	A constraint is specified for the relation between value and bound.
	value is always returned.
	Note that this node does NOT check or assert the constraint, it merely
	specifies it.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Confirm())
    def getter(self):
        return libfirm.get_Confirm_value(self._ir_node)

    def setter(self, value):
        libfirm.get_Confirm_value(self._ir_node, value)

    value = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Confirm_bound(self._ir_node)

    def setter(self, value):
        libfirm.get_Confirm_bound(self._ir_node, value)

    bound = property(getter, setter)
    del getter, setter
    @property
    def relation(self):
        # of type: ir_relation
        return libfirm.get_Confirm_relation(self._ir_node)

class Const(BaseNode):
    """Returns a constant value.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Const())
    @property
    def tarval(self):
        # of type: ir_tarval*
        return libfirm.get_Const_tarval(self._ir_node)

class Conv(BaseNode):
    """Converts values between modes
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Conv())
    def getter(self):
        return libfirm.get_Conv_op(self._ir_node)

    def setter(self, value):
        libfirm.get_Conv_op(self._ir_node, value)

    op = property(getter, setter)
    del getter, setter

class CopyB(BaseNode):
    """Copies a block of memory with statically known size/type.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_CopyB())
    def getter(self):
        return libfirm.get_CopyB_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_CopyB_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_CopyB_dst(self._ir_node)

    def setter(self, value):
        libfirm.get_CopyB_dst(self._ir_node, value)

    dst = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_CopyB_src(self._ir_node)

    def setter(self, value):
        libfirm.get_CopyB_src(self._ir_node, value)

    src = property(getter, setter)
    del getter, setter
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_CopyB_type(self._ir_node))
    @property
    def volatility(self):
        # of type: ir_volatility
        return libfirm.get_CopyB_volatility(self._ir_node)

class Deleted(BaseNode):
    """Internal node which is temporary set to nodes which are already removed
	from the graph.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Deleted())

class Div(BaseNode):
    """returns the quotient of its 2 operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Div())
    def getter(self):
        return libfirm.get_Div_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Div_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Div_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Div_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Div_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Div_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_res = 1

    @property
    def pn_res(self):
        """result of computation
        """
        return self.block.op_Proj(self, self.resmode, 1)

    PN_X_regular = 2

    @property
    def pn_X_regular(self):
        """control flow when no exception occurs
        """
        return self.block.op_Proj(self, types.MODE_X, 2)

    PN_X_except = 3

    @property
    def pn_X_except(self):
        """control flow when exception occured
        """
        return self.block.op_Proj(self, types.MODE_X, 3)
    @property
    def resmode(self):
        # of type: ir_mode*
        return libfirm.get_Div_resmode(self._ir_node)
    @property
    def no_remainder(self):
        # of type: int
        return libfirm.get_Div_no_remainder(self._ir_node)

class Dummy(BaseNode):
    """A placeholder value. This is used when constructing cyclic graphs where
	you have cases where not all predecessors of a phi-node are known. Dummy
	nodes are used for the unknown predecessors and replaced later.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Dummy())

class _End_keepalive(BaseSequence):
    def __len__(self):
        return libfirm.get_End_n_keepalive_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_End_keepalive(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_End_keepalive_(
            self._ir_node, index, value)

class End(BaseNode):
    """Last node of a graph. It references nodes in endless loops (so called
	keepalive edges)
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_End())
    @property
    def keepalive(self):
        return _End_keepalive(self._ir_node)

class Eor(Binop):
    """returns the result of a bitwise exclusive or operation of its operands.

	This is also known as the Xor operation.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Eor())
    def getter(self):
        return libfirm.get_Eor_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Eor_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Eor_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Eor_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Free(BaseNode):
    """Frees a block of memory previously allocated by an Alloc node
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Free())
    def getter(self):
        return libfirm.get_Free_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Free_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Free_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Free_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter

class IJmp(BaseNode):
    """Jumps to the code in its argument. The code has to be in the same
	function and the destination must be one of the blocks reachable
	by the tuple results
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_IJmp())
    def getter(self):
        return libfirm.get_IJmp_target(self._ir_node)

    def setter(self, value):
        libfirm.get_IJmp_target(self._ir_node, value)

    target = property(getter, setter)
    del getter, setter

class Id(BaseNode):
    """Returns its operand unchanged.

	This is mainly used when exchanging nodes. Usually you shouldn't see Id
	nodes since the getters/setters for node inputs skip them automatically.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Id())
    def getter(self):
        return libfirm.get_Id_pred(self._ir_node)

    def setter(self, value):
        libfirm.get_Id_pred(self._ir_node, value)

    pred = property(getter, setter)
    del getter, setter

class Jmp(BaseNode):
    """Jumps to the block connected through the out-value
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Jmp())

class Load(BaseNode):
    """Loads a value from memory (heap or stack).
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Load())
    def getter(self):
        return libfirm.get_Load_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Load_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Load_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Load_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_res = 1

    @property
    def pn_res(self):
        """result of load operation
        """
        return self.block.op_Proj(self, self.mode, 1)

    PN_X_regular = 2

    @property
    def pn_X_regular(self):
        """control flow when no exception occurs
        """
        return self.block.op_Proj(self, types.MODE_X, 2)

    PN_X_except = 3

    @property
    def pn_X_except(self):
        """control flow when exception occurred
        """
        return self.block.op_Proj(self, types.MODE_X, 3)
    @property
    def mode(self):
        # of type: ir_mode*
        return libfirm.get_Load_mode(self._ir_node)
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Load_type(self._ir_node))
    @property
    def volatility(self):
        # of type: ir_volatility
        return libfirm.get_Load_volatility(self._ir_node)
    @property
    def unaligned(self):
        # of type: ir_align
        return libfirm.get_Load_unaligned(self._ir_node)

class Member(BaseNode):
    """Computes the address of a compound type member given the base address
	of an instance of the compound type.

	A Member node must only produce a NULL pointer if the ptr input is NULL.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Member())
    def getter(self):
        return libfirm.get_Member_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Member_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter
    @property
    def entity(self):
        # of type: ir_entity*
        return wrap.entity(libfirm.get_Member_entity(self._ir_node))

class Minus(BaseNode):
    """returns the additive inverse of its operand
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Minus())
    def getter(self):
        return libfirm.get_Minus_op(self._ir_node)

    def setter(self, value):
        libfirm.get_Minus_op(self._ir_node, value)

    op = property(getter, setter)
    del getter, setter

class Mod(BaseNode):
    """returns the remainder of its operands from an implied division.

	Examples:

	* mod(5,3)   produces 2
	* mod(5,-3)  produces 2
	* mod(-5,3)  produces -2
	* mod(-5,-3) produces -2
	
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Mod())
    def getter(self):
        return libfirm.get_Mod_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Mod_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mod_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Mod_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mod_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Mod_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_res = 1

    @property
    def pn_res(self):
        """result of computation
        """
        return self.block.op_Proj(self, self.resmode, 1)

    PN_X_regular = 2

    @property
    def pn_X_regular(self):
        """control flow when no exception occurs
        """
        return self.block.op_Proj(self, types.MODE_X, 2)

    PN_X_except = 3

    @property
    def pn_X_except(self):
        """control flow when exception occured
        """
        return self.block.op_Proj(self, types.MODE_X, 3)
    @property
    def resmode(self):
        # of type: ir_mode*
        return libfirm.get_Mod_resmode(self._ir_node)

class Mul(Binop):
    """returns the product of its operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Mul())
    def getter(self):
        return libfirm.get_Mul_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Mul_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mul_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Mul_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Mulh(Binop):
    """returns the upper word of the product of its operands (the part which
	would not fit into the result mode of a normal Mul anymore)
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Mulh())
    def getter(self):
        return libfirm.get_Mulh_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Mulh_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mulh_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Mulh_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Mux(BaseNode):
    """returns the false or true operand depending on the value of the sel
	operand
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Mux())
    def getter(self):
        return libfirm.get_Mux_sel(self._ir_node)

    def setter(self, value):
        libfirm.get_Mux_sel(self._ir_node, value)

    sel = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mux_false(self._ir_node)

    def setter(self, value):
        libfirm.get_Mux_false(self._ir_node, value)

    false = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Mux_true(self._ir_node)

    def setter(self, value):
        libfirm.get_Mux_true(self._ir_node, value)

    true = property(getter, setter)
    del getter, setter

class NoMem(BaseNode):
    """Placeholder node for cases where you don't need any memory input
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_NoMem())

class Not(BaseNode):
    """returns the bitwise complement of a value. Works for boolean values, too.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Not())
    def getter(self):
        return libfirm.get_Not_op(self._ir_node)

    def setter(self, value):
        libfirm.get_Not_op(self._ir_node, value)

    op = property(getter, setter)
    del getter, setter

class Offset(EntConst):
    """Symbolic constant that represents the offset of an entity in its owner type.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Offset())
    @property
    def entity(self):
        # of type: ir_entity*
        return wrap.entity(libfirm.get_Offset_entity(self._ir_node))

class Or(Binop):
    """returns the result of a bitwise or operation of its operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Or())
    def getter(self):
        return libfirm.get_Or_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Or_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Or_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Or_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class _Phi_pred(BaseSequence):
    def __len__(self):
        return libfirm.get_Phi_n_pred_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Phi_pred(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Phi_pred_(
            self._ir_node, index, value)

class Phi(BaseNode):
    """Choose a value based on control flow. A phi node has 1 input for each
	predecessor of its block. If a block is entered from its nth predecessor
	all phi nodes produce their nth input as result.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Phi())
    @property
    def pred(self):
        return _Phi_pred(self._ir_node)
    @property
    def loop(self):
        # of type: int
        return libfirm.get_Phi_loop(self._ir_node)

class Pin(BaseNode):
    """Pin the value of the node node in the current block. No users of the Pin
	node can float above the Block of the Pin. The node cannot float behind
	this block. Often used to Pin the NoMem node.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Pin())
    def getter(self):
        return libfirm.get_Pin_op(self._ir_node)

    def setter(self, value):
        libfirm.get_Pin_op(self._ir_node, value)

    op = property(getter, setter)
    del getter, setter

class Proj(BaseNode):
    """returns an entry of a tuple value
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Proj())
    def getter(self):
        return libfirm.get_Proj_pred(self._ir_node)

    def setter(self, value):
        libfirm.get_Proj_pred(self._ir_node, value)

    pred = property(getter, setter)
    del getter, setter
    @property
    def num(self):
        # of type: unsigned
        return libfirm.get_Proj_num(self._ir_node)

class Raise(BaseNode):
    """Raises an exception. Unconditional change of control flow. Writes an
	explicit Except variable to memory to pass it to the exception handler.
	Must be lowered to a Call to a runtime check function.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Raise())
    def getter(self):
        return libfirm.get_Raise_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Raise_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Raise_exo_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Raise_exo_ptr(self._ir_node, value)

    exo_ptr = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_X = 1

    @property
    def pn_X(self):
        """control flow to exception handler
        """
        return self.block.op_Proj(self, types.MODE_X, 1)

class _Return_res(BaseSequence):
    def __len__(self):
        return libfirm.get_Return_n_res_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Return_res(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Return_res_(
            self._ir_node, index, value)

class Return(BaseNode):
    """Returns from the current function. Takes memory and return values as
	operands.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Return())
    def getter(self):
        return libfirm.get_Return_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Return_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    @property
    def res(self):
        return _Return_res(self._ir_node)

class Sel(BaseNode):
    """Computes the address of an array element from the array base pointer and
	an index.

	A Sel node must only produce a NULL pointer if the ptr input is NULL.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Sel())
    def getter(self):
        return libfirm.get_Sel_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Sel_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Sel_index(self._ir_node)

    def setter(self, value):
        libfirm.get_Sel_index(self._ir_node, value)

    index = property(getter, setter)
    del getter, setter
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Sel_type(self._ir_node))

class Shl(Binop):
    """Returns its first operands bits shifted left by the amount of the 2nd
	operand.
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Shl())
    def getter(self):
        return libfirm.get_Shl_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Shl_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Shl_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Shl_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Shr(Binop):
    """Returns its first operands bits shifted right by the amount of the 2nd
	operand. No special handling for the sign bit is performed (zero extension).
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Shr())
    def getter(self):
        return libfirm.get_Shr_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Shr_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Shr_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Shr_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Shrs(Binop):
    """Returns its first operands bits shifted right by the amount of the 2nd
	operand. The leftmost bit (usually the sign bit) stays the same
	(sign extension).
	The right input (shift amount) must be an unsigned integer value.
	If the result mode has modulo_shift!=0, then the effective shift amount is
	the right input modulo this modulo_shift amount.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Shrs())
    def getter(self):
        return libfirm.get_Shrs_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Shrs_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Shrs_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Shrs_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Size(TypeConst):
    """A symbolic constant that represents the size of a type
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Size())
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Size_type(self._ir_node))

class Start(BaseNode):
    """The first node of a graph. Execution starts with this node.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Start())

    PN_M = 0

    @property
    def pn_M(self):
        """initial memory
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_P_frame_base = 1

    @property
    def pn_P_frame_base(self):
        """frame base pointer
        """
        return self.block.op_Proj(self, types.MODE_P, 1)

    PN_T_args = 2

    @property
    def pn_T_args(self):
        """function arguments
        """
        return self.block.op_Proj(self, types.MODE_T, 2)

class Store(BaseNode):
    """Stores a value into memory (heap or stack).
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Store())
    def getter(self):
        return libfirm.get_Store_mem(self._ir_node)

    def setter(self, value):
        libfirm.get_Store_mem(self._ir_node, value)

    mem = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Store_ptr(self._ir_node)

    def setter(self, value):
        libfirm.get_Store_ptr(self._ir_node, value)

    ptr = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Store_value(self._ir_node)

    def setter(self, value):
        libfirm.get_Store_value(self._ir_node, value)

    value = property(getter, setter)
    del getter, setter

    PN_M = 0

    @property
    def pn_M(self):
        """memory result
        """
        return self.block.op_Proj(self, types.MODE_M, 0)

    PN_X_regular = 1

    @property
    def pn_X_regular(self):
        """control flow when no exception occurs
        """
        return self.block.op_Proj(self, types.MODE_X, 1)

    PN_X_except = 2

    @property
    def pn_X_except(self):
        """control flow when exception occured
        """
        return self.block.op_Proj(self, types.MODE_X, 2)
    @property
    def type(self):
        # of type: ir_type*
        return wrap.type(libfirm.get_Store_type(self._ir_node))
    @property
    def volatility(self):
        # of type: ir_volatility
        return libfirm.get_Store_volatility(self._ir_node)
    @property
    def unaligned(self):
        # of type: ir_align
        return libfirm.get_Store_unaligned(self._ir_node)

class Sub(Binop):
    """returns the difference of its operands
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Sub())
    def getter(self):
        return libfirm.get_Sub_left(self._ir_node)

    def setter(self, value):
        libfirm.get_Sub_left(self._ir_node, value)

    left = property(getter, setter)
    del getter, setter
    def getter(self):
        return libfirm.get_Sub_right(self._ir_node)

    def setter(self, value):
        libfirm.get_Sub_right(self._ir_node, value)

    right = property(getter, setter)
    del getter, setter

class Switch(BaseNode):
    """Change control flow. The destination is choosen based on an integer input value which is looked up in a table.

	Backends can implement this efficiently using a jump table.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Switch())
    def getter(self):
        return libfirm.get_Switch_selector(self._ir_node)

    def setter(self, value):
        libfirm.get_Switch_selector(self._ir_node, value)

    selector = property(getter, setter)
    del getter, setter

    PN_default = 0

    @property
    def pn_default(self):
        """control flow if no other case matches
        """
        return self.block.op_Proj(self, types.MODE_X, 0)
    @property
    def n_outs(self):
        # of type: unsigned
        return libfirm.get_Switch_n_outs(self._ir_node)
    @property
    def table(self):
        # of type: ir_switch_table*
        return libfirm.get_Switch_table(self._ir_node)

class _Sync_pred(BaseSequence):
    def __len__(self):
        return libfirm.get_Sync_n_pred_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Sync_pred(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Sync_pred_(
            self._ir_node, index, value)

class Sync(BaseNode):
    """The Sync operation unifies several partial memory blocks. These blocks
	have to be pairwise disjunct or the values in common locations have to
	be identical.  This operation allows to specify all operations that
	eventually need several partial memory blocks as input with a single
	entrance by unifying the memories with a preceding Sync operation.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Sync())
    @property
    def pred(self):
        return _Sync_pred(self._ir_node)

class _Tuple_pred(BaseSequence):
    def __len__(self):
        return libfirm.get_Tuple_n_pred_(self._ir_node)

    def getitem(self, index):
        return libfirm.get_Tuple_pred(
            self._ir_node, index)

    def setitem(self, index, value):
        libfirm.set_Tuple_pred_(
            self._ir_node, index, value)

class Tuple(BaseNode):
    """Builds a Tuple from single values.

	This is needed to implement optimizations that remove a node that produced
	a tuple.  The node can be replaced by the Tuple operation so that the
	following Proj nodes have not to be changed. (They are hard to find due to
	the implementation with pointers in only one direction.) The Tuple node is
	smaller than any other node, so that a node can be changed into a Tuple by
	just changing its opcode and giving it a new in array.
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Tuple())
    @property
    def pred(self):
        return _Tuple_pred(self._ir_node)

class Unknown(BaseNode):
    """Returns an unknown (at compile- and runtime) value. It is a valid
	optimization to replace an Unknown by any other constant value.

	Be careful when optimising Unknown values, you cannot simply replace
	Unknown+x or Unknown<x with a new Unknown node if there are multiple
	users of the original unknown node!
    """
    OPCODE = libfirm.get_op_code(libfirm.get_op_Unknown())

by_opcode = {
    ASM.OPCODE : ASM,
    Add.OPCODE : Add,
    Address.OPCODE : Address,
    Align.OPCODE : Align,
    Alloc.OPCODE : Alloc,
    Anchor.OPCODE : Anchor,
    And.OPCODE : And,
    Bad.OPCODE : Bad,
    Bitcast.OPCODE : Bitcast,
    Block.OPCODE : Block,
    Builtin.OPCODE : Builtin,
    Call.OPCODE : Call,
    Cmp.OPCODE : Cmp,
    Cond.OPCODE : Cond,
    Confirm.OPCODE : Confirm,
    Const.OPCODE : Const,
    Conv.OPCODE : Conv,
    CopyB.OPCODE : CopyB,
    Deleted.OPCODE : Deleted,
    Div.OPCODE : Div,
    Dummy.OPCODE : Dummy,
    End.OPCODE : End,
    Eor.OPCODE : Eor,
    Free.OPCODE : Free,
    IJmp.OPCODE : IJmp,
    Id.OPCODE : Id,
    Jmp.OPCODE : Jmp,
    Load.OPCODE : Load,
    Member.OPCODE : Member,
    Minus.OPCODE : Minus,
    Mod.OPCODE : Mod,
    Mul.OPCODE : Mul,
    Mulh.OPCODE : Mulh,
    Mux.OPCODE : Mux,
    NoMem.OPCODE : NoMem,
    Not.OPCODE : Not,
    Offset.OPCODE : Offset,
    Or.OPCODE : Or,
    Phi.OPCODE : Phi,
    Pin.OPCODE : Pin,
    Proj.OPCODE : Proj,
    Raise.OPCODE : Raise,
    Return.OPCODE : Return,
    Sel.OPCODE : Sel,
    Shl.OPCODE : Shl,
    Shr.OPCODE : Shr,
    Shrs.OPCODE : Shrs,
    Size.OPCODE : Size,
    Start.OPCODE : Start,
    Store.OPCODE : Store,
    Sub.OPCODE : Sub,
    Switch.OPCODE : Switch,
    Sync.OPCODE : Sync,
    Tuple.OPCODE : Tuple,
    Unknown.OPCODE : Unknown,
}

import firm.extras # some custom field overrides
