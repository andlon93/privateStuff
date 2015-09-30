class State:
	g = None
	h = None
	rows = []
	cols = []
	board = []
	parent = None
	assumption = None
	#
	def __init__(self, rows, cols, parent):
		self.rows = rows
		self.cols = cols
		self.parent = parent
		self.g = self.calculate_g()
		self.h = self.calculate_h()
		self.board = [[-1 for x in xrange(len(self.cols))] for x in xrange(len(self.rows))]
	#
	def calculate_h(self):
		h = 0
		for n in self.get_rows():
			h += len( n.get_domain() ) - 1
		for n in self.get_cols():
			h += len( n.get_domain() ) - 1
		return h
	def calculate_g(self):
		if not self.get_parent() == None: return self.get_parent().get_g() + 1
		else: return 0
	##-- Getters and setters--##
	def get_g(self): return self.g
	def get_h(self): return self.h
	#
	def get_rows(self): return self.rows
	def get_row(self, index): return self.rows[index]
	def set_row(self, index, new_row): self.rows[index]=new_row
	#
	def get_cols(self): return self.cols
	def get_col(self, index): return self.cols[index]
	def set_col(self, index, new_col): self.cols[index]=new_col
	#
	def get_board(self): return self.board
	def get_board_cell(self, row, col): return self.board[row][col]
	#
	def get_parent(self): return self.parent
	#
	def get_assumption(self): return self.assumption
	def set_assumption(self, assumption): self.assumption = assumption 