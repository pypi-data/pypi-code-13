import firm.types
import contextlib
import firm.operations
from firm.base import libfirm, ffi, FirmException
from firm.operations import NodeBuilder
from firm.entity import MethodEntity
from firm import bitfields, wrap
from firm.types import ident
from firm.memorypolicy import CarefulPolicyFactory


class Block(NodeBuilder, firm.operations.Block):
    @property
    def _ir_val(self):
        return self._ir_block

    def new(cls, ir_block, graph):
        self = cls(ir_block)
        self._ir_graph = self._graph = graph

    def __init__(self, ir_block, graph=None):
        super(Block, self).__init__(ir_block)
        self._ir_block = ir_block
        if graph is None:
            graph = self.graph
        self._ir_graph = graph._ir_graph
        self._debug = ffi.NULL
        self.memory_policy = graph.memory_policy.policy_for(self)

    @property
    def block(self):
        return self

    def op_Block(self, *args):
        block = super(Block, self).op_Block(*args)
        return self.graph.block_factory(block._ir_node, self.graph)

    def get_entity(self):
        return wrap.entity(libfirm.create_Block_entity(self._ir_block))

    def add_predecessor(self, jmp):
        libfirm.add_immBlock_pred(self._ir_block, jmp._ir_node)

    def mature(self):
        libfirm.mature_immBlock(self._ir_block)

    def get_store(self):
        return wrap.node(libfirm.get_r_store(self._ir_graph))

    def set_store(self, value):
        libfirm.set_r_store(self._ir_graph, value._ir_node)

    store = property(get_store, set_store)

    @contextlib.contextmanager
    def debug_info(self, info):
        """A context manager for setting debug info, usually line-by-line.

        For example, for an + operation on line 12, column 6:

        with block.debug(SrcLoc(6, 'file.q', 12)):
            block.op_Add(x, y, mode_Is)
        """
        old = self._debug
        self._debug = info._get_ffi_handle()
        yield self
        self._debug = old

    def op_return(self, *values):
        result = self.op_Return(values)
        self.graph.end_block.add_predecessor(result)
        self.mature()


class SSIBlock(Block):
    """Class for constructing blocks from code already in SSI form.
    """
    def __init__(self, ir_block, graph, modes=()):
        super(SSABlock, self).__init__(ir_block, graph)
        self.prepare_args(modes)
        self.entries = []

    def exit_if(self, condition, target, args):
        cond = self.op_Cond(condition)
        target.enter([cond.pn_True, self.store] + args)

    def enter(self, args):
        self.entries.append((source, args))

    def prepare_args(self, modes):
        self.blockargs = []
        for mode in modes:
            phi = self.op_Phi([], mode)
            self.blockargs.append(phi)
            libfirm.add_Block_phi(self._ir_block, phi._ir_node)

    def bind_args(self):
        for argno, phi in enumerate(self.blockargs):
            phi.predecessors[:] = [ex[argno] for ex in self.entries]


class ImperitiveBlock(Block):
    """Block builder for code in imperitive form.

    Uses libfirm's fast + efficient SSA algorithm.
    """
    def get(self, index, mode=None):
        if mode is None:
            mode = types.mode_X
        return wrap.node(libfirm.get_r_value(self._ir_graph, index, mode))

    def set(self, index, value):
        libfirm.set_r_value(self._ir_graph, index, value._ir_node)


class Function(MethodEntity):
    # def __init__(self, name, prototype):
    #     self.prototype = prototype
    #     self._entity = prototype.new_entity(name)
    #     self._ir_graph = libfirm.new_ir_graph(proto, len(args))
    #     self.graph = IRGraph(self._ir_graph)
    #     self.args_node = libfirm.get_irg_args(self._ir_graph)

    block_factory = ImperitiveBlock
    graph_factory = lambda fun: IRGraph(fun, block_factory=fun.block_factory)

    @classmethod
    def new(cls, signature, name):
        self = cls(libfirm.new_entity(libfirm.get_glob_type(),
                                      ident(name),
                                      signature._ir_type))
        return self

    def build_graph(self, **graph_args):
        self.graph_factory(self, **graph_args)



get_total_visited = libfirm.get_max_irg_visited
set_total_visited = libfirm.set_max_irg_visited
inc_total_visited = libfirm.inc_max_irg_visited


def _irg_property(name, immutable=False, ctor=None):
    underlying_get = getattr(libfirm, 'get_irg_' + name)
    if ctor is None:
        def getter(self):
            return underlying_get(self._graph)
    elif isinstance(ctor, str):
        def getter(self):
            return self.construct(underlying_get(self._graph), ctor)
    else:
        def getter(self):
            return ctor(underlying_get(self._graph))
    if immutable:
        return property(getter)

    underlying_set = getattr(libfirm, 'set_irg_' + name)
    if ctor is None:
        def setter(self, value):
            underlying_set(self._graph, value)
    else:
        def setter(self, value):
            underlying_set(self._graph, value._ir_val)
    return property(getter, setter, doc=name)


