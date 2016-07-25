import graphsim as gs

r = gs.GraphRegister(5)
r.hadamard(0)
r.hadamard(1)
r.cphase(0, 1)
print r.get_adj()
print r.get_vop()

