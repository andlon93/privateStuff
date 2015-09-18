class State:
	nodes = {} #id: peker til objekt
	heuristic = None #heuristic til denne staten
	#
	def __init__(self, nodes):
		self.nodes = nodes
		heuristic = self.calculate_heuristic(nodes)
	#
	def calculate_heuristic(self, nodes):
		h = 0
		for node in nodes:
			h = h + len(nodes[node].domain) - 1
		return h
	#
	def revise(node, c):
		pass
#
#s = State(nodes)