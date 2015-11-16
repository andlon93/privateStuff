import AlfaBeta as AB
import time
import State
import copy
from multiprocessing import Process, Queue
import cProfile
#
'''
W = [
    [  [  10,    9,  7.6, 7.4],
	   [ 7.4,  6.4,  5.7, 5.3],
	   [ 4.5,  4.1,  2.7, 1.2],
	   [0.09, 0.07, 0.04, 0.02] ],

	[  [  10,    9,  7.6, 7.4],
	   [ 7.4,  6.4,  5.7, 5.3],
	   [ 4.5,  4.1,  2.7, 1.2],
	   [0.09, 0.07, 0.04, 0.02] ],

	[  [0.09, 0.07, 0.04, 0.02],
       [ 4.5,  4.1,  2.7, 1.2],
       [ 7.4,  6.4,  5.7, 5.3],
       [  10,    9,  7.6, 7.4] ],

	[  [ 7.4, 5.3, 1.2, 0.02],
       [  7.6,  5.7,  2.7, 0.04],
       [   9,  6.4,  4.1, 0.07],
       [  10,    7.4,  4.5, 0.09] ],

    [  [ 7.4,  7.6,    9,   10],
	   [ 5.3,  5.7,  6.4,  7.4],
       [ 1.2,  2.7,  4.1,  4.5],
       [0.02, 0.04, 0.07, 0.09] ],

    [  [ 0.09,  4.5,    7.4,   10],
	   [ 0.07,  4.1,  6.4,   9],
       [ 0.04,  2.7,  5.7,  7.6],
       [ 0.02, 1.2, 5.3, 7.4] ],

    [  [0.02, 0.04, 0.07, 0.09],
	   [ 1.2,  2.7,  4.1,  4.5],
	   [ 5.3,  5.7,  6.4,  7.4],
	   [ 7.4,  7.6,    9,   10] ],

    [  [0.02, 1.2, 5.3, 7.4],
	   [ 0.04,  2.7,  5.7,  7.6],
	   [ 0.07,  4.1,  6.4,  9],
	   [ 0.09,  4.5,    7.4,   10] ]   ]'''
W = [
    [  [  10,    9,  7.6, 7.4],
	   [ 7.4,  6.4,  5.7, 5.3],
	   [ 4.5,  4.1,  2.7, 1.2],
	   [0.09, 0.07, 0.04, 0.02] ],]

#
def utility(board):
	max_score = 0
	for W_matrix in W:
		temp = 0
		for r in range(4):
			for c in range(4):
				temp += W_matrix[r][c]*board[r][c]
		if temp > max_score:
			max_score = temp
	return max_score
##
#   0    1    2    3    4
P=[0.0, 0.0, 0.9, 0.0, 0.1]
def expectimax(state, depth):
	new_state_m =  AB.new_state_move
	new_state_s = AB.new_state_spawn
	tot_score = 0
	tot_prob = 0
	if depth == 0:# or AB.terminal2(state):
		return utility(state.get_board())
	else:
		for spawn in state.all_spawns():
			newS = new_state_s(state, spawn)
			best_score = 0
			best_move = None
			for move in state.all_valid_moves():
				score = expectimax(new_state_m(newS, move), depth-1)
				if score > best_score:
					best_score = score
					best_move = move
			if best_move != None:
				tot_score += P[spawn[2]] * best_score
			else:
				tot_score += P[spawn[2]] * utility(newS.get_board())
			tot_prob += P[spawn[2]]
	if tot_prob == 0:
		return tot_score
	return tot_score/tot_prob
#
def runExmax(board):
	deep_copy = copy.deepcopy
	state = State.State(board)
	#print state
	state.spawn()
	#
	moves = 0
	highest = 0
	while state.can_make_a_move():
		depth = 0
		best_move = None
		best_val = -1
		#
		if state.number_of_empty_tiles() < 2:
			depth = 2
		elif state.get_highest_tile() > 511:
			depth = 1
		#
		for move in state.all_valid_moves():
			temp_state = deep_copy(state)
			temp_state.move(move)
			#
			alfa = expectimax(temp_state, depth)
			if best_val < alfa:
				best_val = alfa
				best_move = move
				#
		if write_to_file:
			with open("2048training.txt", "a") as myfile:
				b = state.get_board()
				s = ""
				for line in b:
					for num in line:
						s+=str(num)
						s+=","
				s += str(best_move)
				s += "\n"
				myfile.write(s)


		state.move(best_move)
		moves += 1
		if state.get_highest_tile() > highest:
			highest = state.get_highest_tile()
			print ("hoyeste oppnaadd:", highest, " ", moves, "trekk")
		#if state.get_highest_tile() == 2048:
		#	return state
		state.spawn()
	return state
##
if __name__ == '__main__':
	write_to_file = False
	start_time = time.time()
	board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
	###--- To get statistics ---###
	n64 = 0
	n128 = 0
	n256 = 0
	n512 = 0
	n1024 = 0
	n2048 = 0
	n4096 = 0
	n8192 = 0
	nMore = 0
	#
	n = 200
	for x in range(1, n+1):
		print ("Kjoring nummer: ", x)
		board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
		#cProfile.run('runExmax(board)')
		state = runExmax(board)#expectimax
		highest_tile = state.get_highest_tile()
		#
		if highest_tile == 64: n64 += 1
		if highest_tile == 128: n128 += 1
		elif highest_tile == 256: n256 += 1
		elif highest_tile == 512: n512 += 1
		elif highest_tile == 1024: n1024 += 1
		elif highest_tile == 2048: n2048 += 1
		elif highest_tile == 4096: n4096 += 1
		elif highest_tile == 8192: n8192 += 1
		elif highest_tile > 8192: nMore += 1
		#
		'''
		print "Expectimax with weight matrix"
		print "64: ", 100.0*float(n64)/(x), "%"
		print "128: ", 100.0*float(n128)/(x), "%"
		print "256: ", 100.0*float(n256)/(x), "%"
		print "512: ", 100.0*float(n512)/(x), "%"
		print "1024: ", 100.0*float(n1024)/(x), "%"
		print "2048: ", 100.0*float(n2048)/(x), "%"
		print "4096: ", 100.0*float(n4096)/(x), "%"
		print "8192: ", 100.0*float(n8192)/(x), "%"
		print "More than 8192: ", 100.0*float(nMore)/x, "%"
		print("--- %s seconds ---" % (time.time() - start_time))
		print "\n"
		'''
