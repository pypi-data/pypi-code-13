import copy
import uuid

import QuantLib as ql
import networkx as nx

from converters import QuantLibConverter as qlf
from .common import DataType as D
from .fields import Field as F, FieldName


class Controller(object):
    _ROOT = "~ROOT~"

    def __init__(self, data, context=None):
        self._data = copy.deepcopy(data)
        self._graph = nx.DiGraph()
        self._context = context
        edges = []
        self._parse_nodes(self._data, self._graph, edges)
        self._parse_context_nodes(self._context, self._graph)
        self._parse_edges(self._graph, edges)
        self._node_creators = self._compile_node_creator_list()


    def parse(self):
        for n, c in self._node_creators:
            if c:
                c.check()

    def process(self, asof_date, check=True, parse=True):
        asof_date = qlf.to_date(asof_date)
        ql.Settings.instance().evaluationDate = asof_date

        if parse:
            self.parse()

        for n, c in self._node_creators:
            obj = c.create(asof_date) if c else self._graph.node[n]["data"].get(F.OBJECT.id)
            for p in self._graph.predecessors(n):
                edge = self._graph.edge[p][n]
                field_id = edge.get("field_id")
                if field_id:
                    data = self._graph.node[p]["data"]
                    field = FieldName.lookup(field_id)
                    if field.check_type(obj):
                        data[field_id] = obj
                        edge["resolved"] = True
                    else:
                        raise ValueError("Incompatible data type for field %s in object %s" %(field_id, p))

        return self._data

    def object_data(self, object_id):
        return self._graph.node[object_id].get("data")

    def object(self, object_id):
        return self.object_data(object_id)[F.OBJECT.id]

    @property
    def data(self):
        return self._data

    @classmethod
    def _parse_nodes(cls, data_list, graph, edges, parent_id=_ROOT):
        for data in data_list:
            data.setdefault(F.OBJECT_ID.id, str(uuid.uuid4()))
            object_id = data[F.OBJECT_ID.id]
            template = qlf.to_template(data[F.TEMPLATE.id])
            creator = template.get_creator()(data)
            if graph.has_node(object_id):
                raise ValueError("Duplicate ObjectId %s found" % object_id)
            graph.add_node(object_id, template=template, creator=creator, data=data)
            edges.append((parent_id, object_id, {}))  # dependency that doesn't need injection

            for field_id, value in data.iteritems():
                field = FieldName.lookup(field_id)
                if isinstance(value, str) and value[:2] == '->':
                    dependency = value[2:].strip()
                    edges.append((object_id, dependency, {"field_id": field_id}))  # dependency needs injection

                if (field.data_type == D.LIST) and isinstance(value, list):
                    cls._parse_nodes(value, graph, edges, object_id)
        return

    @classmethod
    def _parse_context_nodes(cls, data_list, graph):
        if data_list:
            for data in data_list:
                data.setdefault(F.OBJECT_ID.id, str(uuid.uuid4()))
                object_id = data[F.OBJECT_ID.id]
                graph.add_node(object_id, data=data)

                for field_id, value in data.iteritems():
                    field = FieldName.lookup(field_id)

                    if (field.data_type == D.LIST) and isinstance(value, list):
                        cls._parse_context_nodes(value, graph)
            return




    @classmethod
    def _parse_edges(cls, graph, edges):
        for parent, child, attr in edges:
            graph.add_edge(parent, child, attr)

    def _compile_node_creator_list(self):
        graph = self._graph
        cycles = list(nx.simple_cycles(graph))
        if len(cycles):
            raise ValueError("Found cycles in dependencies "+str(cycles))
        else:
            nodes = list(nx.dfs_postorder_nodes(graph))
            nodes.remove(self._ROOT)  # exclude root
            creators = []
            for n in nodes:
                creator = graph.node[n].get('creator')
                creators.append((n, creator))
            return creators

    def output(self, object_id, param_dict=None):
        creator = self._graph.node[object_id]['creator']
        return creator.output(param_dict)