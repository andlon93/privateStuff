#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
			d[state.get_h()+state.get_g()].append(state)
		except:
			print "Algorithm failed - add_states_to_dict"
			return False
	return d
#
def get_best_state(all_states):#get one of the best states from the dict
	for i in all_states:
		#print all_states[i]
		if len(all_states[i]) > 0:
			return all_states[i][random.randint(0, len(all_states[i])-1)]
#
###--- methods to generate child states ---###
#
'''def create_state(state, assumption):
	new_state=State.State(copy.deepcopy(state.get_rows()), copy.deepcopy(state.get_cols()), state))

	new_state.set_assumption(assumption)
	return new_state'''
#
def generate_child_states(state):
	children = []
	rows = state.get_rows()
	cols = state.get_cols()
	row_list = [-1]*len(rows)
	col_list = [-1]*len(cols)
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
	print row_list,'\n',col_list
	#
	best_row_variable = 0#index
	for n in xrange(1, len(row_list)):
		if row_list[best_row_variable] > row_list[n] and row_list[n] > 0:
			best_row_variable = n
	best_col_variable = 0#index
	for n in xrange(1, len(col_list)):
		if col_list[best_col_variable] > col_list[n]:
			best_col_variable = n
	#
	print best_row_variable, best_col_variable
	if row_list[best_row_variable] <= col_list[best_col_variable]:
		for domain in rows[best_row_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			rows[best_row_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_row(best_row_variable), children[-1].get_row(best_row_variable).get_domain()] )
			print "is_row on new child: ", children[-1].get_assumption()[0].get_is_row()
	else:
		for domain in cols[best_col_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			cols[best_col_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_col(best_col_variable), children[-1].get_col(best_col_variable).get_domain()] )
			print "is_row on new child: ", children[-1].get_assumption()
	#print len(children)
	return children

#
###--- GAC methods ---###
#

def create_GAC_queue(state):#Generates the queue of constraints to run
	queue = deque()
	assumption = state.get_assumption()[0]
	if assumption.get_is_row():
		for n in state.get_cols():
			queue.append( [assumption, n] )
	else:
		for n in state.get_rows():
			queue.append( [assumption, n] )
	return queue
#
###--- Revice methods ---###
def revice(C, state):
	#is_valid = True
	if C[0].get_is_row():
		d_0 = state.get_row(C[0].get_index()).get_domain()

	else:
		d_0 = state.get_col(C[0].get_index()).get_domain()


	is_row_C1 = C[1].get_is_row()
	if is_row_C1:
		d_1 = state.get_row(C[1].get_index()).get_domain()
	else:
		d_1 = state.get_col(C[1].get_index()).get_domain()

	

	if len(d_0) == 0 or len(d_1) == 0 :
		return len(d_1)
	index_d0 = C[0].get_index()
	index_d1 = C[1].get_index()
	print "index_d0", index_d0, "index_d1", index_d1
	#print d_0[0][index_d1]
	#
	#print d_0
	##
	#print len(d_0), d_0, '\n'
	#for d in d_1:
	#	print d
	##
	new_domain = []
	print "d0[0][index_d1]: ",d_0[0][index_d1]
	if len(d_0) == 1:
		for n in xrange(len(d_1)):
			print n, ": ",	d_1[n]
			print d_0[0][index_d1], d_1[n][index_d0]
			#print index, len(d_0[0]), len(d_1[n])
			if d_0[0][index_d1] == d_1[n][index_d0]:
				new_domain.append(d_1[n])
				'''if is_row_C1:
					state.get_row(C[1].get_index()).get_domain().remove(d_1[n])
				else:
					state.get_col(C[1].get_index()).get_domain().remove(d_1[n])'''
		#print new_domain
		#print len(new_domain)
		if is_row_C1:
			state.get_row(C[1].get_index()).domain = copy.deepcopy(new_domain)
			print state.get_row(C[1].get_index()).get_domain()
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			state.get_col(C[1].get_index()).domain = copy.deepcopy(new_domain)
			print state.get_col(C[1].get_index()).get_domain()
			return len(state.get_col(C[1].get_index()).get_domain())
	else:
		#print d_0
		#print "index", index
		is_possible = True
		#print temp_val
		#print is_possible
		for n in xrange(1, len(d_0)):
			if d_0[n][index_d1] != d_0[0][index_d1]:
				#print "test"
				is_possible = False
		#print temp_val
		#print is_possible

		if is_possible:
			for n in xrange(len(d_1)):
				if d_0[0][index_d1] == d_1[n][index_d0]:
					new_domain.append(d_1[0])
					'''if is_row_C1:
						state.get_row(C[1].get_index()).get_domain().remove(d_1[n])
					else:
						state.get_col(C[1].get_index()).get_domain().remove(d_1[n])'''

		#print "len", len(new_domain)
		if is_row_C1:
			state.get_row(C[1].get_index()).domain = copy.deepcopy(new_domain)
			print state.get_row(C[1].get_index()).domain
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			state.get_col(C[1].get_index()).domain = copy.deepcopy(new_domain)
			print state.get_col(C[1].get_index()).domain
			return len(state.get_col(C[1].get_index()).get_domain())
