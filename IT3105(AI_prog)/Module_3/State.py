class State:
	g = None
	h = None
	rows = []
	cols = []
	parent = None
	#
	def __init__(self, rows, cols, parent):
		self.rows = rows
		self.cols = cols
		self.parent = parent
		self.g = self.calculate_g()
		self.h = self.calculate_h()
	#
	def calculate_h(self):
		h = 0
		for n in self.get_rows():
			h += len( n.get_domain() ) - 1
		for n in self.get_cols():
			h += len( n.get_domain() ) - 1
		return h
	def calculate_g(self):
		if self.get_parent() == None: return 0
		else: return self.get_parent().get_g() + 1
	##-- Getters and setters--##
	def get_g(self): return self.g
	def get_h(self): return self.h
	#
	def get_rows(self): return self.rows
	def get_row(self, index): return self.rows[index]
	#
	def get_cols(self): return self.cols
	def get_col(self, index): return self.cols[index]
	#
	def get_parent(self): return self.parent