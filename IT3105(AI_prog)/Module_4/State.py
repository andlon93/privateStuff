from __future__ import division
import random
from collections import deque
import copy

#
class State:
	#
	board = []
	utility = None
	#
	def __init__(self, board):
		self.board = board
	####--- Move methods ---####
	def move_up(self, col):
		rute_ledig = deque()#legger inn tomme ruter i en ko
		for row in xrange(4):
			if self.board[row][col] == 0:#hvis ledig rute -> legg inn i ko
				rute_ledig.append([row, col])
			else:#hvis ikke
				if rute_ledig:
					'''Hvis ledig rute finnes:
					   legg inn verdi i forste rute i ko og fjern den fra ko
					   gjor verdi i denne rute til 0 og legg den inn i ko
					'''
					self.board[rute_ledig[0][0]][rute_ledig[0][1]] = self.board[row][col]
					self.board[row][col] = 0
					rute_ledig.popleft()
					rute_ledig.append([row, col])
	def move_down(self, col):
		'''For code explanation see move_up()'''
		rute_ledig = deque()
		for row in xrange(3, -1, -1):
			if self.board[row][col] == 0: rute_ledig.append([row, col])
			else:
				if rute_ledig:
					self.board[rute_ledig[0][0]][rute_ledig[0][1]] = self.board[row][col]
					self.board[row][col] = 0
					rute_ledig.popleft()
					rute_ledig.append([row, col])
	def move_right(self, row):
		'''For code explanation see move_up()'''
		rute_ledig = deque()
		for col in xrange(3, -1, -1):
			if self.board[row][col] == 0: rute_ledig.append([row, col])
			else:
				if rute_ledig:
					self.board[rute_ledig[0][0]][rute_ledig[0][1]] = self.board[row][col]
					self.board[row][col] = 0
					rute_ledig.popleft()
					rute_ledig.append([row, col])
	def move_left(self, row):
		'''For code explanation see move_up()'''
		rute_ledig = deque()
		for col in xrange(4):
			if self.board[row][col] == 0: rute_ledig.append([row, col])
			else:
				if rute_ledig:
					self.board[rute_ledig[0][0]][rute_ledig[0][1]] = self.board[row][col]
					self.board[row][col] = 0
					rute_ledig.popleft()
					rute_ledig.append([row, col])
	#
	def move(self, direction):
		'''updates the board based on a move in a given direction
		   May add submethods for moving the tiles and merging tiles
		   0 = up
		   1 = right
		   2 = down
		   3 = left
		   direction == 0 has code explanation. almost identical for every move
		'''
		if direction == 0:#hvis move er up
			for col in xrange(4):#iterer over brett kolonne for kolonne
				self.move_up(col)#Move tiles up
				##-- Merge start --##
				rute_ledig = deque()
				for row in xrange(3):
					if self.board[row][col] == self.board[row+1][col]:#merge ruter om de er like
						self.board[row][col] = self.board[row][col] * 2#sett overste til dobbel verdi
						self.board[row+1][col] = 0#sett den under til 0
				##-- Merge end --##
				self.move_up(col)#move tiles up again
		elif direction == 2:#hvis move er down
			for col in xrange(3, -1, -1):
				self.move_down(col)
				##-- Merge start --##
				rute_ledig = deque()
				for row in xrange(3, 0, -1):
					if self.board[row][col] == self.board[row-1][col]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row-1][col] = 0
				##-- Merge end --##
				self.move_down(col)
		elif direction == 1:#hvis move er right
			for row in xrange(4):
				self.move_right(row)
				##-- Merge start --##
				rute_ledig = deque()
				for col in xrange(3, 0, -1):
					if self.board[row][col] == self.board[row][col-1]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row][col-1] = 0
				##-- Merge end --##
				self.move_right(row)
		elif direction == 3:#move left
			for row in xrange(4):
				self.move_left(row)
				##-- Merge start --##
				rute_ledig = deque()
				for col in xrange(3):
					if self.board[row][col] == self.board[row][col+1]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row][col+1] = 0
				##-- Merge end --##
				self.move_left(row)
		else:
			print "wrong direction input given"
	#
	####--- Spawn a 2 or 4 ---####
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
		if open_tiles:
			chosen_tile = open_tiles[random.randint(0, len(open_tiles)-1)]#choose a random tile
		else:
			print "ingen steder aa spawne en tile"
			return False
		if random.randint(0, 100) < 10:#P(4) = 0.1
			self.board[chosen_tile[0]][chosen_tile[1]] = 4
			return True
		else:#P(2) = 0.9
			self.board[chosen_tile[0]][chosen_tile[1]] = 2
			return True
	#
	####--- Can make a move ---####
	def can_make_a_move(self):
		'''If a tile is empty or
		   a tile has an equal tile to merge with
		   then a move can be made
		'''
		for row in xrange(4):
			for col in xrange(4):
				if self.board[row][col] == 0: return True
				elif row-1 > -1:
					if self.board[row][col] == self.board[row-1][col]: return True
				elif row+1 < 4:
					if self.board[row][col] == self.board[row+1][col]: return True
				elif col-1 > -1:
					if self.board[row][col] == self.board[row][col-1]: return True
				elif col+1 < 4:
					if self.board[row][col] == self.board[row][col+1]: return True
		return False
	#
	def is_valid_move(self, direction):
		'''Checks whether the move changes the position of the board.
		   If it does not the move does not count as move
		'''
		board_pre_move = copy.deepcopy(state.get_board())
		temp_state = copy.deepcopy(self)
		temp_state.move(direction)
		for row in xrange(4):
			for col in xrange(4):
				if temp_state.get_tile(row, col) != board_pre_move[row][col]:
					return True
		return False
	#
	####--- Heuristic methods ---####
	def calculate_utility(self):
		'''Based on one or more algorithms the quality/closeness to target
		   is calculated
		'''
		total_tiles = 16
		total_empty_tiles = 0
		for row in self.board:
			for tile in row:
				if tile == 0:
					total_empty_tiles += 1
		print "total empty ", total_empty_tiles
		utility = (total_empty_tiles / total_tiles) * 100
		return utility
	#
	##-- Getters and setter --##
	def get_tile(self, row, column): return self.board[row][column]
	def set_tile(self, row, column, value): self.board[row][column] = value
	#
	def get_board(self): return self.board
	#
	def get_h(self): return self.h
	def get_highest_tile(self):
		highest_tile = 0
		for row in xrange(4):
			for col in xrange(4):
				if self.get_tile(row, col) > highest_tile:
					highest_tile = self.get_tile(row, col)
		return highest_tile
