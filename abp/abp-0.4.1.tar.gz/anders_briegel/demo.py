import graphsim

N = 6
gr = graphsim.GraphRegister(N)

# Make cluster state
for i in range(N):
    gr.hadamard(i)

for i in range(N-1):
    gr.cphase(i, i+1)

#gr.print_adj_list()
#gr.print_stabilizer()

   
#print gr.get_full_stabilizer().paulis
print gr.get_adj_list()

