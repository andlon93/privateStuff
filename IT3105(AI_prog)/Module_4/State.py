import random
#
class State:
	#
	board = []
	h = None
	#
	def __init__(self, board):
		self.board = board
	#
	def move(self, direction):
		'''updates the board based on a move in a given direction
		   May add submethods for moving the tiles and merging tiles'''
		pass
	#
	def spawn(self):
		'''A new 2 or 4 tile spawns on the board.
		   P(2) = 0.9  --  P(4) = 0.1
		   Same prob for every open tile on the board
		'''
		open_tiles = []#list of all tiles with a zero in it
		for row in xrange(4):#iterate over the board
			for col in xrange(4):
				#if tile is zero, a spawn may happen in it
				if self.board[row][col] == 0: open_tiles.append([row, col])
		#
		chosen_tile = open_tiles[random.randint(0, len(open_tiles)-1)]#choose a random tile
		print chosen_tile
		if random.randint(0, 100) < 10:#P(4) = 0.1
			self.board[chosen_tile[0]][chosen_tile[1]] = 4
		else:#P(2) = 0.9
			self.board[chosen_tile[0]][chosen_tile[1]] = 2
	#
	def calculate_heuristic(self):
		'''Based on one or more algorithms the quality/closeness to target
		   is calculated
		'''
		h = 0
		return h
	##-- Getters and setter --##
	def get_tile(self, row, column): return self.board[row][column]
	def set_tile(self, row, column, value): self.board[row][column] = value
	#
	def get_board(self): return self.board
	#
	def get_h(self): return self.h

board =[[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0],
		[0,0,0,0]]
s = State(board)
print s.get_board()
for n in xrange(16):
	s.spawn()
print s.get_board()