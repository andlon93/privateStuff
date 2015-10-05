#!/usr/bin/env python
# -*- coding: utf-8 -*-
import State
import Variable
import readfile as rf
import random
import time
import copy
import threading
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
			#d[state.get_h()+state.get_g()].append(state)
			d[state.get_h()].append(state)
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
	#print row_list,'\n',col_list
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
	#Creates child for the row and col with smallest domain
	#Creates one object for each possibility for the domains
	for domain in rows[best_row_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			rows[best_row_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_row(best_row_variable), children[-1].get_row(best_row_variable).get_domain()] )
	for domain in cols[best_col_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			cols[best_col_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_col(best_col_variable), children[-1].get_col(best_col_variable).get_domain()] )
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
def revise(C, state):
	if show_gui_revise:
		import gui
	if C[0].get_is_row():
		index_d0 = state.get_row(C[0].get_index()).get_index()
		index_d1 = state.get_col(C[1].get_index()).get_index()
		#
		is_possible = True
		#
		if len(state.get_row(C[0].get_index()).get_domain()) == 0 or len(state.get_col(C[1].get_index()).get_domain()) < 2:
			return len(state.get_col(C[1].get_index()).get_domain())
		elif len(state.get_row(C[0].get_index()).get_domain()) > 1:
			for n in xrange(1, len(state.get_row(C[0].get_index()).get_domain())):
				check_val = state.get_row(C[0].get_index()).get_domain()[0][index_d1]
				if check_val != state.get_row(C[0].get_index()).get_domain()[n][index_d1]:
					is_possible = False
		if not is_possible:
			return len(state.get_col(C[1].get_index()).get_domain())
		else:
			check_val = state.get_row(C[0].get_index()).get_domain()[0][index_d1]
			for domain in state.get_col(C[1].get_index()).get_domain():
				if domain[index_d0] != check_val:
					state.get_col(C[1].get_index()).get_domain().remove( domain )
					if show_gui_revise:
						temp, board = state.make_board()
						gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
						gui.app.processEvents()

		return len(state.get_col(C[1].get_index()).get_domain())
	else:
		##-- c[0] == kolonne --##
		index_d0 = state.get_col(C[0].get_index()).get_index()
		index_d1 = state.get_row(C[1].get_index()).get_index()
		#
		is_possible = True
		#
		if len(state.get_col(C[0].get_index()).get_domain()) == 0 or len(state.get_row(C[1].get_index()).get_domain()) < 2:
			return len(state.get_row(C[1].get_index()).get_domain())
		elif len(state.get_col(C[0].get_index()).get_domain()) > 1:
			for n in xrange(1, len(state.get_col(C[0].get_index()).get_domain())):
				check_val = state.get_col(C[0].get_index()).get_domain()[0][index_d1]
				if check_val != state.get_col(C[0].get_index()).get_domain()[n][index_d1]:
					is_possible = False
		if not is_possible:
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			check_val = state.get_col(C[0].get_index()).get_domain()[0][index_d1]
			for domain in state.get_row(C[1].get_index()).get_domain():
				if domain[index_d0] != check_val:
					state.get_row(C[1].get_index()).get_domain().remove( domain )
					if show_gui_revise:
						temp, board = state.make_board()
						gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
						gui.app.processEvents()
		return len(state.get_row(C[1].get_index()).get_domain())
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
#

def draw_gui(state):
	import gui
	print "drawing gui"
	temp, board = state.make_board()
	gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
	gui.app.processEvents()


def Filter(state, queue):#Iterates through the GAC_queue -> runs revice on them
	if show_gui_filter:
		import gui
	while queue:
		q                  = queue.popleft()   	  #popper constraint fra ko
		length_pre_revise  = len(q[1].domain)
		length_post_revice = revise(q,state)			  #kjorer revice paa constrainten som ble poppet
		#
		if length_pre_revise > length_post_revice:  #hvis domenet har blitt forkortet maa nye constarints inn i ko
			if show_gui_filter:
				if len(queue)% 5 == 0:
					#print "Showing gui from filter"
					temp, board = state.make_board()
					gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
					gui.app.processEvents()

			if q[1].get_is_row():
				queue.extend( extend_queue(state, state.get_row(q[1].get_index())))
			else:
				queue.extend( extend_queue(state, state.get_col(q[1].get_index())))
#
###--- Methods to check validity of a state ---###
def is_Valid_line(s, blocks):
		total_1s = s.count('1')
		total_in_blocks = 0
		for j in blocks:
			total_in_blocks += int(j)
		if total_1s != total_in_blocks: # If there are more (or less) "1"s in the input string than there are supposed to, the string is invalid
			return False
		b = copy.deepcopy(blocks) # Blocks. e.g. [1,3,2]
		current_block = 0
		group_done = False
		group_started = False
		for c in s: #For character in string, aka 0 or 1
			if c == '1' and group_done == True:
				# Found a 1 when excepting a 0
				return False
			elif c == '0' and group_done == False and group_started == True:
				# Found a 0 when excpecting a 1
				return False
			elif c == '1' and group_done == False:
				# Found a 1, when looking for 1
				group_started = True
				b[current_block] = int (b[current_block]) - 1 # Decrease remaining number of 1's in the current block
				if b[current_block] == 0:			# If this is 0, it means all of the 1's in the current group has been found
					group_done    = True    		# This group of 1's is done
					group_started = False   		# There is currently no group of 1's active
					current_block += 1				# move to look for the next block of 1's
					if current_block > (len(b)-1):  # If all blocks have been found:
						return True
			elif c == '0' and group_done == True:
				# Found a 0 when excepting a 0
				group_done = False
		return True
