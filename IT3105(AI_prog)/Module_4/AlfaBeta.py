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
		#print "utility"
		return state.calculate_utility()
	if is_max:
		#print "is_max"
		alfas = []
		#print state.all_valid_moves()
		for move in state.all_valid_moves():
			#print "move", move
			alfas.append( ab_prun(new_state_move(state, move), depth-1, alfa, beta, False) )
			alfa = max(alfas)
			#print "alfa", alfa
			if beta <= alfa:
				break
		#print "return alfa"
		return alfa
	else:
		betas = []
		for spawn in state.all_spawns():
			#print "spawn", spawn
			betas.append( ab_prun(new_state_spawn(state, spawn), depth-1, alfa, beta, True) )
			beta = min(betas)
			if beta <= alfa:
				break
		#print "return beta"
		return beta
##
board = [[0,0,0,0],
		 [0,0,0,0],
		 [0,0,0,0],
		 [0,0,0,0]]
state = S.State(board)
state.spawn()
while state.can_make_a_move:
	print "new iteration"
	val = ab_prun(state, 3, -1, 101, True)

	for move in state.all_valid_moves():
		temp_state = copy.deepcopy(state)
		temp_state.move(move)
		print temp_state.calculate_utility(), "   ", val
		if temp_state.calculate_utility() == val:
			state.move(move)
			break
	state.spawn()


	
#alfas = []
#for move in state.all_valid_moves():
#	print move
#print terminal(state, True)
#new_state = new_state_spawn(state, [0,3,4])
#new_state = new_state_move(state, 0)
for r in state.get_board():
	print r