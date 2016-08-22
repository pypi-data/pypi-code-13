#!/usr/bin/python
""" Implementation of generic directed graph. Undirected graph could be modeled with two directional links.
    Terminology: if node A has link to node B, node A is referred as 'source' and node B  is referred as 'target'. 
    Graph can have only one node with label A and only one link from node A to node B. Attempt to add second node or link will.
        end up with replacement of previous one.
    To preserve consistent state nodes A and B should be present in graph to add link from A to B (or backward).
    All connection information resides in graph. node and links are independent from each other. 
    basic_graph._nodes maps label to node - _nodes[label] = node
    basic_graph._forward_links hold links from source perspective - _forward_links[source][target] = link
    basic_graph._backward_links hold the same links from target perspective -  _backward_links[target][source] = link
        _forward_links[A][B] = _backward_links[B][A]
"""
class BasicNode(object):
    """ Basic Node class.
    """
    def __init__(self):
        self._graph = None        
    
    def __str__(self):
        return "%s %d"%(type(self), id(self))
        
class BasicGraph(object):
    """ Graph class, top level container for Nodes and Links.
    """
    class Link(object):
        """ Link representation, place holder for graph specific data.
        """   
        def __init__(self, graph):
            self._graph = graph
            
        def __str__(self):
            return "%s %d"%(type(self), id(self))
        
    def __init__(self, name):
        self._name = name
        # dictionaries nodes {label: node}
        self._nodes = {}
        # dictionary of dictionaries {source : { targets : links}}
        self._forward_links = {}
        # dictionary of dictionaries {target : { sources : links}}
        self._backward_links = {}
        # dictionary of tuples {link: (source, target)}
        self.linked = {}

    def __str__(self):
        return "%s %d, name: %s"%(type(self), id(self), self._name)
                             
    def add_node(self, node, label):
        """ Add given node to the graph.
        If label is present, corresponding node will be replaced with new one.
        """
        node._graph = self
        if (label in self._nodes):
            print "Warning: Node %s already exist in graph and will be replaced" % (label)
        self._nodes[label] = node
        self._forward_links[label] = {}
        self._backward_links[label] = {}
        
    def link(self, source, target):
        """ Add link to the graph.
        Link from node with label 'source' to node with label 'target'
        Nodes should be present in graph.
        """
        assert source in self._nodes, "Node '%s' is not in Graph"%(source)
        assert target in self._nodes, "Node '%s' is not in Graph"%(target)
        link = self.Link(self)
        self._forward_links[source][target] = link
        self._backward_links[target][source] = link
        self.linked[link] = (source, target)
               
    def get_labels(self):
        """ Return list of all labels in graph. 
        """
        return self._nodes.keys()
           
    def get_node(self, label):
        """ Return node with given label or None if not present.
        """
        if (label in self._nodes):
            return self._nodes[label]
        else: 
            return None
      
    def get_targets(self, source):
        """ Return labels for all nodes which have links 
        from node with 'source' label. 
        """
        return self._forward_links[source].keys()
    
    def get_sources(self, target):
        """ Return labels for all nodes which have links 
        to node with 'target' label. 
        """
        return self._backward_links[target].keys()
        
    def get_link(self, source, target):
        """ Return link object connecting node with label 'source' 
        to node with label 'target' or None if not connected. 
        """
        if (target in self._forward_links[source]):
            return self._forward_links[source][target]
        else:
            return None
    
    def get_linked_labels(self, link):
        """ Return end-points labels for given link
        """
        if link in self.linked:
            return self.linked[link]
        else:
            return None 
        
                       
    def display(self):
        """ Display graph structure.
        """
        print self
        for label in self.get_labels():
            print "", label, ":", self.get_node(label)
            for target in self.get_targets(label):
                print "  |" , self.get_link(label,target)
                print "  |->" , target, ":", self.get_node(target)


def test():
    """ Test function/usage example
    """       
    gr = BasicGraph("test graph")
    n1 = BasicNode()
    n2 = BasicNode()      
    gr.add_node(n1, "N1")
    gr.add_node(n2, "N2")
    gr.add_node(BasicNode(), 12.3)
    gr.link("N1", "N2")
    gr.link("N1",12.3)    
    
    gr.display()
        
if __name__ == '__main__':
    test()        
        
        