import readfile as rf
import copy
import State
import time
import random
from collections import deque
#from threading import *
#
#
debug = False
debug_childstates = False
algorithm_delay = 0

def create_dictionary(l):
	d = {}
	for n in xrange(l+1):
		d[n] = []
	return d
#
def add_states_to_dict(states, d):
	for state in states:
		try:
			d[ state.get_heuristic() ].append( state )
		except:
			print "Algorithm failed - add_states_to_dict"
			return False
	return d
#
def generate_child_states(state, constraints):#Creates childtates with an assumption
	children = []
	n = len(state.nodes)
	var_list = [0]*n
	if debug_childstates: print "var_list: ", len(var_list), var_list[0], '\n'

	number_of_children = 0

	max_value = 0
	for c in constraints:#telle antall forekomster av hver variabel
		if len( state.nodes[ c[0] ].domain ) > 1: var_list[c[0]] += 1
		if len( state.nodes[ c[1] ].domain ) > 1: var_list[c[1]] += 1
		if var_list[c[0]] > max_value:
			max_value = var_list[c[0]]
		if var_list[c[1]] > max_value:
			max_value = var_list[c[1]]
	if debug_childstates: print "max: ", max_value, '\n'

	counter = 0
	while number_of_children < 3:
		for i in xrange(n): #endre maks tre av varaiblene med hoyest forekomst til singletons
			if var_list[i] == max_value and len(state.nodes[i].domain) > 1:
				if debug_childstates:
					print 'index: ', i
					print "parent foer copy: ", state.nodes[i].domain
				new_dict = copy.deepcopy(state.nodes)

				choose_random_value = random.randint(0, len(new_dict[i].domain)-1)

				new_dict[i].domain = [new_dict[i].domain[ choose_random_value ] ]
				if debug_childstates:
					print "new child: ", new_dict[i].domain
					print "parent etter copy: ", state.nodes[i].domain

				temp_state = State.State(new_dict)

				if is_valid_state(temp_state,constraints):
					children.append( temp_state )
					children[-1].set_assumption([i, new_dict[i].domain[0]])
					children[-1].set_parent(state)
					number_of_children = number_of_children + 1

					if show_gui:
						gui.circle_matrix = gui.generate_circle_matrix(temp_state)
						gui.app.processEvents()

					###
					###
					if debug_childstates:
						print "parent heuristic: ", state.get_heuristic()
						print "child heuristic: ", children[-1].get_heuristic(), "assumption: ", children[-1].get_assumption() , '\n'
					counter += 1
					if counter == 3:
						if debug_childstates: print '\n\n'
						return children, max_value
		max_value = max_value - 1
		if max_value < 0:
			print "children created ", len(children)
			return children, max_value
		#print "Max_value: ",max_value

	return children, max_value
#
def generate_child_states2(state, constraints):
	from random import randint
	children = []
	for index in state.nodes:
		if len(state.nodes[index].domain) > 1:
			for n in state.nodes[index].domain:
				new_dict = copy.deepcopy(state.nodes)
				new_dict[index].domain = [n]
				temp_state = State.State(new_dict)
				temp_state.set_assumption([index, n])
				temp_state.set_parent(state)
				children.append(temp_state)
			#print "children:", children
			if len(children)>=1:
				return children
#
def get_best_state(all_states):	#iterates and returns one state from the list with lowest heuristic
	for i in all_states:
		if all_states[i]:
			return all_states[i][ random.randint(0, len(all_states[i])-1) ]
#
def create_GAC_constraint_queue(assumption, constraints):
	queue = deque()
	for C in constraints:
		if C[0] == assumption:
			queue.append( [C[1], C] )
		elif C[1] == assumption:
			queue.append( [C[0], C] )
	return queue
#
def revice2(state, c):
	#change = c[0]
	#change_after = !c[0]
	#print "change index", c[0]
	#print "len av change index", len(state.nodes[c[0]].domain)
	#if c[0] == c[1][0]: print "len av check index", len(state.nodes[c[1][1]].domain)
	#elif c[0] == c[1][1]: print "len av check index", len(state.nodes[c[1][0]].domain)


	if len(state.nodes[c[0]].domain) < 2:
		return len(state.nodes[c[0]].domain)
	elif c[0] == c[1][0] and len(state.nodes[c[1][1]].domain) == 1:
		check_node = state.nodes[c[1][1]].domain[0]
	elif c[0] == c[1][1] and len(state.nodes[c[1][0]].domain) == 1:
		check_node = state.nodes[c[1][0]].domain[0]
	else:
		return len(state.nodes[c[0]].domain)

	#print "check_node: ", check_node
	#print "change node: ", state.nodes[c[0]].domain
	for change_node in state.nodes[c[0]].domain:
		if change_node == check_node:
			state.nodes[c[0]].domain.remove(change_node)
			#print "changed node: ", state.nodes[c[0]].domain, "new len", len(state.nodes[c[0]].domain)
			return len(state.nodes[c[0]].domain)

	#print "changed node: ", state.nodes[c[0]].domain
	return len(state.nodes[c[0]].domain)
