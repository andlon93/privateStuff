import copy
import State as S
import time
import Expectimax as EX
def terminal(state, is_max):
	'''sjekke om det kan "lages barn" av staten'''
	if is_max:#check if a move can be done
		if state.can_make_a_move():
			return False
		return True
	else:#check if a spawn can be done
		for r in xrange(4):
			for c in xrange(4):
				#if there is an empty tile then a spawn can be done
				if state.get_tile(r, c) == 0:
					return False
		return True
#
def new_state_move(parent, move):
	'''make new state based on a spawn'''
	new_board = copy.deepcopy(parent.get_board())#copy parents board
	new_state = S.State(new_board)#make new state from the copied board
	new_state.move(move)#make the move in the new state
	return new_state#return the new state
#
def new_state_spawn(parent, spawn):
	'''Make a new state with a spawn'''
	new_board = copy.deepcopy(parent.get_board())#copy parents board
	new_board[spawn[0]][spawn[1]] = spawn[2]
	return S.State(new_board)
#
def ab_prun(state, depth, alfa, beta, is_max, weights):
	#print "ab"
	if depth == 0 or terminal(state, is_max):
		#return EX.utility(state.get_board())
		return state.calculate_utility(weights)
	if is_max:
		v = -1
		for move in state.all_valid_moves():
			v = max(v, ab_prun(new_state_move(state, move), depth-1, alfa, beta, False, weights) )
			alfa = max(alfa, v)
			if beta <= alfa:
				break
		return v
	else:
		v = 101
		for spawn in state.all_spawns():
			v = min(v, ab_prun(new_state_spawn(state, spawn), depth-1, alfa, beta, True, weights) )
			beta = min(beta, v)
			if beta <= alfa:
				break
		return v
########################################################
#   0    1    2    3    4
P=[0.0, 0.0, 0.9, 0.0, 0.1]
def expectimax(state, depth, is_move):
	if depth == 0 or terminal(state, is_move):
		return state.calculate_utility()
	if is_move:
		alfa = -1000000
		for move in state.all_valid_moves():
			alfa = max( alfa, expectimax(new_state_move(state, move), depth-1, False) )
	else:
		alfa = 0
		for spawn in state.all_spawns():
			#print P[spawn[2]]
			#expectimax(new_state_spawn(state, spawn), depth-1, True)
			alfa +=  P[spawn[2]] * expectimax(new_state_spawn(state, spawn), depth-1, True)
	return alfa

########################################################
####-- run alfaBeta and make moves --####
def runAB(state, weights):
	#print "GO"
	#state = S.State(board)
	state.spawn()


	original_depth = 2
	#depth = copy.deepcopy(original_depth)
	moves = 0
	highest = 0
	while state.can_make_a_move():
		best_move = None
		best_val = -1
		depth = original_depth
		if state.get_highest_tile() == 512:
			depth = original_depth + 1
		if state.get_highest_tile() == 1024:
			depth = original_depth + 2
		if state.number_of_empty_tiles() < 5:
			depth = original_depth + 2
		if state.number_of_empty_tiles() < 4:
			depth = original_depth + 3
		if state.number_of_empty_tiles() < 3:
			depth = original_depth + 4
		if state.calculate_utility(weights) < 30:
			depth += 1

		for move in state.all_valid_moves():
			#print move

			temp_state = copy.deepcopy(state)
			temp_state.move(move)
			val = ab_prun(temp_state, depth, best_val, 1000000, False, weights)

			if val > best_val:
				best_val = val
				best_move = move
		state.move(best_move)
		moves += 1
		#if state.get_highest_tile() > highest:
		#	highest = state.get_highest_tile()
		#	print "Hoyeste:", highest, " Trekk:", moves

		state.spawn()
	#print "dybde: ", original_depth,
	return state
#

if __name__ == '__main__':
	weight = [0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1, 0.05]
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


	#state = runExmax(board)



	n = 50
	for x in xrange(n):
		print x
		board = [[0,0,0,0],
			 	[0,0,0,0],
			 	[0,0,0,0],
			 	[0,0,0,0]]
		state = S.State(board)
		state = runAB(state, weight)
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

		print "64: ", 100.0*float(n64)/(x+1), "%"
		print "128: ", 100.0*float(n128)/(x+1), "%"
		print "256: ", 100.0*float(n256)/(x+1), "%"
		print "512: ", 100.0*float(n512)/(x+1), "%"
		print "1024: ", 100.0*float(n1024)/(x+1), "%"
		print "2048: ", 100.0*float(n2048)/(x+1), "%"
		print "4096: ", 100.0*float(n4096)/(x+1), "%"
		print "8192: ", 100.0*float(n8192)/(x+1), "%"


	#
	print n, " runs:"
	print "64: ", 100.0*float(n64)/n, "%"
	print "128: ", 100.0*float(n128)/n, "%"
	print "256: ", 100.0*float(n256)/n, "%"
	print "512: ", 100.0*float(n512)/n, "%"
	print "1024: ", 100.0*float(n1024)/n, "%"
	print "2048: ", 100.0*float(n2048)/n, "%"
	print "4096: ", 100.0*float(n4096)/(x+1), "%"
	print "8192: ", 100.0*float(n8192)/(x+1), "%"
	print("--- %s seconds ---" % (time.time() - start_time))
	#print "Tar med val"
