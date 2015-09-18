class Node:
	index = None
	x = None
	y = None
	domain = []
	def __init__(self, index, x, y, domain_size):
		self.index = index
		self.x = x
		self.y = y
		self.domain = range(0, domain_size)