#
#
def do_moves(state):
	moves = [0, 1, 3, 2]
	while state.can_make_a_move():
		for direction in moves:
			if state.is_valid_move(direction):
				state.move(direction)
				break
		print state.calculate_utility()
		state.spawn()
	return state.get_highest_tile()



#

if __name__ == '__main__':
	n64_ = 0
	n128_ = 0
	n256_ = 0
	n512_ = 0
	n1024_ = 0
	n2048_ = 0
	board =[[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0]]
	n = 1000
	for iii in xrange(n):
		if iii%100 == 0: print "Kjoring nummer ", iii
		board =[[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0]]
		state = State(board)
		highest_tile = do_moves(state)


		if highest_tile == 64: n64_ += 1
		if highest_tile == 128: n128_ += 1
		elif highest_tile == 256: n256_ += 1
		elif highest_tile == 512: n512_ += 1
		elif highest_tile == 1024: n1024_ += 1
		elif highest_tile == 2048: n2048_ += 1

	#
	print n, " runs:"
	print "64: ", 100.0*float(n64_)/n, "%"
	print "128: ", 100.0*float(n128_)/n, "%"
	print "256: ", 100.0*float(n256_)/n, "%"
	print "512: ", 100.0*float(n512_)/n, "%"
	print "1024: ", 100.0*float(n1024_)/n, "%"
	print "2048: ", 100.0*float(n2048_)/n, "%"

'''Resultat:
64: 18.4%
128: 50.4%
256: 28.3%
512: 0.8%
1024: 0.0%
2048: 0.0%'''
