class State:
	nodes = {} #id: peker til objekt
	heuristic = None #heuristic til denne staten

	def __init__(nodes):
		self.nodes = nodes
		heuristic = calculate_heuristic()

	def calculate_heuristic():
		return 1

	def revise(node, c):
		pass