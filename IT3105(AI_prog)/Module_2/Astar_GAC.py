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
def create_dictionary(l):
	d = {}
	for n in xrange(l+1):
		d[n] = []
	return d
#
def add_states_to_dict(states, d):
	for state in states:
		d[ state.get_heuristic() ].append( state )
	return d
#
def generate_child_states(state, constraints):#Creates childstates with an assumption
	childs = []
	n = len(state.nodes)
	var_list = [0]*n
	if debug_childstates: print "var_list: ", len(var_list), var_list[0], '\n'

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
	for i in xrange(n): #endre maks tre av varaiblene med hoyest forekomst til singletons
		if var_list[i] == max_value and len(state.nodes[i].domain) > 1:
			if debug_childstates:
				print 'index: ', i
				print "parent foer copy: ", state.nodes[i].domain
			new_dict = copy.deepcopy(state.nodes)
			new_dict[i].domain = [new_dict[i].domain[ random.randint(0, len(new_dict[i].domain)-1) ] ]
			if debug_childstates:
				print "new child: ", new_dict[i].domain
				print "parent etter copy: ", state.nodes[i].domain
			childs.append( State.State(new_dict) )
			childs[-1].set_assumption(i)
			###
			###
			if debug_childstates:
				print "parent heuristic: ", state.get_heuristic()
				print "child heuristic: ", childs[-1].get_heuristic(), "assumption: ", childs[-1].get_assumption() , '\n'
			counter += 1
			if counter == 3: 
				if debug_childstates: print '\n\n'
				return childs, max_value		

	return childs, max_value
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

	#for qqq in xrange(7):
	while queue:
		constraint = queue.popleft()#popper constraint fra ko
		if debug: print "constraint: ", constraint
		#
		length_pre_revise = len(state.nodes[constraint[0]].domain)
		#
		if debug: print "for:", state.nodes[constraint[0]].domain
		length_post_revice = revice(state, constraint)#kjorer revice paa constrainten som ble poppet
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
def Astar(start_state, constraints):
	import main
	#main.rungui()
	
	all_states = create_dictionary( start_state.get_heuristic() )#dict over alle states som ses paa. Nokkel er heurestikkverdier(heltall)
	##print "dict laget: ", len(all_states), '\n'
	#
	all_states[start_state.get_heuristic()].append(start_state) #adding start_state into dictionary
	##print "start state lagt inn i dict: ", all_states[start_state.get_heuristic()], '\n'
	#
	current_state = get_best_state(all_states)


	main.circle_matrix = main.generate_circle_matrix(current_state)
	main.app.processEvents()


	##print "funnet beste state: ", current_state, '\n\n'
	#
	#
	while True:
	#for xyz in xrange(1):
		#
		new_states, number_constarints = generate_child_states( current_state, constraints )
		if debug: print "new child states:", new_states, '\n\n'
		#
		for new_state in new_states:
			#print new_state.get_assumption
			queue = create_GAC_constraint_queue(new_state.get_assumption(), constraints)
			if debug: print "queue:", queue
			Filter( new_state, queue, constraints )
			new_state.set_heuristic( new_state.calculate_heuristic() )
			#
			'''for s in new_state.nodes:
				print s, ":", new_state.nodes[s].domain'''
			#
		all_states = add_states_to_dict( new_states, all_states )
		#
		###--- start printing ---###
		if debug:
			print "all_states med barn:"
			for n in xrange(len(all_states)):
				if len(all_states[n]) > 0:
					print n, all_states[n]
			print '\n\n'
		###--- end printing ---###
		#
		current_state = get_best_state(all_states)#Staten som analyseres naa er alltid current_state


		main.circle_matrix = main.generate_circle_matrix(current_state)
		main.app.processEvents()
		time.sleep(0.5)

		#
		#
		for domain in current_state.nodes:
			if len(current_state.nodes[domain].domain) == 0:
				all_states[current_state.get_heuristic()].remove(current_state)
				current_state = get_best_state(all_states)

				main.circle_matrix = main.generate_circle_matrix(current_state)
				main.app.processEvents()
				#print "current state er ikke gyldig"
		#
		#
		'''if current_state.get_heuristic() < 5:
			for domain in current_state.nodes:
					print domain, current_state.nodes[domain].domain
			print '\n\n ny heuristic:', current_state.get_heuristic()'''
		#
		#
		if current_state.get_heuristic() == 0: 
			print '\n\n', True, '\n'
			for domain in current_state.nodes:
				print domain, current_state.nodes[domain].domain
			return True	
#
# s, c = rf.read_graph("graph6.txt")
# Astar(s, c)