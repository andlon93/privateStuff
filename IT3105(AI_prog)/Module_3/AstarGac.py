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
'''def possible_to_update(t):#Checks whether any of the cells van be updated
		for i in t:
			if i!=-1: return True
		return False
#
def update_state_cell_rows(C, state, new_list):#updates state board rows
	#
	#print "board for oppdatering"
	#for s in state.get_board():
	#	print s
	#
	for n in xrange(len(new_list)):
		if state.board[C[1].get_index()][n]==-1:
			state.board[C[1].get_index()][n]=int(new_list[n])
	#
	#print "board etter oppdatering"
	#for s in state.get_board():
	#	print s
def update_state_cell_cols(C, state, new_list):#updates state board columns
	#
	#print "board for oppdatering"
	#for s in state.get_board():
	#	print s
	#
	for n in xrange(len(new_list)):
		if state.board[n][C[1].get_index()]==-1:
			state.board[n][C[1].get_index()]=int(new_list[n])
	#
	#print "board etter oppdatering"
	#for s in state.get_board():
	#	print s
#
def revice(state, C):#changes a state based on a constraint
	domain_updated=False
	cells_updated=False
	if C[0][1] == -1:
		#print "UPDATING CELLS"
		new_list=update_cell(C)
		#print "new_list:  ", new_list
		##--update cell rows or columns if needed--##
		if len(new_list)>0 and len(C[1].get_domain()) > 1:
			if C[1].get_is_row():
				update_state_cell_rows(C, state, new_list)
			else:
				update_state_cell_cols(C, state, new_list)
			cells_updated=True
		##
	else:
		#print "UPDATING DOMAIN"
		old_domain_len=len(C[1].get_domain())
		new_domain=update_variable_domain(C)

		##--update domain if needed--##
		if old_domain_len>len(new_domain):
			#print "new domain", new_domain
			if C[1].get_is_row():

				state.set_row(C[1].get_index(), new_domain)
				#print "is row", state.get_row(C[1].get_index())
			else:
				state.set_col(C[1].get_index(), new_domain)
				#print "is not row", state.get_col(C[1].get_index()).get_domain()
			domain_updated=True
		##
	return domain_updated, cells_updated
#######'''
def update_board_from_one_domain(state, C):
	if C[1].get_is_row():
		for d in xrange( len(C[1].get_domain()[0])):
			state.set_board_cell(C[1].get_index(), d, int(C[1].get_domain()[0][d]))
	else:
		for d in xrange( len(C[1].get_domain()[0])):
			state.set_board_cell(d, C[1].get_index(), int(C[1].get_domain()[0][d]))
#
def update_cell(state, C):#updates the cell in Board if possible
	domains = C[1].get_domain()
	index = C[0][0]
	temp_cell = domains[0][index]
	for n in xrange(1, len(domains)):
		if temp_cell != domain[n][index]:
			return False
	##kan oppdatere cell fordi alle domenene har lik verdi for ruta
	if C[1].get_is_row():
		state.set_board_cell( C[1].get_index(), index )
	else:
		state.set_board_cell( index, C[1].get_index() )
	return True
#
def update_variable_domain(state, C):#updates the domain based on a cell value
	index = C[0][0]
	domains = C[1].get_domain()
	new_domain = []
	#
	#print "domain:"
	for n in domains:
		#print "Hvis  ", n[index], "  ==  ", str(C[0][1]), "legg til i new domain"
		if n[index] == str(C[0][1]):
			new_domain.append(n)
			#print "de var like: ny len", len(new_domain)
	#print '\n'
	if len(domains) > len(new_domain):
		if C[1].get_is_row():
			state.set_row(C[1].get_index(), new_domain)
		else:
			state.set_col(C[1].get_index(), new_domain)
		return True
	return False
#
def revice2(state, C):
	board_updated = False
	cell_updated = False
	is_valid_state = True
	domain_updated = False
	##
	domains = C[1].get_domain()
	cell = C[0][1]
	##
	if len(domains) == 0:
		print "ugyldig state"
		is_valid_state = False
	elif len(domains) == 1:
		print "kun et gyldig domene"
		update_board_from_one_domain(state, C)
		board_updated = True
	elif cell == -1:
		print "rute er ukjent. prov aa sette dens verdi"
		cell_updated = update_cell(state, domains, cell)
	elif cell != -1:
		print "rute er bestemt. Prov aa redusere domene"
		domain_updated = update_variable_domain(state, C)
		if C[1].get_is_row():
			if len(state.get_row(C[0][0])) == 1:
				update_board_from_one_domain(state, C)
				board_updated = True
				domain_updated = False
		else:
			if len(state.get_col(C[0][0])) == 1:
				update_board_from_one_domain(state, C)
				board_updated = True
				domain_updated = False
	return is_valid_state, board_updated, cell_updated, domain_updated
