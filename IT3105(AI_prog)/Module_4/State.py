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
		   Same prob for every open tile on the board'''
	#
	def calculate_heuristic(self):
		'''Based on one or more algorithms the quality/closeness to target
		   is calculated'''
		return h
	##-- Getters and setter --##
	def get_tile(self, row, column): return self.board[row][column]
	def set_tile(self, row, column, value): self.board[row][column] = value
	#
	def get_board(self): return self.board
	#
	def get_h(self): return self.h