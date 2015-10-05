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
	#print best_row_variable, best_col_variable
	'''if row_list[best_row_variable] <= col_list[best_col_variable]:
		for domain in rows[best_row_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			rows[best_row_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_row(best_row_variable), children[-1].get_row(best_row_variable).get_domain()] )
			#print "is_row on new child: ", children[-1].get_assumption()[0].get_is_row()
	else:
		for domain in cols[best_col_variable].get_domain():
			cols = copy.deepcopy(state.get_cols())
			rows = copy.deepcopy(state.get_rows())
			cols[best_col_variable].domain = [domain]
			children.append( State.State(rows, cols, state) )
			children[-1].set_assumption( [children[-1].get_col(best_col_variable), children[-1].get_col(best_col_variable).get_domain()] )
			#print "is_row on new child: ", children[-1].get_assumption()'''
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



	if len(d_0) == 0 or len(d_1) == 0 or len(d_1)==1:
		if is_row_C1:
			#print "domain for nytt rad: ",state.get_row(C[1].get_index()).domain
			#print state.get_row(C[1].get_index()).get_domain()
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			#print "domain for nytt kol: ",state.get_col(C[1].get_index()).domain
			#print state.get_col(C[1].get_index()).get_domain()
			return len(state.get_col(C[1].get_index()).get_domain())
	index_d0 = C[0].get_index()
	index_d1 = C[1].get_index()
	#print "index_d0", index_d0, "index_d1", index_d1
	#print d_0[0][index_d1]
	#
	#print d_0
	##
	#print len(d_0), d_0, '\n'
	#for d in d_1:
	#	print d
	##
	new_domain = []
	#print "d0[0][index_d1]: ",d_0[0][index_d1]
	if len(d_0) == 1:
		for n in xrange(len(d_1)):
			#print n, ": ",	d_1[n]
			#print d_0[0][index_d1], d_1[n][index_d0]
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
			#print "domain for nytt rad: ",state.get_row(C[1].get_index()).domain
			state.get_row(C[1].get_index()).domain = copy.deepcopy(new_domain)
			#print state.get_row(C[1].get_index()).get_domain()
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			#print "domain for nytt kol: ",state.get_col(C[1].get_index()).domain
			state.get_col(C[1].get_index()).domain = copy.deepcopy(new_domain)
			#print state.get_col(C[1].get_index()).get_domain()
			return len(state.get_col(C[1].get_index()).get_domain())
	else:
		#####
		if is_row_C1:
			#print "domain for nytt rad: ",state.get_row(C[1].get_index()).domain
			#print state.get_row(C[1].get_index()).get_domain()
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			#print "domain for nytt kol: ",state.get_col(C[1].get_index()).domain
			#print state.get_col(C[1].get_index()).get_domain()
			return len(state.get_col(C[1].get_index()).get_domain())
		#####
		#print "ER INNE I ELSE-CLAUSEN", "len d_0",len(d_0)
		#print "index", index
		is_possible = True
		#print temp_val
		#print is_possible
		for n in xrange(1, len(d_0)):
			#print d_0[n][index_d1], d_0[0][index_d1]
			if d_0[n][index_d1] != d_0[0][index_d1]:
				#print "test"
				is_possible = False
		#print temp_val
		#print "is_possible", is_possible

		if is_possible:
			for n in xrange(len(d_1)):
				#print n, ": ",	d_1[n]
				#print d_0[0][index_d1], d_1[n][index_d0]
				#print index, len(d_0[0]), len(d_1[n])
				if d_0[0][index_d1] == d_1[n][index_d0]:
					new_domain.append(d_1[0])
					'''if is_row_C1:
						state.get_row(C[1].get_index()).get_domain().remove(d_1[n])
					else:
						state.get_col(C[1].get_index()).get_domain().remove(d_1[n])'''
		else:
			if is_row_C1:
				#print "domain for nytt rad: ",state.get_row(C[1].get_index()).domain
				return len(state.get_row(C[1].get_index()).get_domain())

				return len(state.get_col(C[1].get_index()).get_domain())
				#print "domain etter kol: ", state.get_col(C[1].get_index()).domain


		#print "New domain: ",new_domain
		if is_row_C1:
			#print "domain for nytt rad: ",state.get_row(C[1].get_index()).domain
			state.get_row(C[1].get_index()).domain = copy.deepcopy(new_domain)
			#print "domain etter: ", state.get_row(C[1].get_index()).domain
			return len(state.get_row(C[1].get_index()).get_domain())
		else:
			#print "domain for nytt kol: ",state.get_col(C[1].get_index()).domain
			state.get_col(C[1].get_index()).domain = copy.deepcopy(new_domain)
			#print state.get_col(C[1].get_index()).domain
			return len(state.get_col(C[1].get_index()).get_domain())
##############################
def revise(C, state):
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
		return len(state.get_row(C[1].get_index()).get_domain())
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
		#print "q[0]: ",q[0].get_is_row(), q[0].get_index(), "  q[1]:", q[1].get_is_row(), q[1].get_index()
		length_post_revice = revise(q,state)			  #kjorer revice paa constrainten som ble poppet
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
		done = False

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
						done = True # If we find another 1 after done == True, there are too many.

			elif c == '0' and group_done == True:
				# Found a 0 when excepting a 0
				group_done = False

			elif c == '1' and done == True:
				# Found a 1 after we are supposed to have found them all.
				return False
		return True

