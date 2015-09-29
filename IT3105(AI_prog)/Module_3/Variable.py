class Variable:
	domain = []
	is_row = None
	index = None
	#
	def __init__(self, is_row, index, blocks, length):
		self.is_row = is_row
		self.index = index
		self.create_full_domain(blocks, length)
	#
	def create_full_domain(self, blocks, length):
		self.domain = [0]
		#create the full domain
	##-- Getters --##
	def get_domain(self): return self.domain
	def get_is_row(self): return self.is_row
	def get_index(self): return self.index