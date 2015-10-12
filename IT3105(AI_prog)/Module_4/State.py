import random
from collections import deque
#
class State:
	#
	board = []
	h = None
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
		chosen_tile = open_tiles[random.randint(0, len(open_tiles)-1)]#choose a random tile
		print chosen_tile
		if random.randint(0, 100) < 10:#P(4) = 0.1
			self.board[chosen_tile[0]][chosen_tile[1]] = 4
		else:#P(2) = 0.9
			self.board[chosen_tile[0]][chosen_tile[1]] = 2
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
					if board[row][col] == board[row-1][col]: return True
				elif row+1 < 4:
					if board[row][col] == board[row+1][col]: return True
				elif col-1 > -1:
					if board[row][col] == board[row][col-1]: return True
				elif col+1 < 4:
					if board[row][col] == board[row][col+1]: return True
		return False
	#
	####--- Heuristic methods ---####
	def calculate_heuristic(self):
		'''Based on one or more algorithms the quality/closeness to target
		   is calculated
		'''
		h = 0
		return h
	#
	##-- Getters and setter --##
	def get_tile(self, row, column): return self.board[row][column]
	def set_tile(self, row, column, value): self.board[row][column] = value
	#
	def get_board(self): return self.board
	#
	def get_h(self): return self.h
#
if __name__ == '__main__':
	board =[[4,2,4,2],
			[2,4,2,4],
			[4,2,4,2],
			[2,4,2,4]]
	s = State(board)
	for row in s.get_board():
		print row
	print '\n'
	print s.can_make_a_move()
	#for row in s.get_board():
	#	print row