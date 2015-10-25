import AlfaBeta as AB
import time
import State
import copy
from multiprocessing import Process, Queue
#########################
'''W = [[[0.15759, 0.121925, 0.102812, 0.099937],
	   [0.0120, 0.0888405, 0.076711, 0.0724143],
	   [0.050654, 0.0462579, 0.027116, 0.0161889],
	   [0.0005498, 0.00002495, 0.00005871, 0.00005193]]]'''
'''W = [
    [  [100,  10,  1,   -1],
	   [ 10,   1,  -1,  -10],
	   [  1,   -1, -10, -100],
	   [  -1,  -10,-100,-1000] ],

	[  [-1,  -10,-100,-1000],
       [1,   -1, -10, -100],
       [10,   1,  -1,  -10],
       [100,  10,  1,   -1] ],

    [  [   -1,    1,  10,  100],
	   [  -10,    -1,   1,  10],
       [ -100,   -10,   -1,  1],
       [-1000,  -100,  -10,  -1] ],

    [  [-1000,  -100,   -10,    -1],
	   [ -100,   -10,    -1,    1],
	   [  -10,    -1,    1,   10],
	   [   -1,    1,   10,  100] ]   ]'''
W = [
    [ [0.135759, 0.121925, 0.102812, 0.099937],
	   [0.0997992, 0.0888405, 0.076711, 0.0724143],
	   [0.060654, 0.0562579, 0.037116, 0.0161889],
	   [0.0125498, 0.00992495, 0.00575871, 0.00335193] ],

	[ [0.0125498, 0.00992495, 0.00575871, 0.00335193],
       [0.060654, 0.0562579, 0.037116, 0.0161889],
       [0.0997992, 0.0888405, 0.076711, 0.0724143],
       [0.135759, 0.121925, 0.102812, 0.099937] ],

    [ [0.099937, 0.102812, 0.121925, 0.135759],
	   [0.0724143, 0.076711, 0.0888405, 0.0997992],
       [0.0161889, 0.037116, 0.0562579, 0.060654],
       [0.00335193, 0.00575871, 0.00992495, 0.0125498] ],

    [ [0.00335193, 0.00575871, 0.00992495, 0.0125498],
	   [0.0161889, 0.037116, 0.0562579, 0.060654],
	   [0.0724143, 0.076711, 0.0888405, 0.0997992],
	   [0.099937, 0.102812, 0.121925, 0.135759] ]   ]
#print W[0]
def utility(board):
	max_score = 0
	for W_matrix in W:
		temp = 0
		for r in xrange(4):
			for c in xrange(4):
				temp += W_matrix[r][c]*board[r][c]
		if temp > max_score:
			max_score = temp
	return max_score
#########################
#   0    1    2    3    4
P=[0.0, 0.0, 0.9, 0.0, 0.1]
def expectimax(state, depth, is_move):
	if depth == 0 or AB.terminal(state, is_move):
		return utility(state.get_board())
	if is_move:
		alfa = -1000000
		for move in state.all_valid_moves():
			alfa = max( alfa, expectimax(AB.new_state_move(state, move), depth-1, False) )
	else:
		alfa = 0
		for spawn in state.all_spawns():
			alfa +=  P[spawn[2]] * expectimax(AB.new_state_spawn(state, spawn), depth-1, True)
	return alfa
##
#P=[0.9, 0.1]
#S=[2, 4]
def expectimax2(state, depth):
	tot_score = 0
	tot_prob = 0
	if depth == 0 or AB.terminal(state, True):
		return utility(state.get_board())
	else:
		#for r in xrange(4):
		#	for c in xrange(4):
		#		if state.get_tile(r, c) == 0:
		#			for n in xrange(2):
		for spawn in state.all_spawns():
			#newS = AB.new_state_spawn(state, [r, c, S[n]])
			newS = AB.new_state_spawn(state, spawn)
			best_score = 0
			best_move = None
			for move in state.all_valid_moves():
				newState = AB.new_state_move(newS, move)
				score = expectimax2(newState, depth-1)
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

def runExmax(board):
	print "pp"
	state = State.State(board)
	#print state
	state.spawn()
	#
	moves = 0
	highest = 0
	while state.can_make_a_move():
		depth = 1
		best_move = None
		best_val = -1
		#
		if depth < 3 and state.number_of_empty_tiles() < 2:
			depth = 3
		elif depth < 2 and state.get_highest_tile() > 511:
			depth = 2

		for move in state.all_valid_moves():
			temp_state = copy.deepcopy(state)
			temp_state.move(move)
			#
			alfa = expectimax2(temp_state, depth)
			if best_val < alfa:
				best_val = alfa
				best_move = move
		#
		state.move(best_move)
		moves += 1
		if state.get_highest_tile() > highest:
			highest = state.get_highest_tile()
			print "hoyeste oppnaadd:", highest, " ", moves, "trekk"
		if state.get_highest_tile() == 2048:
			return state
			#print "hoyeste oppnaadd:", highest, " ", moves, "trekk"
		state.spawn()
	return state
##
if __name__ == '__main__':

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

	n = 200
	for x in xrange(1, n+1):
		print "Kjoring nummer: ", x
		print "Dybde: 3"
		board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
		#state = State.State(board)
		#print state
		state = runExmax(board)#runAB(board)
		#print state.highest_tile()
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

	#
	print n, " runs:"
	print "64: ", 100.0*float(n64)/n, "%"
	print "128: ", 100.0*float(n128)/n, "%"
	print "256: ", 100.0*float(n256)/n, "%"
	print "512: ", 100.0*float(n512)/n, "%"
	print "1024: ", 100.0*float(n1024)/n, "%"
	print "2048: ", 100.0*float(n2048)/n, "%"
	print "4096: ", 100.0*float(n4096)/(n), "%"
	print "8192: ", 100.0*float(n8192)/(n), "%"
	print("--- %s seconds ---" % (time.time() - start_time))