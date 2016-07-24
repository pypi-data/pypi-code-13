"""
Utils to store category ancestors graph in a flattened representation
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import defaultdict, deque

from .ordered_set import OrderedSet


NO_SUCH_VERTEX_EXC_FMT = 'Graph contains no vertex with key "{}"'
NO_SUCH_EDGE_EXC_FMT = 'Graph contains no edge from key "{}" to "{}"'

DUPLICATE_VERTEX_EXC_FMT = 'Graph already contains vertex with key "{}"'
DUPLICATE_EDGE_EXC_FMT = 'Graph already contains edge from key "{}" to "{}"'


class NoSuchVertexException(Exception):
    """
    Raised when `DiGraph` attempts to access a nonexistant vertex
    """
    pass


class DuplicateVertexException(Exception):
    """
    Raised when `DiGraph` attempts to add a duplicate vertex key
    """
    pass


class VertexHasEdgesException(Exception):
    """
    Raised when deleting a vertex with non-zero number of edges
    """
    pass


class NoSuchEdgeException(Exception):
    """
    Raised when `DiGraph` attempts to access a nonexistant edge
    """
    pass


class DuplicateEdgeException(Exception):
    """
    Raised when `DiGraph` attempts to add a duplicate edge
    """
    pass


class DiGraph(object):
    """
    Directed graph
    """

    def __init__(self):
        self._vertices = OrderedSet()
        self._outgoing_edges = defaultdict(OrderedSet)
        self._incoming_edges = defaultdict(OrderedSet)

    def _verify_vertex_exists(self, key):
        if not self.has_vertex(key):
            msg = NO_SUCH_VERTEX_EXC_FMT.format(key)
            raise NoSuchVertexException(msg)

    def _verify_vertex_nonexistant(self, key):
        if self.has_vertex(key):
            msg = DUPLICATE_VERTEX_EXC_FMT.format(key)
            raise DuplicateVertexException(msg)

    def _verify_edge_exists(self, from_key, to_key):
        if not self.has_edge(from_key, to_key):
            msg = NO_SUCH_EDGE_EXC_FMT.format(from_key, to_key)
            raise NoSuchEdgeException(msg)

    def _verify_edge_nonexistant(self, from_key, to_key):
        if self.has_edge(from_key, to_key):
            msg = DUPLICATE_EDGE_EXC_FMT.format(from_key, to_key)
            raise DuplicateEdgeException(msg)

    def has_vertex(self, key):
        return key in self._vertices

    def has_edge(self, from_vertex, to_vertex):
        return all([
            from_vertex in self._vertices,
            to_vertex in self._vertices,
            to_vertex in self._outgoing_edges[from_vertex],
            from_vertex in self._incoming_edges[to_vertex],
        ])

    def vertex_has_edges(self, key):
        return any([
            key in self._outgoing_edges,
            key in self._incoming_edges,
        ])

    def add_vertex(self, key):
        self._verify_vertex_nonexistant(key)
        self._vertices.add(key)
        return key

    def remove_vertex(self, key, remove_edges=False):
        self._verify_vertex_exists(key)
        if not remove_edges and self.vertex_has_edges(key):
            msg = '{} has edges and remove_edges is False'.format(key)
            raise VertexHasEdgesException(msg)
        elif remove_edges and self.vertex_has_edges(key):
            for other_key in self._outgoing_edges[key]:
                self.remove_edge(key, other_key)
            for other_key in self._incoming_edges[key]:
                self.remove_edge(other_key, key)
        self._vertices.remove(key)

    def add_edge(self, from_key, to_key):
        self._verify_vertex_exists(from_key)
        self._verify_vertex_exists(to_key)
        self._verify_edge_nonexistant(from_key, to_key)
        self._outgoing_edges[from_key].add(to_key)
        self._incoming_edges[to_key].add(from_key)

    def remove_edge(self, from_key, to_key):
        self._verify_vertex_exists(from_key)
        self._verify_vertex_exists(to_key)
        self._verify_edge_exists(from_key, to_key)
        self._outgoing_edges[from_key].remove(to_key)
        self._incoming_edges[to_key].remove(from_key)

    def get_outgoing_edges(self, vertex):
        self._verify_vertex_exists(vertex)
        return [key for key in self._outgoing_edges[vertex]]

    def get_incoming_edges(self, vertex):
        self._verify_vertex_exists(vertex)
        return [key for key in self._incoming_edges[vertex]]

    def dfs_traversal(self, starting_vertex):
        """
        Starting from a given vertex, perform a depth first traversal

        Traversal is in-order
        """
        self._verify_vertex_exists(starting_vertex)
        visited = set()
        to_visit = deque([starting_vertex])
        while to_visit:
            curr_vertex = to_visit.popleft()
            if curr_vertex not in visited:
                outgoing = self.get_outgoing_edges(curr_vertex)
                unvisited = [key for key in outgoing if key not in visited]
                # extendleft reverses elements if left to own devices
                to_visit.extendleft(reversed(unvisited))
                visited.add(curr_vertex)
                yield curr_vertex

    def bfs_traversal(self, starting_vertex):
        """
        Starting at the given node, perform a breadth first traversal
        """
        self._verify_vertex_exists(starting_vertex)
        visited = set()
        to_visit = deque([starting_vertex])
        while to_visit:
            curr_vertex = to_visit.popleft()
            if curr_vertex not in visited:
                outgoing = self.get_outgoing_edges(curr_vertex)
                unvisited = [key for key in outgoing if key not in visited]
                to_visit.extend(unvisited)
                visited.add(curr_vertex)
                yield curr_vertex
