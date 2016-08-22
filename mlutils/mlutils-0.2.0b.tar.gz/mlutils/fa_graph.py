#!/usr/bin/python
""" Implementation of Finite Automata network on base of basic directed graph.   
    Link from Node A to Node B represent dependency of Node A from Node B 
        and Node A will be updated as A.state = A.update(A.state, [B.state]).
"""
from mlutils import basic_graph as bg
import copy as cp

class FANode(bg.BasicNode):
    """ Node with state.
    """
    def __init__(self, initial_state, update_func):
        super(FANode, self).__init__()
        self.state = initial_state
        self.update = update_func
        
    def __str__(self):
        return "%s, state : %s "%(type(self), str(self.state)) 
        
class FAGraph(bg.BasicGraph):
    """ Implementation of finite automata state machine.
    """    
    def __init__(self, name):
        super(FAGraph, self).__init__(name)
        
    def step(self):
        """ Move finite automata graph to next state. 
        1. Latch states of all nodes.
        2. Update states of all nodes based on current state and 
        states of all nodes given node has dependency on.  
        """  
        # latch arguments
        for label in self.get_labels():
            for target in self.get_targets(label):
                    self.get_link(label,target).arg = cp.deepcopy(self.get_node(target).state)

        # move to next states
        for label in self.get_labels():
            node = self.get_node(label)
            args = []
            for target in self.get_targets(label):
                args.append(self.get_link(label,target).arg)
            node.state = node.update(node.state, args)   
                
        
def test():
    """ Test function/usage example
    """
    fa = FAGraph("FibNums")
    fa.add_node(FANode(1, lambda state, args: args[0]), "F(-1)") 
    fa.add_node(FANode(1, lambda state, args: state + args[0]), "F(0)")
    fa.link("F(0)", "F(-1)")  
    fa.link("F(-1)", "F(0)")
           
    for i in range(10):
        print "F(%d) = %d" % (i+1, fa.get_node("F(0)").state)
        fa.step()

    fa.display()

if __name__ == '__main__':
    test()