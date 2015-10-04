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
		self.board = [[None for x in xrange(len(self.cols))] for x in xrange(len(self.rows))]
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
	def set_h(self, h): self.h = h
	#
	def get_rows(self): return self.rows
	def get_row(self, index): return self.rows[index]
	def set_row(self, index, new_row): self.rows[index].domain=new_row
	#
	def get_cols(self): return self.cols
	def get_col(self, index): return self.cols[index]
	def set_col(self, index, new_col): self.cols[index].domain=new_col
	#
	def get_board(self): return self.board
	def get_board_cell(self, row, col): return self.board[row][col]
	def set_board_cell(self, row, col, val): self.board[row][col] = val
	def make_board(self):
		for row in self.rows:
			if len(row.domain) == 1:
				for n in xrange(len(row.domain[0])):
					if row.domain[0][n] == '1':
						self.board[row.index][n] = True
					elif row.domain[0][n] == '0':
						self.board[row.index][n] = False
			else:
				#print len(row.domain[0])
				temp_list = [True]*len(row.domain[0])
				for d_index in xrange(1, len(row.domain)):
					for n in xrange(0, len(row.domain[d_index])):
						if temp_list[n] and row.domain[0][n] != row.domain[d_index][n]:
							temp_list[n] = False
				#
				for n in xrange(len(temp_list)):
					if temp_list[n] == True:
						if row.domain[0][n] == '1':
							self.board[row.index][n] = True
						elif row.domain[0][n] == '0':
							self.board[row.index][n] = False
					else:
						self.board[row.index][n] = None
		######
		for col in self.cols:
			if len(col.domain) == 1:
				for n in xrange(len(col.domain[0])):
					if self.board[n][col.index] == None:
						if col[0][n] == '1':
							self.board[n][col.index] = True
						elif col[0][n] == '0':
							self.board[n][col.index] = False
					elif col[0][n] == '1' and self.board[n][col.index] == False:
						self.board[n][col.index] = None
					elif col[0][n] == '0' and self.board[n][col.index] == True:
						self.board[n][col.index] = None
					elif col[0][n] == '1' and self.board[n][col.index] == False:
						return False, []
					elif col[0][n] == '0' and self.board[n][col.index] == True:
						return False, []
			else:
				temp_list = [True]*len(col.domain[0])
				for d_index in xrange(1, len(col.domain)):
					for n in xrange(len(col.domain[d_index])):
						if temp_list and col.domain[0][n] != col.domain[d_index][n]:
							temp_list[n] = False
				#
				for n in xrange(len(temp_list)):
					if temp_list[n]:
						if col.domain[0][n] == '1':
							if self.board[n][col.index] == None:
								self.board[n][col.index] = True
							elif self.board[n][col.index] == False:
								return False, []
							elif self.board[n][col.index] == True:
								self.board[n][col.index] = True

						elif col.domain[0][n] == '0':
							if self.board[col.index][n] == None:
								self.board[col.index][n] = False
							elif self.board[col.index][n] == True:
								return False, []
							elif self.board[n][col.index] == False:
								self.board[col.index][n] = False
					else:
						if self.board[col.index][n] == None:
							self.board[col.index][n] = None
						elif self.board[col.index][n] == True:
							self.board[col.index][n] = True
						elif self.board[col.index][n] == False:
							self.board[col.index][n] = False
		#for b in self.board:
			print b
		b = []
		for row in xrange(len(self.board)):
			rad = ''
			for col in xrange(len(self.board[row])):
				if self.board[row][col] == True:
					rad += '1'
				elif self.board[row][col] == False:
					rad += '0'
				else:
					rad += '2'
			b.append(rad)

		return True, b
					

	#
	def get_parent(self): return self.parent
	#
	def get_assumption(self): return self.assumption
	def set_assumption(self, assumption): self.assumption = assumption
