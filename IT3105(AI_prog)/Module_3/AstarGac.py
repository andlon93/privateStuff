import State
import Variable
import random
from collections import deque
#
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
#
###--- method to generate child states ---###
def generate_child_states(state):
	pass
#
###--- GAC methods ---###
def create_GAC_queue(assumption):#Generates the queue of constraints to run
	queue = deque()
	pass
#
###--- Revice methods ---###
def possible_to_update(t):#Checks whether any of the cells van be updated
		for i in t:
			if i!=-1: return True
		return False
def update_cell(C):#updates the cell in Board if possible
	d=C[1].domain
	temp_list=[]*len(d[0])
	#
	for n in xrange(len(d[0])):#sets temp_list to the first list in domain
		temp_list[n]=d[0][n]
	##--if a cell can have two values, it cannot be set to a value--##
	for n in xrange(1, len(d)):
		for i in xrange(len(d[n])):
			if temp_list[i]!=d[n][i]: temp_list[i]=-1
		if not possible_to_update(temp_list): return [] #temp_list should be all -1's
	return temp_list
#
def update_state_cell_rows(state, new_list):#updates state board rows
	for n in xrange(len(new_list)):
		if state.board[C[1].get_index()][n]==-1:
			state.board[C[1].get_index()][n]=new_list[n]
def update_state_cell_cols(state, new_list):#updates state board columns
	for n in xrange(len(new_list)):
		if state.board[n][C[1].get_index()]==-1:
			state.board[n][C[1].get_index()]=new_list[n]
#
def update_variable_domain(C):#updates the domain based on a cell value
	d=C[1].domain
	for n in d:
		if n[index]!=C[0][1]:
			d.remove(n)
	return d
#
def revice(state, C):#changes a state based on a constraint
	domain_updated=False
	cells_updated=False
	if C[0][1]==-1: 
		new_list=update_cell(C)
		##--update cell rows or columns if needed--##
		if len(new_list)>0:
			if C[1].get_is_row():
				update_state_cell_rows(state, new_list)
			else:
				update_state_cell_cols(state, new_list)
			cells_updated=True
		##
	else: 
		old_domain_len=len(C[1].domain)
		new_domain=update_variable_domain(state, C)
		##--update domain if needed--##
		if old_domain_len>len(new_domain):
			if C[1].get_is_row():
				state.set_row(C[1].get_index(), new_domain)
			else:
				state.set_col(C[1].get_index(), new_domain)
			domain_updated=True
		##
	return new_list, new_domain
#
###--- Filter methods ---###
def extend_queue():#extends the GAC_queue when needed
	pass
#
def Filter(state):#Iterates through the GAC_queue -> runs revice on them
	pass
#
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