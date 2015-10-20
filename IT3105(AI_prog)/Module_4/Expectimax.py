import AlfaBeta as AB
import time
import State as S
import copy
#########################
'''W = [[[0.15759, 0.121925, 0.102812, 0.099937],
	   [0.0120, 0.0888405, 0.076711, 0.0724143],
	   [0.050654, 0.0462579, 0.027116, 0.0161889],
	   [0.0005498, 0.00002495, 0.00005871, 0.00005193]]]'''
W = [
    [  [1000,  700,  500,  300],
	   [25,    50,  75,   100],
	   [ 12,    7,   5,   5],
	   [  0,     0,   1,   2] ]]#,
'''
	[  [  7,     5,   1,   0],
       [ 20,    10,   5,   1],
       [100,    30,  15,   7],
       [1000,  200,  50,  15] ],

    [  [15, 50, 200, 1000],
	   [ 7, 15,  30,  100],
       [ 1,  5,  10,   20],
       [ 0,  1,   2,    3] ],

    [  [ 0,  1,   2,    3],
	   [ 1,  5,  10,   20],
	   [ 7, 15,  30,  100],
	   [15, 50, 200, 1000] ]   ]'''
'''W = [
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
	   [0.099937, 0.102812, 0.121925, 0.135759] ]   ]'''
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
		#return state.calculate_utility()
		return utility(state.get_board())
	if is_move:
		alfa = -1000000
		for move in state.all_valid_moves():
			alfa = max( alfa, expectimax(AB.new_state_move(state, move), depth-1, False) )
	else:
		alfa = 0
		for spawn in state.all_spawns():
			#print P[spawn[2]]
			#expectimax(new_state_spawn(state, spawn), depth-1, True)
			alfa +=  P[spawn[2]] * expectimax(AB.new_state_spawn(state, spawn), depth-1, True)
	return alfa
##
def runExmax(board):
	state = S.State(board)
	state.spawn()
	#

	moves = 0
	highest = 0
	while state.can_make_a_move():
		depth = 4
		best_move = None
		best_val = -1
		#
		#if state.get_highest_tile() > 1023 and state.number_of_empty_tiles() < 3:
		#	depth = 6
		#		print depth

		for move in state.all_valid_moves():
			temp_state = copy.deepcopy(state)
			temp_state.move(move)
			#
			alfa = expectimax(temp_state, depth-1, False)

			#
			if best_val < alfa:
				best_val = alfa
				best_move = move
		#
		state.move(best_move)
		moves += 1
		if state.get_highest_tile() > highest:
			highest = state.get_highest_tile()
			print "hoyeste oppnaadd:", highest, " ", moves, "trekk"
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

	n = 100
	for x in xrange(1, n+1):
		print "Kjoring nummer: ", x
		board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
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