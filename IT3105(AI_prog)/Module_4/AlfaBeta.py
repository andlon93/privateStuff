import copy
import State as S
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
def ab_prun(state, depth, alfa, beta, is_max):
	if depth == 0 or terminal(state, is_max):
		return state.calculate_utility()
	if is_max:
		v = -1
		for move in state.all_valid_moves():
			v = max(v, ab_prun(new_state_move(state, move), depth-1, alfa, beta, False) )
			alfa = max(alfa, v)
			if beta <= alfa:
				break
		return v
	else:
		v = 101
		for spawn in state.all_spawns():
			v = min(v, ab_prun(new_state_spawn(state, spawn), depth-1, alfa, beta, True) )
			beta = min(beta, v)
			if beta <= alfa:
				break
		return v
####-- run alfaBeta and make moves --####
def runAB(board):
	state = S.State(board)
	state.spawn()
	depth = 3
	while state.can_make_a_move():
		best_move = None
		best_val = -1
		if depth < 5 and state.get_highest_tile() == 512: 
			depth = 5
			print "depth = ", depth
		if state.number_of_empty_tiles() < 5:
			depth = 10
		else:
			if depth < 5 and state.get_highest_tile() == 512: 
				depth = 5
			else:
				depth = 3
		for move in state.all_valid_moves():
			temp_state = copy.deepcopy(state)
			temp_state.move(move)
			val = ab_prun(temp_state, depth, -1, 101, False)
			if val > best_val:
				best_val = val
				best_move = move
		state.move(best_move)
		state.spawn()
	return state
#
if __name__ == '__main__':
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

	n = 1
	for x in xrange(n):
		board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
		state = runAB(board)
		highest_tile = state.get_highest_tile()
		#
		print x
		if highest_tile == 64: n64 += 1
		if highest_tile == 128: n128 += 1
		elif highest_tile == 256: n256 += 1
		elif highest_tile == 512: n512 += 1
		elif highest_tile == 1024: n1024 += 1
		elif highest_tile == 2048: n2048 += 1
	#
	print highest_tile
	print n, " runs:"
	print "64: ", 100.0*float(n64)/n, "%"
	print "128: ", 100.0*float(n128)/n, "%"
	print "256: ", 100.0*float(n256)/n, "%"
	print "512: ", 100.0*float(n512)/n, "%"
	print "1024: ", 100.0*float(n1024)/n, "%"
	print "2048: ", 100.0*float(n2048)/n, "%"