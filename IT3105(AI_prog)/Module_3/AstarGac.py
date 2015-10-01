import State
import Variable
import readfile as rf
import random
import copy
from collections import deque
from multiprocessing import Process, Queue
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
###--- methods to generate child states ---###
def create_state(state, assumption):
	new_state=State.State(copy.deepcopy(state.get_rows()), copy.deepcopy(state.get_cols()), state)
	new_state.set_board_cell(assumption[0], assumption[1], assumption[2])
	new_state.set_assumption(assumption)
	return new_state
#
def generate_child_states(state):
	b = state.get_board()
	states=[]
	for row in xrange(len(b)):#finner en rute som ikke er satt.
		for col in xrange(len(b[row])):
			if b[row][col] == -1:#Lager et barn per mulighet for ruta
				states.append( create_state(state, [row, col, 1]) )
				states.append( create_state(state, [row, col, 0]) )
				return states
#
###--- GAC methods ---###
def create_GAC_queue(state, assumption):#Generates the queue of constraints to run
	queue = deque()
	queue.append([[assumption[0], assumption[2]], state.get_row(assumption[0])])
	queue.append([[assumption[1], assumption[2]], state.get_col(assumption[1])])
	return queue
#
###--- Revice methods ---###
def possible_to_update(t):#Checks whether any of the cells van be updated
		for i in t:
			if i!=-1: return True
		return False
def update_cell(C):#updates the cell in Board if possible
	d=C[1].get_domain()
	temp_list=[None]*len(d[0])
	#
	for n in xrange(len(d[0])):#sets temp_list to the first list in domain
		temp_list[n]=int(d[0][n])
	print "temp_list:  ", temp_list
	##--if a cell can have two values, it cannot be set to a value--##
	for n in xrange(1, len(d)):
		for i in xrange(len(d[n])):
			print "I:",i
			print "hvis temp_list[i]  !=  ", int(d[n][i]), "then temp_list[i]=-1"
			if temp_list[i]!=int(d[n][i]): 
				temp_list[i] = -1
		print temp_list
		if not possible_to_update(temp_list): return [] #temp_list should be all -1's
	return temp_list
#
def update_state_cell_rows(C, state, new_list):#updates state board rows
	#
	print "board for oppdatering"
	for s in state.get_board():
		print s
	#
	for n in xrange(len(new_list)):
		if state.board[C[1].get_index()][n]==-1:
			state.board[C[1].get_index()][n]=int(new_list[n])
	#
	print "board etter oppdatering"
	for s in state.get_board():
		print s
def update_state_cell_cols(C, state, new_list):#updates state board columns
	#
	print "board for oppdatering"
	for s in state.get_board():
		print s
	#
	for n in xrange(len(new_list)):
		if state.board[n][C[1].get_index()]==-1:
			state.board[n][C[1].get_index()]=int(new_list[n])
	#
	print "board etter oppdatering"
	for s in state.get_board():
		print s
#
def update_variable_domain(C):#updates the domain based on a cell value
	index = C[0][0]
	d=C[1].get_domain()
	#
	print "domain:"
	for n in d:
		print n
	for n in d:
		print "Hvis  ", n[index], "  !=  ", str(C[0][1]), "fjern fra domain"
		if n[index] != str(C[0][1]):
			d.remove(n)
			print "de var ikke like: ny len", len(d)
	print '\n'
	return d
