class State:
	nodes = {} #id: peker til objekt
	heuristic = None #heuristic til denne staten
	assumption = None

	def __init__(self, nodes):
		self.nodes = nodes
		self.heuristic = self.calculate_heuristic()
	#
	def calculate_heuristic(self):
		h = 0
		for node in self.nodes:
			h = h + len(self.nodes[node].domain) - 1
		return h
	def set_heuristic(self, heuristic): self.heuristic = heuristic
	def get_heuristic(self): return self.heuristic
	#
	def set_assumption(self, assumption): self.assumption = assumption
	def get_assumption(self): return self.assumption
	#
	def revise(node, c):
		pass
	#
	def is_contradictory(self):
		## TODO: implement
		return True

#
#s = State(nodes)