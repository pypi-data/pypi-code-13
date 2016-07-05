from origami_dense import PillowcaseCover_dense_pyx
from sage.groups.perm_gps.permgroup import PermutationGroupElement


def PillowcaseCover(g0, g1, g2, g3=None,
        sparse=False,
        check=True,
        as_tuple=False,
        positions=None, name=None):
    r"""
    Pillowcase cover constructor.
    """
    if not as_tuple:
        g0 = PermutationGroupElement(g0, check=check)
        g1 = PermutationGroupElement(g1, check=check)
        g2 = PermutationGroupElement(g2, check=check)
        if g3 is None:
            g3 = (~g2) * (~g1) * (~g0)
        else:
            g3 = PermutationGroupElement(g3, check=check)

        g0 = [i-1 for i in g0.domain()]
        g1 = [i-1 for i in g1.domain()]
        g2 = [i-1 for i in g2.domain()]
        g3 = [i-1 for i in g3.domain()]

        N = max([len(g0),len(g1),len(g2),len(g3)])
        g0.extend(xrange(len(g0),N))
        g1.extend(xrange(len(g1),N))
        g2.extend(xrange(len(g2),N))
        g3.extend(xrange(len(g3),N))

    elif check:
        s0 = set(g0)
        s1 = set(g1)
        s2 = set(g2)
        s3 = set(g3)
        N = len(g0)
        if len(g1) != N or len(g2) != N or len(g3) != N:
            raise ValueError("the four tuples must be of the same length")
        for i in xrange(N):
            if not i in g0:
                raise ValueError("%d is not in g0=%s" %(i,str(g0)))
            if not i in g1:
                raise ValueError("%d is not in g1=%s" %(i,str(g1)))
            if not i in g2:
                raise ValueError("%d is not in g2=%s"%(i,str(g2)))
            if not i in g3:
                raise ValueError("%d is not in g3=%s"%(i,str(g3)))

    pcc = PillowcaseCover_dense(tuple(g0),tuple(g1),tuple(g2),tuple(g3))

    if name is not None:
        pcc.rename(name)
#    if positions is not None:
#        o.set_positions(positions)
    if check:
        pcc._check()
    return pcc

class PillowcaseCover_dense(PillowcaseCover_dense_pyx):
    r"""
    Generic class for pillowcase cover.
    """
    def _repr_(self):
        return '\n'.join("g_%d = %s"%(i,self.g(i)) for i in xrange(4))

    def g(self,i=None):
        r"""
        Return the ``i``-th permutation that defines this pillowcase cover.
        """
        if i is None:
            return self.g(0), self.g(1), self.g(2), self.g(3)

        i = int(i)
        if i < 0 or i > 3:
            raise IndexError("the index i (={}) must be in {{0,1,2,3}}".format(i))

        return PermutationGroupElement([j+1 for j in self.g_tuple(i)], check=False)

    def _check(self):
        x = self.g(0) * self.g(1) * self.g(2) * self.g(3)
        if not x.is_one():
            raise ValueError

    def monodromy(self):
        r"""
        Return the monodromy group of the pillowcase cover.

        The monodromy group of an origami is the group generated by the
        permutations `g_i` for `i` in 0,1,2,3.
        """
        from sage.groups.perm_gps.permgroup import PermutationGroup
        return PermutationGroup(self.g())

    def as_graph(self):
        r"""
        Return the graph associated to self
        """
        from sage.graphs.digraph import DiGraph

        G = DiGraph(multiedges=True,loops=True)
        d = self.degree()
        g = [self.g_tuple(i) for i in xrange(4)]
        for i in xrange(d):
            for j in xrange(4):
                G.add_edge(i,g[j][i],j)
        return G

    def is_connected(self):
        r"""
        Check whether the origami is connected or not

        It is equivalent to ask whether the group generated by `r` and `u` acts
        transitively on the `\{1,\dots,n\}`.
        """
        return self.as_graph().is_connected()

    def connected_components(self):
        r"""
        Return the list of connected origami that composes this origami.
        """
        cc = self.as_graph().connected_components()
        g = [self.g_tuple(i) for i in xrange(4)]
        if len(cc) == 1:
            return [self]
        l = []
        for c in cc:
            gg = [[None] * len(c) for _ in xrange(4)]
            d = dict((c[i],i) for i in xrange(len(c)))
            for i in c:
                for j in xrange(4):
                    gg[j][d[i]] = d[g[j][i]]
            l.append(Pillowcase_cover(g[0],g[1],g[2],g[3],check=True,as_tuple=True))
        return l

    def is_orientable(self):
        r"""
        Test whether the foliation is orientable.
        """
        return self.as_graph().to_undirected().is_bipartite()

    def to_origami(self):
        r"""
        If self is orientable returns it as a cover of a torus, otherwise raise
        an AssertionError.
        """
        assert self.is_orientable()

        raise NotImplementedError

    def profile(self,i=None):
        r"""
        Return the profile (= ramification type above each pole).
        """
        if i is None:
            return [self.profile(i) for i in xrange(4)]
        return sorted((len(c) for c in self.g(i).cycle_tuples(singletons=True)),reverse=True)

    def stratum(self,fake_zeros=False):
        r"""
        Return the stratum of self. It may be either a stratum of Abelian or
        quadratic differentials.
        """
        p = sum(self.profile(),[])
        if self.is_orientable():
            from surface_dynamics.flat_surfaces.abelian_strata import AbelianStratum
            if fake_zeros:
                zeros = [(i-2)//2 for i in p]
            else:
                zeros = [(i-2)//2 for i in p if i != 2]
            if zeros == []:
                return AbelianStratum([0])
            return AbelianStratum(zeros)

        else:
            from surface_dynamics.flat_surfaces.quadratic_strata import QuadraticStratum
            if fake_zeros:
                zeros = [i-2 for i in p]
            else:
                zeros = [i-2 for i in p if i != 2]
            return QuadraticStratum(zeros)

    def is_primitive(self, return_base=False):
        r"""
        A pillowcase cover is primitive if it does not cover an other pillowcase
        cover.
        """
        from sage.arith.all import is_prime
        if is_prime(self.degree()):
            return True

        return bool(gap.IsPrimitive(self.monodromy()))