#
def revice(state, constraint):
	for n in xrange(2):
		if constraint[1][n] != constraint[0]:
			index = constraint[1][n]
	if debug:
		print "fjerne med henhold til: ", state.nodes[index].domain
		print index, ":", state.nodes[index].domain, "skal fjernes fra domain", constraint[0],":",state.nodes[constraint[0]].domain
	#
	if len(state.nodes[index].domain) == 1:
		check_value = state.nodes[index].domain[0]
		for change_value in state.nodes[constraint[0]].domain:
			if debug: print "check_value", check_value, "   change_value", change_value
			if change_value == check_value:
				state.nodes[constraint[0]].domain.remove(change_value)
	return len(state.nodes[constraint[0]].domain)
#
def extend_queue(x, constraints):
	l = []
	for C in constraints:
		if C[0] == x:
			l.append( [C[1], C] )
		elif C[1] == x:
			l.append( [C[0], C] )
	return l
	pass
#
def Filter(state, queue, constraints):

	#for qqq in xrange(2):
	while queue:
		constraint = queue.popleft()#popper constraint fra ko
		if debug: print "constraint: ", constraint
		#
		length_pre_revise = len(state.nodes[constraint[0]].domain)
		#
		if debug: print "for:", state.nodes[constraint[0]].domain
		length_post_revice = revice2(state, constraint)#kjorer revice paa constrainten som ble poppet
		if debug: print "etter: ", state.nodes[constraint[0]].domain, '\n'
		#
		if length_pre_revise > length_post_revice:#hvis domenet har blitt forkortet maa nye constarints inn i ko
			if debug: print "domenet her blitt forkortet. Maa oppdatere kooen"
			queue.extend( extend_queue(constraint[0], constraints) )
			###--- print q ---###
			#for q in queue:
			#	print q
			###--- print q ---###



	pass
#
def is_valid_state(state, constraints):
	for node in state.nodes:
		if len(state.nodes[node].domain) == 0:
			return False
	for C in constraints:
		if len(state.nodes[C[0]].domain) == 1 and len(state.nodes[C[1]].domain) == 1:
			if state.nodes[C[0]].domain[0] == state.nodes[C[1]].domain[0]:
				return False
	return True
#
def is_done(state, constraints):
	for c in constraints:
		if len(state.nodes[c[0]].domain) != 1:
			return False
		elif len(state.nodes[c[1]].domain) != 1:
			return False
		elif state.nodes[c[0]].domain[0] == state.nodes[c[1]].domain[0]:
			return False
	return True
#
def Astar(start_state, constraints):
	start_time = time.time()
	if show_gui:
		import gui
	all_states = create_dictionary(start_state.get_heuristic())

	start_state.set_assumption([0, 0])
	start_state.nodes[0].domain = [0]
	queue = create_GAC_constraint_queue(start_state.get_assumption()[0], constraints)
	Filter(start_state, queue, constraints)
	start_state.set_heuristic( start_state.calculate_heuristic() )
	all_states[start_state.get_heuristic()].append(start_state)

	#print "ny heuristic", start_state.get_heuristic()

	#for node in start_state.nodes:
	#	print node, ":", start_state.nodes[node].domain

	current_state = start_state
	while True:
		new_states = generate_child_states2(current_state, constraints)
		if len(new_states) != 0:
			valid_states = []
			parent = new_states[0].get_parent()
			all_states[parent.get_heuristic()].remove(parent)
			for new_state in new_states:
				queue = create_GAC_constraint_queue(new_state.get_assumption()[0], constraints)
				Filter(new_state, queue, constraints)
				if is_valid_state(new_state, constraints):
					new_state.set_heuristic( new_state.calculate_heuristic() )
					valid_states.append(new_state)
					#print "ny heuristic", new_state.get_heuristic()
				else:
					#print "invalid state", new_state.get_assumption()
					#print "parent heuristic FOR", parent.get_heuristic()
					parent.nodes[new_state.get_assumption()[0]].domain.remove(new_state.get_assumption()[1])

			if is_valid_state(parent, constraints):
				#print "heuristic for", parent.get_heuristic()
				parent.set_heuristic(parent.calculate_heuristic())
				#print "heuristic etter", parent.get_heuristic()
				#print "all_states FOR", all_states[parent.get_heuristic()]
				all_states[parent.get_heuristic()].append(parent)
				#print "all_states ETTER", all_states[parent.get_heuristic()]

			all_states = add_states_to_dict(valid_states, all_states)
			current_state = get_best_state(all_states)
			time.sleep(algorithm_delay)
			#
			if is_done(current_state, constraints):
				print "Done"
				if show_gui:
					gui.circle_matrix = gui.generate_circle_matrix(current_state)
					gui.app.processEvents()
					print("--- %s seconds ---" % (time.time() - start_time))
					print ""
					print "Press ENTER to close gui, input 'n' to keep it open"
					stri = str(raw_input(""))
					if not (stri=="n" or stri=="N"):
						import subprocess
						subprocess.call("taskkill /F /IM python.exe", shell=True)
				for C in constraints:
					print current_state.nodes[C[0]].domain, current_state.nodes[C[1]].domain
				print("--- %s seconds ---" % (time.time() - start_time))
				print "--------------------------------------------"
				return True


			if show_gui:
				gui.circle_matrix = gui.generate_circle_matrix(current_state)
				gui.app.processEvents()
				# time.sleep(1)


		else:
			all_states[current_state.get_heuristic()].remove(current_state)
			current_state = get_best_state(all_states)
			#
			if is_done(current_state, constraints):

				print "ER FERDIG"

				for C in constraints:
					print current_state.nodes[C[0]].domain, current_state.nodes[C[1]].domain
				if show_gui:
					gui.circle_matrix = gui.generate_circle_matrix(current_state)
					gui.app.processEvents()
					time.sleep(5)
				return True