#
###--- Revice methods ---###
#
def extend_queue(state, var):
	queue = deque()
	if var.get_is_row():
		for col in state.get_cols():
			temp = [var,col]
			queue.append(temp)
	else:
		for row in state.get_rows():
			temp = [var,row]
			queue.append(temp)
	return queue

def Filter(state, queue):#Iterates through the GAC_queue -> runs revice on them
	while queue:
		#print "koLengde ",len(queue)
		#time.sleep(0.2)
		q                  = queue.popleft()   	  #popper constraint fra ko
		length_pre_revise  = len(q[1].domain)
		length_post_revice = revice(q,state)			  #kjorer revice paa constrainten som ble poppet
		#
		#
		if length_pre_revise > length_post_revice:  #hvis domenet har blitt forkortet maa nye constarints inn i ko
			if q[1].get_is_row():
				queue.extend( extend_queue(state, state.get_row(q[1].get_index())))
			else:
				queue.extend( extend_queue(state, state.get_col(q[1].get_index())))
#
###--- Methods to check validity of a state ---###
#
def is_in_closed(closed, state):
	if not closed[state.get_h()]:
		return False
	for n in closed[state.get_h()]:
		for row in xrange(len(n.get_rows())):
			if n.get_row(row).get_domain() != state.get_row(row).get_domain():
				return False
		for col in xrange(len(n.get_cols())):
			if n.get_col(col).get_domain() != state.get_col(col).get_domain():
				return False
	return True
#
def is_done(state):
	if len(state.rows) < len(state.cols):
		for row in state.rows:
			if len(row.domain) != 1:
				return False
		for col in state.cols:
			if len(col.domain) != 1:
				return False
		return True
	else:
		for col in state.cols:
			if len(col.domain) != 1:
				return False
		for row in state.rows:
			if len(row.domain) != 1:
				return False
		return True
#
###--- Astar ---###
def Astar(start_state):
	print "Astar is running..."
	closed = create_dictionary(start_state.get_h())
	##
	all_states = create_dictionary(start_state.get_h())
	current_state = start_state
	children = generate_child_states(current_state)
	#
	while True:
		if children:
			valid_children = []
			#print children
			for child in children:
				if not is_in_closed(closed, child):
					#current_state.set_assumption((current_state.rows[0],current_state.rows[0].domain[0]))
					current_state = child
					queue = create_GAC_queue(current_state)
					# for col in current_state.cols:
					# 	print len(col.domain)
					# print "\n"
					# for row in current_state.rows:
					# 	print len(row.domain)
					Filter(current_state,queue)
					if is_valid_state(child):
						child.set_h(child.calculate_h())
						valid_children.append(child)
						##-- check if if child is a solution --##
						if is_done(child):
							print "ER I MAAL!!!"
							print "Antall steg til maal: ", child.get_g()
							for row in child.get_rows():
								print row.get_domain()[0]
							for col in child.get_cols():
								print col.get_domain()[0]
						##
						
					# print "\n\nafter filter"
					# for col in current_state.cols:
					# 	print len(col.domain)
					# print "\n"
					# for row in current_state.rows:
					# 	print len(row.domain)

					print "\n"
			print "valid_children",valid_children

			all_states = add_states_to_dict(valid_children, all_states)
			#for s in all_states:
			#	print all_states[state]
			current_state = get_best_state(all_states)
			print "current_state", 	current_state
			children = generate_child_states(current_state)
			#
			all_states[current_state.get_h()+current_state.get_g()].remove(current_state)
			closed[current_state.get_h()].append(current_state)
			#
			if is_done(current_state):
				print "FERDIG"
		else:
			current_state = get_best_state(all_states)
			children = generate_child_states(current_state)
			all_states[current_state.get_h()+current_state.get_g()].remove(current_state)
			closed[current_state.get_h()].append(current_state)

		print "\n"


	#print len(children)
	# for child in children:
	# 	queue = create_GAC_queue(child)
	# 	for q in queue:
	# 		revice(q, child)
	# 		break
	# 	break
	'''gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(c.get_board()))
	gui.app.processEvents()
	print "GUI processing from astar"
	time.sleep(0.5)'''

if __name__ == '__main__':
	Astar(rf.read_graph("nono-heart.txt"))