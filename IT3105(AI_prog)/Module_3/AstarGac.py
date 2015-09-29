import State
import Variable
import random
from collections import deque
#
def create_dictionary(l):
	d = {}
	for n in xrange(l+1):
		d[n] = []
	return d
#
def add_states_to_dict(states, d):
	for state in states:
		try:
			d[state.get_h()].append(state)
		except:
			print "Algorithm failed - add_states_to_dict"
			return False
	return d
#
def generate_child_states(state):
	pass
#
def get_best_state(all_states):
	for i in all_states:
		if all_states[i]:
			return all_states[i][random.randint(0, len(all_states[i])-1)]
#
def create_GAC_queue(assumption):
	queue = deque()
	pass
# 
def revice():
	pass
#
def extend_queue():
	pass
#
def Filter(state):
	pass
#
def is_valid_state(state):
	pass
#
def is_done(state):
	pass
#
def Astar(start_state):
	print "Astar is running..."
	
	pass