#
###--- Filter methods ---###

#
def extend_queue_domain_updated(C, state):
	new_c = deque()
	if C[1].get_is_row():
		for index in xrange(len(C[1].get_domain()[0])):
			#print "Hvis ikke  ", state.get_board_cell(C[1].get_index(), index), " == -1" 
			if state.get_board_cell(C[1].get_index(), index) != -1:
				#print "new constraint:  ", [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ]
				new_c.append( [ [index, state.get_board_cell(C[1].get_index(), index)], C[1] ] )
	else:
		for index in xrange(len(C[1].get_domain()[0])):
			#print "Hvis ikke  ", state.get_board_cell(index, C[1].get_index()), " == -1"
			if state.get_board_cell(index, C[1].get_index()) != -1:
				#print "new constraint:  ", [ [index, state.get_board_cell(index, C[1].get_index())], C[1] ]
				new_c.append( [ [index, state.get_board_cell(index, C[1].get_index())], C[1] ] )
	return new_c
#
def Filter(state, queue):#Iterates through the GAC_queue -> runs revice on them
	while queue:
		C = queue.popleft()
		#print "NY CONSTRAINT:  ", C[0][0], C[0][1], C[1].get_domain()
		is_valid_state, board_updated, cell_updated, domain_updated = revice2(state, C)
		if not is_valid_state: return False
		elif board_updated:
			print "board er oppdatert med ny rad eller kolonne."
			print "legg inn C med hver verdi og rad eller kolonne(motsatt av hva det var)"
			
		elif cell_updated:
			print "en rute er oppdatert. Legg in C med dens verdi og rad og kolonne"
			if C[1].get_is_row():
				domain = state.get_row(C[1].get_index()).get_domain()
				val = state.get_board_cell( C[1].get_index(), C[0][0] )
				new_c = [[[C[0][0], val], domain]]
				#
				domain = state.get_col(C[0][0]).get_domain()
				new_c.append( [C[1].get_index(), val], domain] )
				#
			else:
				domain = state.get_col(C[1].get_index()).get_domain()
				val = state.get_board_cell(C[0][0], C[1].get_index())
				new_c = [[[C[0][0], val], domain]]
				#
				domain = state.get_row( C[0][0] ).get_domain()
				new_c.append( [C[1].get_index(), val], domain] )
		elif domain_updated:
			print "domenet er redusert, men er ikke lengde 1."
			print "legg in C med hver verdi != -1 og raden eller kolonnen og prov aa sett en"
			queue.extend( extend_queue_domain_updated(C, state) )

	return True
'''if domain_updated:
	#print "domain updated"
	queue.extend(extend_queue_domain(C, state))
	#print "\n"
if cells_updated:
	#print "cells updated"
	queue.extend(extend_queue_cells(C, state))
	#print "\n"'''
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
	#import gui
	print "Astar is running..."
	all_states = create_dictionary(start_state.get_h())
	all_states[start_state.get_h()].append(start_state)
	#
	children = generate_child_states(start_state)
	for c in children:

		#print "assumption: ", c.get_assumption()


		'''gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(c.get_board()))
		gui.app.processEvents()
		print "GUI processing from astar"
		time.sleep(1.5)'''


		#print "assumption: ", c.get_assumption()

		queue = create_GAC_queue(c, c.get_assumption())
		#print "Queue:"
		#for q in queue:
		#	print q[0], q[1].get_is_row(), q[1].get_index()
		#for q in queue:
		#	print q[1].get_is_row()
		#print "\n"
		print "h for Filter", c.get_h()
		for row in c.get_board():
			print row
		Filter(c, queue)
		c.set_h(c.calculate_h())
		print "h etter Filter", c.get_h(), "  g verdi", c.get_g(),"\n"
		for row in c.get_board():
			print row
		print '\n\n'

if __name__ == '__main__':
	Astar(rf.read_graph("nono-cat.txt"))