#
def revice(state, C):#changes a state based on a constraint
	domain_updated=False
	cells_updated=False
	if C[0][1]==-1:
		print "UPDATING CELLS"
		new_list=update_cell(C)
		print "new_list:  ", new_list
		##--update cell rows or columns if needed--##
		if len(new_list)>0:
			if C[1].get_is_row():
				update_state_cell_rows(C, state, new_list)
			else:
				update_state_cell_cols(C, state, new_list)
			cells_updated=True
		##
	else:
		print "UPDATING DOMAIN"
		old_domain_len=len(C[1].get_domain())
		new_domain=update_variable_domain(C)

		##--update domain if needed--##
		if old_domain_len>len(new_domain):
			print "new domain", new_domain
			if C[1].get_is_row():

				state.set_row(C[1].get_index(), new_domain)
				#print "is row", state.get_row(C[1].get_index())
			else:
				state.set_col(C[1].get_index(), new_domain)
				#print "is not row", state.get_col(C[1].get_index()).get_domain()
			domain_updated=True
		##
	return domain_updated, cells_updated
#
###--- Filter methods ---###
def extend_queue_domain(C, state):#extends the GAC_queue when needed
	new_c = deque()
	if C[1].get_is_row():
		for index in xrange(len(C[1].get_domain()[0])):
			print "new constraint:  ", [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ]
			new_c.append( [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ] )
	else:
		for index in xrange(len(C[1].get_domain()[0])):
			print "new constraint  ", [[index, state.get_board_cell( index, C[1].get_index() )], C[1]]
			new_c.append( [ [index, state.get_board_cell( index, C[1].get_index() )], C[1] ] )
	return new_c
#
def extend_queue_cells(C, state):
	new_c = deque()
	if C[1].get_is_row():
		for index in xrange(len(C[1].get_domain()[0])):
			print "Hvis ikke  ", state.get_board_cell(C[1].get_index(), index), " == -1" 
			if state.get_board_cell(C[1].get_index(), index) != -1:
				print "new constraint:  ", [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ]
				new_c.append( [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ] )
	else:
		for index in xrange(len(C[1].get_domain()[0])):
			print "Hvis ikke  ", state.get_board_cell(C[1].get_index(), index), " == -1"
			if state.get_board_cell(C[1].get_index(), index) != -1:
				print "new constraint:  ", [ [index, state.get_board_cell(index, C[1].get_index())], C[1] ]
				new_c.append( [ [index, state.get_board_cell(index, C[1].get_index())], C[1] ] )
	return new_c
#
def Filter(state, queue):#Iterates through the GAC_queue -> runs revice on them
	#while queue:
	for Foo in xrange(1):
		C = queue.popleft()
		print "NY CONSTRAINT:  ", C[0][0], C[0][1], C[1].get_domain()
		domain_updated, cells_updated = revice(state, C)
		if domain_updated:
			print "domain updated"
			queue.extend(extend_queue_domain(C, state))
			print "\n"
		if cells_updated:
			print "cells updated"
			queue.extend(extend_queue_cells(C, state))
			print "\n"
#
###--- Methods to check validity of a state ---###
def is_valid_state(state):
	for var in state.get_rows():
		if len(var.get_domain()) == 0: return False
	for var in state.get_cols():
		if len(var.get_domain()) == 0: return False
	return True
#
def is_done(state):
	pass
###--- Astar ---###
def Astar(start_state):
	print "Astar is running..."
	all_states = create_dictionary(start_state.get_h())
	all_states[start_state.get_h()].append(start_state)
	#
	children = generate_child_states(start_state)
	for c in children:
		print "assumption: ", c.get_assumption()
		queue = create_GAC_queue(c, c.get_assumption())
		print "Queue:"
		for q in queue:
			print q[0], q[1].get_is_row(), q[1].get_index()
		#for q in queue:
		#	print q[1].get_is_row()
		#print "\n"
		print "h for Filter", c.get_h()
		Filter(c, queue)
		c.set_h(c.calculate_h())
		print "h etter Filter", c.get_h(), "  g verdi", c.get_g(), '\n\n'
		for row in c.get_board():
			print row
		print '\n\n\n'
		pass
#
#
#if __name__ == '__main__':
	#qc = Queue()
	#qr = Queue()
	#Astar(rf.read_graph("nono-heart.txt")#,qc,qr))
Astar(rf.read_graph("nono-heart.txt"))