valid_chars = ['0','1']
combos = []


def is_valid_state(board, constraints_rows, constraints_columns):
	del combos[:]
	rows_valid = [False] * len(board)
	for row in range (len(board)):
		generate_combos(board[row],"")
		for combo in combos:
			if is_Valid_line(combo, constraints_rows[row]):
				rows_valid[row] = True
		del combos[:]

	del combos[:]

	cols_valid = [False] * len(board[0])
	temp_string = ""
	for column_index in range (len(board[0])):
		for row_index in range (len(board)):
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
			print "NOT VALID STATE - rows"
			return False
	print cols_valid
	for t in cols_valid:
		if t == False:
			print
			print "NOT VALID STATE - cols"
			return False
	return True

def is_done(state):
	for row in state.rows:
		if len(row.domain) != 1:
			return False
	for col in state.cols:
		if len(col.domain) != 1:
			return False
	return True


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
###--- Astar ---###
def Astar(start_state, constraints_rows, constraints_columns):
	start_time2 = time.time()
	print "Astar is running..."
	closed = create_dictionary(start_state.get_h())
	##
	all_states = create_dictionary(start_state.get_h())
	current_state = start_state
	constraints = deque()
	for row in current_state.get_rows():
		for col in current_state.get_cols():
			constraints.append([row, col])
			constraints.append([col, row])

	temp, board = current_state.make_board()
	for r in board:
		print r
	Filter(current_state, constraints)
	print "\nFirst filtering done \n"
	temp, board = current_state.make_board()
	for r in board:
		print r
	print ""
	# for row in current_state.get_rows():
	# 	print row.domain
	# print '\n'
	# for col in current_state.get_cols():
	# 	print col.domain


	children = generate_child_states(current_state)
	#
	while True:
		if children:
			valid_children = []
			#print children
			for child in children:
				if True:
					#if not is_in_closed(closed, child):
					#print "child not in closed"
					#current_state.set_assumption((current_state.rows[0],current_state.rows[0].domain[0]))
					queue = create_GAC_queue(child)
					# for col in current_state.cols:
					# 	print len(col.domain)
					# print "\n"
					# for row in current_state.rows:
					# 	print len(row.domain)
					'''print "for filter"
					for row in child.get_rows():
						print row.get_domain()
					for col in child.get_cols():
						print col.get_domain()
					print "\n\n"'''

					Filter(child,queue)
					'''print "etter filter"
					for row in child.get_rows():
						print row.get_domain()
					for col in child.get_cols():
						print col.get_domain()'''

					temp, board = child.make_board()
					for b in board:
						print b


					# print '\n'
					# for col in child.cols:
					# 	print col.domain
					# print '\n'
					# for r in board:
					# 	print r
					# print "Temp", temp
					if temp and is_valid_state(board, constraints_rows, constraints_columns):
						print "H for filter: ",child.get_h()
						child.set_h(child.calculate_h())
						print "H etter filter: ",child.get_h(),"\n"
						valid_children.append(child)
						print "ROW"
						for row in child.get_rows():
							print row.get_domain()
						print "COULMNS"
						for col in child.get_cols():
							print col.get_domain()
						####
						board_done = True
						for row in board:
							for c in row:
								#print c
								if c == '2':
									board_done = False
						####
						##-- check if if child is a solution --##
						if board_done or is_done(child):
							print("--- Solved in %s seconds ---" % (time.time() - start_time2))
							print "ER I MAAL!!!"
							print "Antall steg til maal: ", child.get_g()
							print "\nBRETTTET"
							for b in board:
								print b
							#for row in child.get_rows():
							# 	print row.get_domain()[0]
							#for col in child.get_cols():
							#	print col.get_domain()[0]
							return True
						##

					# print "\n\nafter filter"
					# for col in current_state.cols:
					# 	print len(col.domain)
					# print "\n"
					# for row in current_state.rows:
					# 	print len(row.domain)

					print "\n"
			#return True
			#print "valid_children",valid_children

			all_states = add_states_to_dict(valid_children, all_states)
			#for s in all_states:
			#	if all_states[s]:
			#		print s, all_states[s]
			current_state = get_best_state(all_states)
			print "current_state", 	current_state
			# if True:
			# 	print "rows:"
			# 	for row in current_state.get_rows():
			# 		print row.get_domain()
			# 	print "\nCols:"
			# 	for col in current_state.get_cols():
			# 		print col.get_domain()
			# 	print "\n\n"

			children = generate_child_states(current_state)
			#
			#all_states[current_state.get_h()+current_state.get_g()].remove(current_state)
			all_states[current_state.get_h()].remove(current_state)
			closed[current_state.get_h()].append(current_state)
			#
			'''
			if is_done(current_state):
				print "FERDIG"
			'''
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
	start_state, rows, cols = rf.read_graph("nono-sailboat.txt")
	Astar(start_state,rows,cols)
	# print is_Valid_line("0011111000",[4])
	# generate_combos("00111112000","")
	# for comb in combos:
	# 	print comb