####
valid_chars = ['0','1']
combos = []
####
def is_valid_state(board, constraints_rows, constraints_columns):
	del combos[:]
	rows_valid = [False] * len(board)
	for row in xrange (len(board)):
		generate_combos(board[row],"")
		for combo in combos:
			if is_Valid_line(combo, constraints_rows[row]):
				rows_valid[row] = True
		del combos[:]
	del combos[:]
	cols_valid = [False] * len(board[0])
	temp_string = ""
	for column_index in xrange (len(board[0])):
		for row_index in xrange (len(board)):
			temp_string += board[row_index][column_index]
		#temp_string += board[-1][column_index]
		generate_combos(temp_string,"")
		temp_string += board[-1][column_index]
		for combo in combos:
			if is_Valid_line(combo, constraints_columns[column_index]):
				cols_valid[column_index] = True
				break
		del combos[:]
		temp_string = ""
	for t in rows_valid:
		if t == False:
			return False
	for t in cols_valid:
		if t == False:
			return False
	return True
#
def is_done(state):
	for row in state.rows:
		if len(row.domain) != 1:
			return False
	for col in state.cols:
		if len(col.domain) != 1:
			return False
	return True
#
def generate_combos(mask, combination):
	# Takes string of form 0102211 and generates all possible strings, where 2 can be 1 or 0

	if len(mask) <= 0:
		combos.append(combination)
		return
	if mask[0] != '2':
		generate_combos(mask[1:], combination + mask[0])
	else:
		for cha in valid_chars:
			generate_combos(mask[1:], combination + cha)
#

def make_all_constraints(current_state):
	constraints = deque()
	for row in current_state.get_rows():
		for col in current_state.get_cols():
			constraints.append([row, col])
			constraints.append([col, row])
	return constraints
#
def is_board_done(board):
	for row in board:
		for c in row:
			if c == '2':
				return False
	return True
###--- Astar ---###
def Astar(start_state, constraints_rows, constraints_columns):
	if show_gui:
		import gui

	print "press any key to continue"
	raw_input()
	start_time2 = time.time()
	print "Astar running..."
	##
	all_states = create_dictionary(start_state.get_h())
	##
	if show_gui:
		temp, board = start_state.make_board()
		gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
		gui.app.processEvents()
	print "for philter"
	time.sleep(0.5+algorithm_delay)

	Filter(start_state, make_all_constraints(start_state))

	if show_gui:
		temp, board = start_state.make_board()
		gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
		gui.app.processEvents()
		time.sleep(0.2+algorithm_delay)

	temp, board = start_state.make_board()
	children = generate_child_states(start_state)
	#
	nodes_generated = 0
	nodes_expanded = 1
	while True:
		time.sleep(algorithm_delay)
	#for xxx in xrange(2):
		if children:
			nodes_generated += len(children)
			valid_children = []
			for child in children:
				if show_gui:
					gui.app.processEvents()
					temp, board = child.make_board()
					gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
					gui.app.processEvents()
					time.sleep(algorithm_delay)
				#
				Filter(child,create_GAC_queue(child))

				if show_gui:
					temp, board = child.make_board()
					gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
					gui.app.processEvents()
				#
				temp, board = child.make_board()
				#
				if temp and is_valid_state(board, constraints_rows, constraints_columns):
					#print "H for filter: ",child.get_h()
					child.set_h(child.calculate_h())
					#print "H etter filter: ",child.get_h(),"\n"
					valid_children.append(child)
					##-- check if if child is a solution --##
					if is_board_done(board) or is_done(child):
						print("--- Solved in %s seconds ---" % (time.time() - start_time2))
						print "ER I MAAL!!!\n\n"
						print "Number of nodes generated", nodes_generated
						print "Number of nodes expanded", nodes_expanded
						print "Antall steg til maal: ", child.get_g()
						print "\n\nBRETTTET"
						for b in board:
							print b
						gui.app.processEvents()
						temp, board = child.make_board()
						gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
						gui.app.processEvents()

						print "Press ENTER to close gui, input 'n' to keep it open"
						stri = str(raw_input(""))
						if not (stri=="n" or stri=="N"):
							import subprocess
							subprocess.call("taskkill /F /IM python.exe", shell=True)
						time.sleep(10)
						return True
			#

			all_states = add_states_to_dict(valid_children, all_states)
			current_state = get_best_state(all_states)
			nodes_expanded += 1
			gui.app.processEvents()
			temp, board = current_state.make_board()
			gui.rectMatrix = gui.generate_rectMatrix(gui.generate_color_matrix(board))
			gui.app.processEvents()
			time.sleep(algorithm_delay)


			children = generate_child_states(current_state)
			all_states[current_state.get_h()].remove(current_state)
			#
		else:
			current_state = get_best_state(all_states)
			children = generate_child_states(current_state)
			all_states[current_state.get_h()+current_state.get_g()].remove(current_state)

		#
#


show_gui = True
show_gui_revise = False
show_gui_filter = True


algorithm_delay = 0
if __name__ == '__main__':

	start_state, rows, cols = rf.read_graph("nono-cat.txt") #Ikke ende her, endre i gui
	Astar(start_state,rows,cols)

