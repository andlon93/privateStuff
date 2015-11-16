from __future__ import division
import random
from collections import deque
import copy
import math
#
class State:
	#
	board = []
	utility = None
	weights = []
	#
	def __init__(self, board):
		self.board = board
	####--- Move methods ---####
	def move_up(self, col):
		rute_ledig = deque()#legger inn tomme ruter i en ko
		for row in range(4):
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
		for row in range(3, -1, -1):
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
		for col in range(3, -1, -1):
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
		for col in range(4):
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
		   1 = left
		   2 = right
		   3 = down
		   direction == 0 has code explanation. almost identical for every move
		'''
		if direction == 0:#hvis move er up
			for col in range(4):#iterer over brett kolonne for kolonne
				self.move_up(col)#Move tiles up
				##-- Merge start --##
				rute_ledig = deque()
				for row in range(3):
					if self.board[row][col] == self.board[row+1][col]:#merge ruter om de er like
						self.board[row][col] = self.board[row][col] * 2#sett overste til dobbel verdi
						self.board[row+1][col] = 0#sett den under til 0
				##-- Merge end --##
				self.move_up(col)#move tiles up again
		elif direction == 3:#hvis move er down
			for col in range(3, -1, -1):
				self.move_down(col)
				##-- Merge start --##
				rute_ledig = deque()
				for row in range(3, 0, -1):
					if self.board[row][col] == self.board[row-1][col]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row-1][col] = 0
				##-- Merge end --##
				self.move_down(col)
		elif direction == 2:#hvis move er right
			for row in range(4):
				self.move_right(row)
				##-- Merge start --##
				rute_ledig = deque()
				for col in range(3, 0, -1):
					if self.board[row][col] == self.board[row][col-1]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row][col-1] = 0
				##-- Merge end --##
				self.move_right(row)
		elif direction == 1:#move left
			for row in range(4):
				self.move_left(row)
				##-- Merge start --##
				rute_ledig = deque()
				for col in range(3):
					if self.board[row][col] == self.board[row][col+1]:
						self.board[row][col] = self.board[row][col] * 2
						self.board[row][col+1] = 0
				##-- Merge end --##
				self.move_left(row)
		else:
			print ("wrong direction input given")
	#
	####--- Spawn a 2 or 4 ---####
	def spawn(self):
		'''A new 2 or 4 tile spawns on the board.
		   P(2) = 0.9  --  P(4) = 0.1
		   Same prob for every open tile on the board
		'''
		open_tiles = []#list of all tiles with a zero in it
		for row in range(4):#iterate over the board
			for col in range(4):
				#if tile is zero, a spawn may happen in it
				if self.board[row][col] == 0: open_tiles.append([row, col])
		#
		if open_tiles:
			chosen_tile = open_tiles[int(round(random.uniform(0, len(open_tiles)-1)))]#choose a random tile
		else:
			#print ("ingen steder aa spawne en tile")
			return False
		if random.uniform(0, 100) < 10.0:#P(4) = 0.1
			self.board[chosen_tile[0]][chosen_tile[1]] = 4
			return True
		else:#P(2) = 0.9
			self.board[chosen_tile[0]][chosen_tile[1]] = 2
			return True
	####--- valid and find all moves and spawns methods ---####
	def can_make_a_move(self):
		'''If a tile is empty or
		   a tile has an equal tile to merge with
		   then a move can be made
		'''
		for row in range(4):
			for col in range(4):
				if self.board[row][col] == 0:
					return True
				if row > 0:
					if self.board[row][col] == self.board[row-1][col]: return True
				if row < 3:
					if self.board[row][col] == self.board[row+1][col]: return True
				if col > 0:
					if self.board[row][col] == self.board[row][col-1]: return True
				if col < 3:
					if self.board[row][col] == self.board[row][col+1]: return True
		return False
	#
	def is_valid_move(self, direction):
		'''Checks whether the move changes the position of the board.
		   If it does not the move does not count as move
		'''
		board_pre_move = copy.deepcopy(self.get_board())
		temp_state = copy.deepcopy(self)
		temp_state.move(direction)
		for row in range(4):
			for col in range(4):
				if temp_state.get_tile(row, col) != board_pre_move[row][col]:
					return True
		return False
	#
	def all_valid_moves(self):
		valid_moves = []
		for move in range(4):
			if self.is_valid_move(move): valid_moves.append(move)
		return valid_moves
	#
	def all_spawns(self):
		all_spawns = []
		for r in range(4):
			for c in range(4):
				if self.board[r][c] == 0:
					all_spawns.append([r, c, 2])
					all_spawns.append([r, c, 4])
		return all_spawns
	#
	####--- Utility methods ---####
	def calculate_utility(self, weights):
		'''Based on one or more algorithms the quality/closeness to target
		   is calculated'''
		free_tiles_utility = self.free_tiles_utility() * weights[0]# * 0.5
		highest_tile_utility = self.highest_tile_utility() * weights[1]#* 0.05
		largest_tile_corner_util = self.largest_tile_corner_util() * weights[2] #* 0.05
		cluster_score = self.cluster_score() *  weights[3]#* 0.05
		twos_fours = self.number_of_2s4s() * weights[4] #* 0.05
		number_of_same = self.number_of_same() * weights[5] #* 0.05
		brute_method = self.brute_method() * weights[6]#* 0.15
		upper_vs_lower = self.sum_greater_upper() * weights[7]#* 0.1
		first_over_second = self.first_over_second() * weights[8]
		first_column_filled = self.first_column_filled() * weights[9]
		#
		h=max(first_column_filled, first_over_second, upper_vs_lower, brute_method, free_tiles_utility, highest_tile_utility, largest_tile_corner_util, cluster_score, number_of_same, twos_fours)
		return first_column_filled/h, first_over_second/h, upper_vs_lower/h, brute_method/h, free_tiles_utility/h, highest_tile_utility/h, largest_tile_corner_util/h, cluster_score/h, number_of_same/h, twos_fours/h
		#sum_utilities = ( first_over_second + upper_vs_lower + brute_method + free_tiles_utility + highest_tile_utility + largest_tile_corner_util + cluster_score + number_of_same + twos_fours )
		#return sum_utilities
	#
	def first_over_second(self):
		board = self.board
		summ = 0
		for col in range(len(board[0])):
			if board[0][col] == 0:
				continue
			if board[0][col] >= board[1][col]:
				summ += 25
		return summ
	#
	def first_column_filled(self):
		board = self.board
		summ = 0
		for row in board:
			if row[0] == 0:
				continue
			else:
				summ += 8
		for col in board[0]:
			if col == 0:
				continue
			else:
				summ += 17
		return summ
	#
	def sum_greater_upper(self):
		board = self.board
		upper_sum = 0
		for tile in board[0]:
			upper_sum += tile
		lower_sum = 0
		for row in range(len(board)):
			if row == 0:
				continue
			for tile in board[row]:
				lower_sum += tile
		if lower_sum == 0:
			lower_sum = 1
		ratio = upper_sum / lower_sum
		if ratio > 3:
			return 100
		if ratio > 2:
			return 75
		if ratio > 1:
			return 30
		if ratio < 0.01:
			return 5
		if ratio < 0.1:
			return 10
		else:
			return 0
		return ratio
	#
	def brute_line2(self):
		board = self.board
		if board[1][3] >= board[1][2] and board[1][2] >= board[1][1] and board[1][1] >= board [1][0]:
			return 100
		if board[1][3] >= board[1][2] and board[1][2] >= board[1][1]:
			return 75
		if board[1][2] >= board[1][1] and board[1][1] >= board[1][0]:
			return 65
		if board[1][3] >= board[1][2]:
			return 50
		if board[1][2] >= board[1][1]:
			return 40
		return 0
	#
	def brute_method(self):
		board = self.board
		if board[0][0] >= board[0][1] and board[0][1] >= board[0][2] and board[0][2] >= board[0][3]:
			return 100
		if board[0][0] >= board[0][1] and board[0][1] >= board[0][2]:
			return 75
		if board[0][1] >= board[0][2] and board[0][2] >= board[0][3]:
			return 65
		if board[0][0] >= board[0][1]:
			return 50
		if board[0][1] >= board[0][2]:
			return 40
		else:
			return 0
	#
	def number_of_same(self):
		number = [0] * 11
		for row in self.board:
			for tile in row:
				if tile == 2:
					number[0] += 1
				if tile == 4:
					number[1] += 1
				if tile == 8:
					number[2] += 1
				if tile == 16:
					number[3] += 1
				if tile == 32:
					number[4] += 1
				if tile == 64:
					number[5] += 1
				if tile == 128:
					number[6] += 1
				if tile == 256:
					number[7] += 1
				if tile == 512:
					number[8] += 1
				if tile == 1024:
					number[9] += 1
				if tile == 2048:
					number[10] += 1
		score = 0
		for num in number:
			if num > 1:
				score += num -1
		score = score * 10
		if score > 100:
			score = 100
		return 100 - score
	#
	def number_of_2s4s(self):
		twos = 0
		fours = 0
		score = 0
		for row in self.board:
			for tile in row:
				if tile == 2:
					twos += 1
				elif tile == 4:
					fours += 1
		score = twos
		score = score + fours
		return (100 - (score*10))
	#
	def number_of_similar_tiles(self): #NOT DONE
		for row in self.board:
			for tile in row:
				return False
	#
	def number_of_empty_tiles(self):
		total_empty_tiles = 0
		for row in self.board:
			for tile in row:
				if tile == 0:
					total_empty_tiles += 1
		return total_empty_tiles
	#
	def free_tiles_utility(self):
		total_tiles = 16.0
		total_empty_tiles = self.number_of_empty_tiles()
		utility = (total_empty_tiles / total_tiles) * 100.0
		return utility
	#
	def highest_tile_utility(self):
		return float(self.get_highest_tile())**2 * 0.000023841
	#
	def largest_tile_corner_util(self):
		highest_tile = self.get_highest_tile()
		util = 0
		for r in range (len(self.board)):
			for c in range (len(self.board[0])):
				if self.board[r][c]==highest_tile:
					if (r == 0 and c == 0):
						util = 100
					elif (r==0 and c == 3 or r == 3 and c == 0):
						util = 50
		return util
	#
	def cluster_score(self):
		cluster_score = 0
		neighbours = [-1,0,1]
		board = self.board
		for i in range (len(board)):
			for j in range (len(board[0])):
				if board[i][j] == 0:
					continue
				num_neighbors = 0
				temp_sum = 0
				for k in neighbours:
					x = i+k
					if x<0 or x >= len(board):
						continue
					for l in neighbours:
						y = j + l
						if y<0 or y >= len(board):
							continue
						if board[i][j]>0:
							num_neighbors += 1
							temp_sum += abs(board[i][j]-board[x][y])
				cluster_score += abs(temp_sum) / num_neighbors
		cluster_score = cluster_score / 40
		cluster_score = 100 - cluster_score
		if cluster_score < 0:
			return 0
		elif cluster_score > 100:
			return 100
		else:
			return cluster_score
	##-- Getters and setter --##
	def get_tile(self, row, column): return self.board[row][column]
	def set_tile(self, row, column, value): self.board[row][column] = value
	#
	def get_board(self): return self.board
	#
	def get_h(self): return self.h
	def get_highest_tile(self):
		highest_tile = 0
		for row in range(4):
			for col in range(4):
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
		state.calculate_utility()

		state.spawn()
	return state.get_highest_tile()
#
#
if __name__ == '__main__':
	board =[[2,4,2,4],
			[4,2,4,8],
			[16,8,16,2],
			[2,4,8,0]]
	s = State(board)
	l = s.all_valid_moves()
	print (len(l))
	'''n64_ = 0
	n128_ = 0
	n256_ = 0
	n512_ = 0
	n1024_ = 0
	n2048_ = 0
	board =[[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0],
			[0,0,0,0]]
	n = 500
	for iii in range(n):
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
	print "2048: ", 100.0*float(n2048_)/n, "%"'''
'''Resultat:
64: 18.4%
128: 50.4%
256: 28.3%
512: 0.8%
1024: 0.0%
2048: 0.0%'''