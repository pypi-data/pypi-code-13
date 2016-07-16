from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from itertools import permutations
from random import normalvariate
from random import random
from random import shuffle
from pprint import pprint

from munkres import Munkres

from py_search.search import *

def print_matrix(m):
    for row in m:
        print("\t".join(["%0.2f" % v for v in row]))

def random_assignment(n):
    a = list(range(n))
    shuffle(a)
    return tuple(a)

def mary_cost_dict(n, m, r):
    """
    n x n is the number of number of objects in being matched
    
    m specifies the number of objects contained in relations
    """
    objs = list(range(n))
    costs = {}

    for i in range(1, m+1):
        for p1 in permutations(objs, i):
            if random() > r**i:
                continue
            for p2 in permutations(objs, i):
                if p1 not in costs:
                    costs[p1] = {}
                costs[p1][p2] = normalvariate(0,1)

    return costs

def cost(assignment, cost_dict):
    c = 0
    m = 1
    for k in cost_dict:
        if len(k) > m:
            m = len(k)

    for i in range(1,m+1):
        for p in permutations(assignment, i):
            if p in cost_dict:
                mp = tuple([assignment[v] for v in p])
                if mp in cost_dict[p]:
                    c += cost_dict[p][mp]

    return c

def compile_matrix(n, cost_dict):
    #costs = [[cost_dict[(r,)][(c,)] for c in range(n)] for r in range(n)]
    costs = [[0.0 for c in range(n)] for r in range(n)]

    for t in cost_dict:
        for ct in cost_dict[t]:
            for i, r in enumerate(t):
                c = ct[i]
                costs[r][c] += cost_dict[t][ct] / len(t)

    return costs

class TreeNaryAssignment(Problem):

    def h(self, node):
        node.state
        costs, unassigned = node.extra

        empty_rows = [i for i,v in enumerate(node.state) if v is None]

        min_possible = 0
        for r in empty_rows:
            sub_c = [v for i, v in enumerate(costs[r]) if i in unassigned]
            min_possible += min(sub_c)

        return min_possible

    def node_value(self, node):
        return node.cost() + self.h(node)

    def successors(self, node):
        state = node.state
        costs, unassigned = node.extra

        for i,v in enumerate(state):
            if v is None:
                for u in unassigned:
                    new_state = tuple([u if i==j else k 
                                       for j,k in enumerate(state)])
                    new_unassigned = tuple([k for k in unassigned if k != u])
                    
                    c = node.cost() + costs[i][u]
                    yield Node(new_state, node, (i, u), c, extra=(costs,
                                                            new_unassigned))

    def goal_test(self, node):
        state = node.state
        return None not in state

class OptNaryAssignment(OptimizationProblem):
    """
    This class represents an assignment problem and instantiates the successor
    and goal test functions necessary for conducting search. 
    """
    def node_value(self, node):
        """
        Function for computing the value of a node.
        """
        state = node.state
        costs = node.extra[0]

        #if cost(state, costs) != node.cost():
        #    print(node.cost())
        #    print(cost(state, costs))
        #    print()
        #    assert False
        return cost(state, costs)
    
    def random_successor(self, node):
        costs = node.extra[0]

        r1 = randint(0, len(node.state))
        r2 = r1
        while r1 == r2:
            r2 = randint(0, len(node.state))

        new_cost = node.cost()
        new_cost -= costs.get((r1,), {}).get(node.state[r1],0.0)
        new_cost -= costs.get((r2,), {}).get(node.state[r2],0.0)
        new_cost += costs.get((r1,), {}).get(node.state[r2],0.0)
        new_cost += costs.get((r2,), {}).get(node.state[r1],0.0)

        state = list(node.state)
        temp = state[r1]
        state[r1] = state[r2]
        state[r2] = temp

        # add rewards of things changed to

        yield Node(tuple(state), node, p, new_cost, extra=node.extra)

    def successors(self, node):
        """
        Generates successor states by flipping each pair of assignments. 
        """
        costs = node.extra[0]
    
        for p in permutations(node.state, 2):
            new_cost = node.cost()
            new_cost -= costs.get((p[0],), {}).get(node.state[p[0]],0.0)
            new_cost -= costs.get((p[1],), {}).get(node.state[p[1]],0.0)
            new_cost += costs.get((p[0],), {}).get(node.state[p[1]],0.0)
            new_cost += costs.get((p[1],), {}).get(node.state[p[0]],0.0)
            # subtract and add relational rewards

            state = list(node.state)
            temp = state[p[0]]
            state[p[0]] = state[p[1]]
            state[p[1]] = temp

            # add rewards of things changed to

            yield Node(tuple(state), node, p, new_cost, extra=node.extra)

if __name__ == "__main__":

    n = 10
    m = 1 
    r = 100
    costs = mary_cost_dict(n, m, r)
    print("Costs constructed!")

    initial = random_assignment(n)
    print(initial)
    initial_cost = cost(initial, costs)
    print(initial_cost)

    compiled_m = compile_matrix(n, costs)
    compiled_d = {(r,): {(c,): compiled_m[r][c] for c in range(n)} for r in
                  range(n)}
    #print()
    #print("Compiled Matrix:")
    #print_matrix(compiled_m)
    #print()

    m = Munkres()
    indices = m.compute(compiled_m)
    munkres_sol = tuple([v[1] for v in indices])
    print("MUNKRES SOLUTION")
    print(munkres_sol)
    print("Compiled cost:")
    print(cost(munkres_sol, compiled_d))
    print()
    print("Actual cost:")
    print(cost(munkres_sol, costs))
    print()

    problem = OptNaryAssignment(initial, initial_cost=initial_cost, extra=(costs,)) 
    problem2 = OptNaryAssignment(munkres_sol, 
                                initial_cost=cost(munkres_sol, costs),
                                extra=(costs,)) 

    def beam1(problem):
        return beam_search_opt(problem, beam_width=1)
    def beam2(problem):
        return beam_search_opt(problem, beam_width=2)
    def annealing(problem):
        return simulated_annealing_opt(problem)

    compare_searches(problems=[problem],#, problem2],
                     searches=[beam1])#, beam2, annealing])

    ## TREE SEARCH APPROACH
    #empty = tuple([None for i in range(len(costs))])
    #unassigned = [i for i in range(len(costs))]

    ##new_costs = [[c - min(row) for c in row] for row in costs]
    ##min_c = [min([row[c] for row in costs]) for c,v in enumerate(costs[0])]
    ##new_costs = [[v - min_c[c] for c, v in enumerate(row)] for row in costs]

    #tree_problem = TAssignmentProblem(empty, extra=(costs,unassigned)) 
    ##sol = next(beam_search(tree_problem))
    ##sol.extra = (costs, tuple())
    ##print(problem.node_value(sol))

    #def Tbeam_2(problem):
    #    return beam_search(problem, beam_width=2)

    #print()
    #compare_searches(problems=[tree_problem],
    #                 searches=[#simulated_annealing_opt,
    #                           beam_search,
    #                           Tbeam_2])
    #                           #best_first_search])
    #                           #restart_hill])