class Nodes(object):
    def __init__(self, graph):
        self._graph = graph

    def __getitem__(self, index):
        assert isinstance(index, int)
        return self._graph.construct(libfirm.get_idx_irn(self._graph), 'node')

    def __len__(self):
        return libfirm.get_irg_last_idx(self._graph) + 1


NOGRAPH = object()

class IRGraph(NodeBuilder):
    @classmethod
    def const_graph(cls):
        return cls(libfirm.get_const_code_irg())

    @property
    def _ir_val(self):
        return self._graph

    @property
    def graph(self):
        return self

    @classmethod
    def new(cls, entity, n_locals=0, block_factory=None):
        """Create an IR Graph.

        @param entity An IR entity of type method
        @param n_locals the number of local variables of the graph,
               including arguments
        """
        return cls(libfirm.new_ir_graph(entity._ir_entity, n_locals),
                   block_factory)

    def __init__(self, ir_graph, block_factory=None, memory_policy=None):
        self._graph = self._ir_graph = ir_graph
        self.nodes = Nodes(ir_graph)
        if block_factory is None:
            block_factory = ImperitiveBlock
        self.block_factory = block_factory
        if memory_policy is None:
            memory_policy = CarefulPolicyFactory()
        self.memory_policy = memory_policy
        self._debug = ffi.NULL

    @property
    def args_node(self):
        return wrap.node(libfirm.get_irg_args(self._ir_graph))

    def arg(self, name, mode):
        if isinstance(name, int):
            index = name
        else:
            index = self.prototype.argnames.index(name)
        return self.start_block.op_Proj(self.args_node, mode, index)

    def get_current_block(self):
        return self.block_factory(libfirm.get_r_cur_block(self._graph), self)

    def set_current_block(self, value):
        libfirm.set_r_cur_block(self._graph, value._ir_block)

    current_block = property(get_current_block, set_current_block)

    def finalise(self):
        libfirm.irg_finalize_cons(self._ir_graph)

    def free(self, *discard):
        if self._graph is not NOGRAPH:
            libfirm.free_ir_graph(self._graph)
            self._graph = NOGRAPH

    entity = _irg_property('entity', ctor=Function)
    frame_type = _irg_property('frame_type', ctor=wrap.type)
    frame = _irg_property('frame')

    start = _irg_property('start', ctor='node')
    end = _irg_property('end', ctor='node')

    start_block = _irg_property('start_block', ctor='node')
    end_block = _irg_property('end_block', ctor='node')

    initial_mem = _irg_property('initial_mem', ctor='node')
    args = _irg_property('args', ctor='node')
    no_mem = _irg_property('no_mem', ctor='node')
    
    value_number_max = _irg_property('n_locs', immutable=True)
    graph_number = _irg_property('graph_nr', immutable=True)
    pinned = _irg_property('pinned', immutable=True, ctor=bitfields.PinState)
    #callee_info_state = _irg_property('callee_info_state')
    
    link = _irg_property('link') # XXX: box/unbox?
    def get_link(self):
        link = libfirm.get_irg_link(self._ir_graph)
        if link != ffi.NULL:
            return ffi.from_handle(link)

    def set_link(self, value):
        libfirm.set_irg_link(self._ir_graph, value._get_ffi_handle())

    link = property(get_link, set_link)
    visited = _irg_property('visited')

    def inc_visited(self):
        libfirm.inc_irg_visited(self._graph)

    block_visited = _irg_property('block_visited')

    def reserve_resources(self, resources):
        libfirm.ir_reserve_resources(self._graph, int(resources))

    def free_resources(self, resources):
        libfirm.ir_free_resources(self._graph, int(resources))

    @property
    def resources(self):
        return bitfields.Resources(libfirm.ir_resources_reserved(self._graph))

    def add_constraints(self, constraints):
        libfirm.add_irg_constraints(self._graph, int(constraints))

    def clear_constraints(self, constraints):
        libfirm.clear_irg_constraints(self._graph, int(constraints))

    def is_constrained(self, constraints):
        return libfirm.irg_is_constrained(self._graph, int(constraints))

    def add_properties(self, properties):
        libfirm.add_irg_properties(self._graph, int(properties))

    def clear_properties(self, properties):
        libfirm.clear_irg_properties(self._graph, int(properties))

    def has_propreties(self, properties):
        return libfirm.has_irg_properties(int(properties))

    def set_loc_description(self, n, description):
        libfirm.set_irg_loc_description(self._graph, n,
                                        description._get_ffi_handle())

    def get_loc_description(self, n):
        description = libfirm.get_irg_loc_description(self._graph, n)
        if description != ffi.NULL:
            return ffi.from_handle(description)

    def assure(self, properties):
        libfirm.assure_irg_properties(self._graph, int(properties))

    def confirm(self, properties):
        libfirm.confirm_irg_properties(self._graph, int(properties))

    def construct(self, ir_node, name):
        if name == 'node':
            node = wrap.node(ir_node)
            if isinstance(node, firm.operations.Block):
                return self.block_factory(ir_node, self)
            return node

    def op_Block(self, *args):
        block = super(IRGraph, self).op_Block(*args)
        return self.block_factory(block._ir_node, self)

    def verify(self):
        if not libfirm.irg_verify(self._graph):
            raise FirmException('Graph failed to verify')
