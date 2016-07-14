###############################################################################
#
#   Copyright: (c) 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from .graph import DependencyGraph, GraphError, PropertyNode, SettableNode
from .graph import create_node
from .graph_api import GetNode

from .. import depgraph as onyx_dg

import collections

__all__ = ["EvalBlock", "GraphScope"]


###############################################################################
class EvalBlock(object):
    """
    Description:
        Context manager used to manage lifetime of one or more one-off changes.
    Usage:
        Typical use is as follows:

        with EvalBlock() as eb:
            ...
            eb.change_value("abc", "xyz", 123)
            ...
    """
    # -------------------------------------------------------------------------
    def __init__(self):
        self.__changes = []
        self.__changed_nodes = {}

    # -------------------------------------------------------------------------
    def __enter__(self):
        # --- return a reference to itself (to be used by change_value)
        return self

    # -------------------------------------------------------------------------
    def __exit__(self, *args, **kwds):
        for node_id in reversed(self.__changes):
            old_node = self.__changed_nodes[node_id]

            # --- invalidate all parents, but not the node itself
            for parent in onyx_dg.graph[node_id].parents | old_node.parents:
                onyx_dg.graph[parent].invalidate()

            # --- reconstruct connection with children
            for child in old_node.children:
                onyx_dg.graph[child].parents.add(node_id)

            # --- store pre-change node into the graph
            onyx_dg.graph[node_id] = old_node

        self.__changes = []
        self.__changed_nodes = {}

        # --- returns False so that all execptions raised will be propagated
        return False

    # -------------------------------------------------------------------------
    def change_value(self, obj, VT, value):
        """
        Description:
            Change the in-memory value of a ValueType within an EvalBlock.
        Inputs:
            obj   - instance (or name) of an object derived from UfoBase
            VT    - name of the target ValueType
            value - the new value for the VT
        Returns:
            None.
        """
        name = obj if isinstance(obj, str) else obj.Name
        node_id = (name, VT, ())

        try:
            node = onyx_dg.graph[node_id]
        except KeyError:
            onyx_dg.graph[node_id] = node = create_node(node_id)

        if not isinstance(node, (PropertyNode, SettableNode)):
            raise GraphError("Unsupported node type: "
                             "{0:s}".format(node.__class__.__name__))

        # --- copy pre-change node and store it in __changed_nodes. This is
        #     only required the first time a VT is changed.
        if node_id not in self.__changed_nodes:
            self.__changes.append(node_id)
            self.__changed_nodes[node_id] = node.clone()

        # --- remove this node from the set of parents of all its children
        for child in node.children:
            onyx_dg.graph[child].parents.remove(node_id)

        # --- remove all its children
        node.children.clear()

        # --- invalidate all its parents
        for parent in node.parents:
            onyx_dg.graph[parent].invalidate()

        # --- set the node value and set its state to valid
        node.value = value
        node.valid = True


###############################################################################
class dict_with_fallback(collections.UserDict):
    # -------------------------------------------------------------------------
    def __init__(self, fallback, *args, **kwds):
        super().__init__(*args, **kwds)
        self.fallback = fallback

    # -------------------------------------------------------------------------
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            return self.fallback[item]


###############################################################################
class GraphScope(DependencyGraph):
    """
    Description:
        Context manager used to manage the lifetime of in-memory changes to
        ValueTypes. GraphScope can be used to create persistent scenarions that
        are then re-used multiple times.
    Usage:
        Typical use is as follows:

        scope = GraphScope()
        scope.change_value("abc", xyz", 123)
        with scope:
            ...
            scope.change_value("abc", "xxx", 666)
            ...

        with scope:
            ...
            ...
    """
    # -------------------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.active = False
        self.curr_graph = None
        self.vts_by_obj = dict_with_fallback({})

    # -------------------------------------------------------------------------
    def __enter__(self):
        self.active = True
        self.curr_graph = onyx_dg.graph
        self.vts_by_obj.fallback = onyx_dg.graph.vts_by_obj
        onyx_dg.graph = self

        # --- return a reference to itself (to be used for disposable scopes)
        return self

    # -------------------------------------------------------------------------
    def __exit__(self, *args, **kwds):
        self.active = False
        onyx_dg.graph = self.curr_graph
        # --- returns False so that all execptions raised will be propagated
        return False

    # -------------------------------------------------------------------------
    def __getitem__(self, item):
        if self.curr_graph is None:
            raise RuntimeError("GraphScope can "
                               "only be used as a context manager")

        try:
            return super().__getitem__(item)
        except KeyError:
            # --- always make a copy of every node that is requested within
            #     the graph scope so as to keep the outside graph unchanged
            self[item] = node = self.curr_graph[item].clone()
            return node

    # -------------------------------------------------------------------------
    def __deepcopy__(self, memo):
        clone = self.__new__(self.__class__)
        clone.data = self.data.copy()
        clone.active = self.active
        clone.vts_by_obj = self.vts_by_obj.copy()
        memo[id(self)] = clone
        return clone

    # -------------------------------------------------------------------------
    def copy_graph(self, node_id):
        """
        Recursively make a copy (if needed) of the portion of graph that
        depends on the current node. Each node is invalidated.
        """
        try:
            node = super().__getitem__(node_id)
            node.valid = False
        except KeyError:
            try:
                node = self.curr_graph[node_id].clone()
                node.valid = False
            except KeyError:
                node = create_node(node_id)

            self[node_id] = node

        for parent in node.parents:
            self.copy_graph(parent)

        return node

    # -------------------------------------------------------------------------
    def change_value(self, obj, VT, value):
        """
        Description:
            Change the value of a ValueType within a GraphScope.
            NB: only StoredAttrs and VTs defined as Property can be changed.
        Inputs:
            obj   - instance (or name) of an object derived from UfoBase
            VT    - name of the target ValueType
            value - the new value for the VT
        Returns:
            None.
        """
        if not self.active:
            # --- switch graph to graph scope
            self.curr_graph = onyx_dg.graph
            self.vts_by_obj.fallback = onyx_dg.graph.vts_by_obj
            onyx_dg.graph = self

        name = obj if isinstance(obj, str) else obj.Name
        node_id = (name, VT, ())

        # --- make a copy of the sub-graph that depends on the changed node and
        #     return a reference to the node itself (invalidation of parents
        #     takes place here too)
        node = self.copy_graph(node_id)

        if not isinstance(node, (PropertyNode, SettableNode)):
            raise GraphError("Unsupported node type: "
                             "{0:s}".format(node.__class__.__name__))

        # --- remove this node from the set of parents of all its children
        for child in node.children:
            self[child].parents.discard(node_id)

        # --- remove all its children
        node.children = set()

        # --- set the node value and set its state to valid
        node.value = value
        node.valid = True

        if not self.active:
            # --- switch graph back to the fallback
            onyx_dg.graph = self.curr_graph
            self.curr_graph = None
