import copy
import State as S
def terminal(state, is_max):
	'''sjekke om det kan "lages barn" av staten'''
	if is_max:#check if a move can be done
		return state.can_make_a_move()
	else:#check if a spawn can be done
		for r in xrange(4):
			for c in xrange(4):
				#if there is an empty tile then a spawn can be done
				if state.get_tile(r, c) == 0:
					return True
		return False
#
def new_state_move(state, move):
	'''Lage ny state basert på et move'''
	new_board = copy.deepcopy(state.get_board())#copy parents board
	new_state = S.State(new_board)#make new state from the copied board
	new_state.move(move)#make the move in the new state
	return new_state#return the new state
#
def new_state_spawn(state, spawn):
	'''Make a new state with a spawn'''
	new_board = copy.deepcopy(state.get_board())#copy parents board
	new_board[spawn[0]][spawn[1]] = spawn[2]
	return S.State(new_board)