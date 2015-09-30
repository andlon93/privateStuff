import State
import Variable
import random
from collections import deque
###--- Dictionary methods(contains all states) ---###
def create_dictionary(l):#The key is the F-value of the states
	d = {}
	for n in xrange(l+1):
		d[n] = []
	return d
#
def add_states_to_dict(states, d):#add newly created states to the dict
	for state in states:
		try:
			d[state.get_h()].append(state)
		except:
			print "Algorithm failed - add_states_to_dict"
			return False
	return d
#
def get_best_state(all_states):#get one of the best states from the dict
	for i in all_states:
		if all_states[i]:
			return all_states[i][random.randint(0, len(all_states[i])-1)]
###--- method to generate child states ---###
def generate_child_states(state):
	pass
###--- GAC methods ---###
def create_GAC_queue(assumption):#Generates the queue of constraints to run
	queue = deque()
	pass
#
def update_cell(C):
	pass
#
def update_variable(C):
	pass
#
def revice(state, C):#changes a state based on a constraint
	if C[0][2] == -1:
		update_cell(state, C)
	else:
		update_variable(state, C)
#
def extend_queue():#extends the GAC_queue when needed
	pass
#
def Filter(state):#Iterates through the GAC_queue -> runs revice on them
	pass
###--- Methods to check validity of a state ---###
def is_valid_state(state):
	pass
#
def is_done(state):
	pass
###--- The main algorithm ---###
def Astar(start_state):
	print "Astar is running..."

	pass