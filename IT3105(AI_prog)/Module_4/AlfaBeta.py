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
	#print "depth", depth
	if depth == 0 or terminal(state, is_max):
		'''
		for r in state.board:
			print r
		print '\n'
		'''
		return state.calculate_utility()
	if is_max:
		#print "is_max"
		v = -1
		#print state.all_valid_moves()
		for move in state.all_valid_moves():
			#print "move", move
			v = max(v, ab_prun(new_state_move(state, move), depth-1, alfa, beta, False) )
			alfa = max(alfa, v)
			#print "alfa", alfa
			if beta <= alfa:
				break
		#print "return alfa"
		#for r in state.board:
		#	print r
		return v
	else:
		v = 101
		for spawn in state.all_spawns():
			#print "spawn", spawn
			v = min(v, ab_prun(new_state_spawn(state, spawn), depth-1, alfa, beta, True) )
			beta = min(beta, v)
			if beta <= alfa:
				break
		#print "return beta"
		#for r in state.board:
		#	print r
		return v
##
if __name__ == '__main__':
	board = [[0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]]
	state = S.State(board)
	state.spawn()
	for r in state.get_board():
		print r

	depth = 2
	while state.can_make_a_move():
		#for n in range(10):	
		print "new iteration"
		#val = ab_prun(state, 3, -1, 101, True)
		best_move = None
		best_val = -1
		all_vals = []
		'''if state.get_highest_tile() > 255:
			print "256 -- 256" 
			depth = 4
		elif state.get_highest_tile() > 511:
			print "512 -- 512"
			depth = 5'''
		for move in state.all_valid_moves():
			temp_state = copy.deepcopy(state)
			temp_state.move(move)
			#for r in temp_state.get_board():
			#	print r
			#print '\n\n\n'
			val = ab_prun(temp_state, depth, -1, 101, False)
			all_vals.append(val)
			if val > best_val:
				best_val = val
				best_move = move
			#break
		print all_vals
		print best_val, best_move
		if best_val == 0:
			for r in state.get_board():
				print r
			print '\n\n'
		state.move(best_move)
		#break
		state.spawn()
		if best_val == 0:
			for r in state.get_board():
				print r
			print "can_make_a_move ",state.can_make_a_move()
	
	
	#alfas = []
	#for move in state.all_valid_moves():
	#	print move
	#print terminal(state, True)
	#new_state = new_state_spawn(state, [0,3,4])
	#new_state = new_state_move(state, 0)
	for r in state.get_board():
			print r
