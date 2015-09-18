class State:
	nodes = {} #id: peker til objekt
	heuristic = None #heuristic til denne staten

	def __init__(self, nodes):
		self.nodes = nodes
		heuristic = self.calculate_heuristic(nodes)

	def calculate_heuristic(self, nodes):
		h = 0
		for i in nodes:
			h = h + len(nodes[i]) - 1
			print h
		return h

	def revise(node, c):
		pass

nodes = {0: [0, 1, 2],
         1: [0, 1, 2],
	     2: [0]
				     }

s = State(nodes)