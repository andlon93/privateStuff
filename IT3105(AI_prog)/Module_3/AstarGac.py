import State
import Variable
import readfile as rf
import random
import time
import copy
from collections import deque
from multiprocessing import Process, Queue
#
###--- Dictionary methods(contains all states) ---###
#
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
		if len(all_states[i]) > 0:
			return all_states[i][random.randint(0, len(all_states[i])-1)]
#
###--- methods to generate child states ---###
#
def create_state(state, assumption):
	new_state=State.State(copy.deepcopy(state.get_rows()), copy.deepcopy(state.get_cols()), state))
	
	new_state.set_assumption(assumption)
	return new_state
#
def generate_child_states(state):
	children = []
	rows = state.get_rows()
	cols = state.get_cols()
	row_list = []
	col_list = []
	for row in rows:
		if len(row.get_domain()) < 2:
			row_list[row.get_index()] = -1
		else:
			row_list[row.get_index()] = len(row.get_domain())
	for col in cols:
		if len(col.get_domain()) < 2:
			col_list[col.get_index()] = -1
		else:
			col_list[col.get_index()] = len(col.get_domain())
	#
	best_row_variable = 0#index
	for n in xrange(1, row_list):
		if row_list[best_row_variable] > row_list[n]:
			best_row_variable = n
	best_col_variable = 0#index
	for n in xrange(1, col_list):
		if col_list[best_col_variable] > col_list[n]:
			best_col_variable = n
	#
	if row_list[best_row_variable] < col_list[best_col_variable]:
		for domain in rows[best_row_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			rows[best_row_variable].domain = domain
			children.append( State.State(rows, cols, state) )
	else:
		for domain in cols[best_col_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			cols[best_col_variable].domain = domain
			children.append( State.State(rows, cols, state) )

#
###--- GAC methods ---###
#
def create_GAC_queue(state, assumption):#Generates the queue of constraints to run
	
#
###--- Revice methods ---###
#

def Filter(state, queue):#Iterates through the GAC_queue -> runs revice on them

#
###--- Methods to check validity of a state ---###
def is_valid_state(state):
	for row in xrange(len(state.get_board())):
		for col in xrange(len(state.get_board()[row])):
			rute = state.get_board_cell(row, col)
			#if rute == -1:
			#	return False
			is_possible = False
			for d in state.get_row(row).get_domain():
				if rute == d[col] or rute == -1:
					is_possible = True
			if not is_possible: return False
			is_possible = False
			for d in state.get_col(col).get_domain():
				is_possible = False
				if rute == d[row] or rute == -1:
					is_possible = True
			if not is_possible: return False
	return True
#
def is_done(state):
	for row in xrange(len(state.get_board())):
		for col in xrange(len(state.get_board()[row])):
			rute = state.get_board_cell(row, col)
			if rute == -1:
				return False
			for d in state.get_row(row).get_domain():
				is_possible = False
				if rute == d[col]:
					is_possible = True
			if not is_possible: return False
			for d in state.get_col(col).get_domain():
				is_possible = False
				if rute == d[row]:
					is_possible = True
			if not is_possible: return False
	return True
#
#
###--- Astar ---###
def Astar(start_state):
	#import gui
	print "Astar is running..."
	all_states = create_dictionary(start_state.get_h())
	#all_states[start_state.get_h()].append(start_state)
	#
	children = generate_child_states(start_state)

	'''gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(c.get_board()))
	gui.app.processEvents()
	print "GUI processing from astar"
	time.sleep(0.5)'''



if __name__ == '__main__':
	b = Astar(rf.read_graph("nono-heart.txt"))
