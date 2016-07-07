import networkx as nx
from collections import defaultdict
from blist import sortedlist

def weighted_core_number(G,weight='weight'):
	"""Return the core number for each vertex.

	A k-core is a maximal subgraph that contains nodes of degree k or more.

	The core number of a node is the largest value k of a k-core containing
	that node.

	Parameters
	----------
	G : NetworkX graph
	A weighted graph or directed graph

	Returns
	-------
	weighted_core_number : dictionary
	A dictionary keyed by node to the core number.

	Raises
	------
	NetworkXError
		The k-core is not defined for graphs with self loops or parallel edges.

	Notes
	-----
	Not implemented for graphs with parallel edges or self loops.

	For directed graphs the node strenght is defined to be the
	in-strenght + out-strenght.

	References
	----------
	.. [1] http://journals.aps.org/pre/abstract/10.1103/PhysRevE.88.062819
	
	"""
	if G.is_multigraph():
		raise nx.NetworkXError(
				'MultiGraph and MultiDiGraph types not supported.')

	if G.number_of_selfloops()>0:
		raise nx.NetworkXError(
				'Input graph has self loops; the core number is not defined.',
				'Consider using G.remove_edges_from(G.selfloop_edges()).')

	if G.is_directed():
		import itertools
		def neighbors(v):
			return itertools.chain.from_iterable([G.predecessors_iter(v),G.successors_iter(v)])
	else:
		neighbors=G.neighbors_iter

	#--------------
	#per ogni nodo, trova i vicini
	nbrs = dict((v,set(neighbors(v))) for v in G)
	
	#calcola la strength di ogni nodo
	strenght = G.degree(weight=weight)
	nodes_in_strenght_class = defaultdict(set)
	#raggruppa i nodi in classi in base alla loro strength (ogni classe una strength diversa)
	for n,s in strenght.iteritems():
		nodes_in_strenght_class[s].add(n)
	thresholds = sortedlist(nodes_in_strenght_class.keys())
#	thresholds.sort()
	
	max_strenght = max(thresholds)
	
	residual_strenght = strenght
	s_core = {}
	
	#finche' thresholds non e' vuoto
	while thresholds:
		#togli il primo valore da thresholds
		s = thresholds.pop(0)
		print s,max_strenght,'\r',
		#prendi i nodi che hanno strength s
		queue = nodes_in_strenght_class[s]
		#pruning the queue
		while queue:
			#prendine uno, v
			v = queue.pop()
			#assegnagli s_core uguale a s
			s_core[v] = s
			#per ogni suo vicino u
			for u in nbrs[v]:
				#togli v dal vicinato di u
				nbrs[u].remove(v)
				#togli u dai nodi con strength s(u)				
				nodes_in_strenght_class[residual_strenght[u]].remove(u)
				#sottrai alla strength di u il weight del link (u,v)
				residual_strenght[u] -= G[u][v][weight]
				#rimetti u nei nodi con strength s(u) (cambiata)
				nodes_in_strenght_class[residual_strenght[u]].add(u)
				#se la strength di u adesso e' minore di s
				if residual_strenght[u] <= s:
					#metti u nella queue
					queue.add(u)
				else:	
					#altrimenti metti s(u) in thresholds (in modo ordinato)
					thresholds.add(residual_strenght[u])
	return s_core
