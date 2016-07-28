# -*- coding: utf8 -*-

import requests, json
import random


__all__ = ["Graph"]

def test_unicode(text):
    if type(text) == unicode:
        text = str(text)
    return text

class Graph:
    def __init__(self):
        self.url = 'http://localhost:8529'
        self.graph_name = 'graph' + str(random.randint(1, 1000))


    """ Management """

    def list(self):
        """ List all graphs """

        r = requests.get(self.url + '/_api/gharial')
        return r.json()

    def create(self, collection_name, from_list, to_list):
        """ Create a graph """

        if type(from_list) != list:
            from_list = list(from_list)
        if type(to_list) != list:
            to_list = list(to_list)

        data = {
            "name": self.graph_name,
            "edgeDefinitions": [
                {
                    "collection": collection_name,
                    "from": from_list,
                    "to": to_list
                }
            ]
        }
        r = requests.post(self.url + '/_api/gharial',
                          data=json.dumps(data))
        return r.json()

    def drop(self):
        """ Drop a graph """

        r = requests.delete(self.url + '/_api/gharial/' + self.graph_name)
        return r.json()

    def get(self):
        """ Get a graph """

        r = requests.get(self.url + '/_api/gharial/' + self.graph_name)
        return r.json()

    def list_vertex_collections(self):
        """ List vertex collections """

        r = requests.get(self.url + '/_api/gharial/' + self.graph_name + '/vertex')
        return r.json()

    def add_vertex_collection(self, collection_name):
        """ Add vertex collection"""

        data = {
            "collection": collection_name
        }
        r = requests.post(self.url + '/_api/gharial/' + self.graph_name + '/vertex',
                          data=json.dumps(data))
        return r.json()

    def remove_vertex_collection(self, collection_name):
        """ Remove vertex collection """

        r = requests.delete(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name)
        return r.json()

    def list_edge_definitions(self):
        """ List edge collections """

        r = requests.get(self.url + '/_api/gharial/' + self.graph_name + '/edge')
        return r.json()

    def add_edge_definition(self, collection_name, from_list, to_list):
        """ Add edge collection """

        if type(from_list) != list:
            from_list = list(from_list)
        if type(to_list) != list:
            to_list = list(to_list)

        data = {
            "collection": collection_name,
            "from": from_list,
            "to": to_list
        }
        r = requests.post(self.url + '/_api/gharial/' + self.graph_name + '/edge',
                          data=json.dumps(data))
        return r.json()

    def replace_edge_definition(self, collection_name, from_list, to_list):
        """ Replace edge definition """

        if type(from_list) != list:
            from_list = list(from_list)
        if type(to_list) != list:
            to_list = list(to_list)

        data = {
            "collection": collection_name,
            "from": from_list,
            "to": to_list
        }
        r = requests.post(self.url + '/_api/gharial/' + self.graph_name + '/edge' + collection_name,
                          data=json.dumps(data))
        return r.json()

    def remove_edge_definitino(self, collection_name):
        """ Remove edge definition """

        r = requests.delete(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name)
        return r.json()


    """ Vertices """

    def create_vertex(self, collection_name, data):
        """ Create a vertex """

        r = requests.post(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name,
                          data=json.dumps(data))
        return r.json()

    def get_vertex(self, collection_name, vertex_key):
        """ Get a vertex """

        r = requests.get(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name + '/' + vertex_key)
        return r.json()

    def modify_vertex(self, collection_name, vertex_key, data):
        """ Modify a vertex """

        r = requests.patch(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name + '/' + vertex_key,
                           data=json.dumps(data))
        return r.json()

    def replace_vertex(self, collection_name, vertex_key, data):
        """ Replace a vertex """

        r = requests.put(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name + '/' + vertex_key,
                           data=json.dumps(data))
        return r.json()

    def remove_vertex(self, collection_name, vertex_key):
        """ Remove a vertex """

        r = requests.delete(self.url + '/_api/gharial/' + self.graph_name + '/vertex/' + collection_name + '/' + vertex_key)
        return r.json()


    """ Edges """

    def create_edge(self, collection_name, data):
        """ Create an edge """

        r = requests.post(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name,
                          data=json.dumps(data))
        return r.json()

    def get_edge(self, collection_name, edge_key):
        """ Get a edge """

        r = requests.get(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name + '/' + edge_key)
        return r.json()

    def modify_edge(self, collection_name, edge_key, data):
        """ Modify a edge """

        r = requests.patch(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name + '/' + edge_key,
                           data=json.dumps(data))
        return r.json()

    def replace_edge(self, collection_name, edge_key, data):
        """ Replace a edge """

        r = requests.put(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name + '/' + edge_key,
                         data=json.dumps(data))
        return r.json()

    def remove_edge(self, collection_name, edge_key):
        """ Remove a edge """

        r = requests.delete(self.url + '/_api/gharial/' + self.graph_name + '/edge/' + collection_name + '/' + edge_key)
        return r.json()