show_gui = False
def run(delay):
	if not show_gui:
		s, c = rf.read_graph("graph6.txt")
		Astar(s, c)
	else:
		algorithm_delay = delay
# def Astar(start_state, constraints):
# 	import main


# 	all_states = create_dictionary( start_state.get_heuristic() )#dict over alle states som ses paa. Nokkel er heurestikkverdier(heltall)
# 	##print "dict laget: ", len(all_states), '\n'
# 	#
# 	all_states[start_state.get_heuristic()].append(start_state) #adding start_state into dictionary
# 	##print "start state lagt inn i dict: ", all_states[start_state.get_heuristic()], '\n'
# 	#
# 	current_state = get_best_state(all_states)


# 	main.circle_matrix = main.generate_circle_matrix(current_state)
# 	main.app.processEvents()


# 	##print "funnet beste state: ", current_state, '\n\n'
# 	#
# 	#
# 	while True:
# 	#for xyz in xrange(1):
# 		#
# 		new_states, number_constarints = generate_child_states( current_state, constraints )


# 		if len(new_states) == 0:
# 			all_states[current_state.get_heuristic()].remove(current_state)

# 			current_state = get_best_state(all_states)

# 		if debug: print "new child states:", new_states, '\n\n'
# 		#
# 		new_valid_states = []
# 		for new_state in new_states:

# 			main.circle_matrix = main.generate_circle_matrix(new_state)
# 			main.app.processEvents()

# 			#print new_state.get_assumption()
# 			queue = create_GAC_constraint_queue(new_state.get_assumption(), constraints)
# 			if debug: print "queue:", queue
# 			Filter( new_state, queue, constraints )
# 			new_state.set_heuristic( new_state.calculate_heuristic() )

# 			if not is_valid_state(new_state, constraints):
# 				print "domain som skal fjernes fra", new_state.get_parent().nodes[new_state.get_assumption()[0]].domain
# 				print "remove verdi fra domain", new_state.get_assumption()[1]
# 				print "assumption", new_state.get_assumption()


# 				new_state.get_parent().nodes[new_state.get_assumption()[0]].domain.remove(new_state.get_assumption()[1])

# 				all_states[new_state.get_parent().get_heuristic()].remove(new_state.get_parent())


# 				print "after assumption is removed", new_state.get_parent().nodes[new_state.get_assumption()[0]].domain, '\n'
# 				if is_valid_state(new_state.get_parent(), constraints):
# 					new_state.get_parent().set_heuristic( new_state.get_parent().calculate_heuristic() )
# 					all_states[new_state.get_parent().get_heuristic()].append(new_state.get_parent())
# 			else:
# 				new_valid_states.append(new_state)
# 			#
# 		all_states = add_states_to_dict( new_valid_states, all_states )
# 		#
# 		###--- start printing ---###
# 		if debug:
# 			print "all_states med barn:"
# 			for n in xrange(len(all_states)):
# 				if len(all_states[n]) > 0:
# 					print n, all_states[n]
# 			print '\n\n'
# 		###--- end printing ---###
# 		#
# 		try:
# 			current_state = get_best_state(all_states)#Staten som analyseres naa er alltid current_state
# 		except:
# 			print "Algorithm failed - no more states"
# 			break

# 		main.circle_matrix = main.generate_circle_matrix(current_state)
# 		main.app.processEvents()
# 		# time.sleep(0.1)

# 		#
# 		#
# 		'''for domain in current_state.nodes:
# 			if len(current_state.nodes[domain].domain) == 0:
# 				all_states[current_state.get_heuristic()].remove(current_state)
# 				current_state = get_best_state(all_states)

# 				main.circle_matrix = main.generate_circle_matrix(current_state)
# 				main.app.processEvents()'''
# 				# time.sleep(0.1)
# 				#print "current state er ikke gyldig"
# 		#
# 		#
# 		'''if current_state.get_heuristic() < 5:
# 			for domain in current_state.nodes:
# 					print domain, current_state.nodes[domain].domain
# 			print '\n\n ny heuristic:', current_state.get_heuristic()'''
# 		#
# 		#
# 		if current_state.get_heuristic() == 0:
# 			print '\n\n', True, '\n'
# 			for domain in current_state.nodes:
# 				print domain, current_state.nodes[domain].domain
# 			return True
# #
