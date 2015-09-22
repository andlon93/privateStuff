import readfile as rf
import copy
import State
import random
from collections import deque
#
#
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
	print "var_list: ", len(var_list), var_list[0], '\n'

	max_value = 0
	for c in constraints:#telle antall forekomster av hver variabel
		var_list[c[0]] += 1
		var_list[c[1]] += 1
		if var_list[c[0]] > max_value: max_value = var_list[c[0]]
		if var_list[c[1]] > max_value: max_value = var_list[c[1]]
	print "max: ", max_value, '\n'

	counter = 0
	for i in xrange(n): #endre maks tre av varaiblene med hoyest forekomst til singletons
		if var_list[i] == max_value and len(state.nodes[i].domain) > 1:
			print 'index: ', i
			print "parent foer copy: ", state.nodes[i].domain
			new_dict = copy.deepcopy(state.nodes)
			new_dict[i].domain = [new_dict[i].domain[ random.randint(0, len(new_dict[i].domain)-1) ] ]
			print "new child: ", new_dict[i].domain
			print "parent etter copy: ", state.nodes[i].domain
			childs.append( State.State(new_dict) )
			childs[-1].set_assumption(i)
			print "parent heuristic: ", state.get_heuristic()
			print "child heuristic: ", childs[-1].get_heuristic(), "assumption: ", childs[-1].get_assumption() , '\n'
			counter += 1
			if counter == 3: 
				print '\n\n'
				return childs, max_value		

	return childs, max_value
#
def get_best_state(all_states):	#iterates and returns one state from the list with lowest heuristic
	for i in all_states:
		if all_states[i]: 
			return all_states[i][ random.randint(0, len(all_states[i])-1) ]
#
def create_GAC_constraint_queue(assumption, constraints, n):
	queue = deque()
	counter = 0
	for C in constraints:
		if C[0] == assumption:
			queue.append( [C[1], C] )
			counter += 1
			if counter == n: return queue
		elif C[1] == assumption:
			queue.append( [C[0], C] )
			counter += 1
			if counter == n: return queue
#
def Filter(state, queue):
	#iterate over q
	#run revice on all elements of q
		#everytime one changes state --> push new constraints on q
	#while queue:
	for qqq in xrange(1):
		constraint = queue.popleft()
		print "constraint: ", constraint
		#
		length_pre_revise = len(state.nodes[constraint[0]].domain)
		print "length_pre_revise: ", length_pre_revise
		#
		state.revice

	pass
#
def Astar(start_state, constraints):
	all_states = create_dictionary( start_state.get_heuristic() )#dict over alle states som ses paa. Nokkel er heurestikkverdier(heltall)
	print "dict laget: ", len(all_states), '\n'
	#
	all_states[start_state.get_heuristic()].append(start_state) #adding start_state into dictionary
	print "start state lagt inn i dict: ", all_states[start_state.get_heuristic()], '\n'
	#
	current_state = get_best_state(all_states)
	print "funnet beste state: ", current_state, '\n\n'
	#
	#while True:
	for xyz in xrange(1):
		#
		new_states, number_constarints = generate_child_states( get_best_state(all_states), constraints )
		print "new child states:", new_states, '\n\n'
		#
		all_states = add_states_to_dict( new_states, all_states )
		#
		###--- start printing ---###
		print "all_states med nye barn:"
		for n in xrange(len(all_states)):
			if len(all_states[n]) > 0:
				print n, all_states[n]
		print '\n\n'
		###--- end printing ---###
		#
		current_state = get_best_state(all_states)#Staten som analyseres naa er alltid current_state
		print "new best state: ",current_state, ", heuristic:", current_state.get_heuristic(), '\n'
		#
		queue = create_GAC_constraint_queue(current_state.get_assumption(), constraints, number_constarints)
		print "GAC queue: ", queue, '\n\n'
		#
		#Check whether new state is contrdictory, either in filtering loop or after it
		Filter(current_state, queue)
		#Check whether new state is contrdictory, either in filtering loop or after it

		current_state.set_heuristic( current_state.calculate_heuristic() )

		if current_state.get_heuristic() == 0: print True
		#else:

			#update the states position in all_states 
		
	pass


s, c = rf.read_graph("graph1.txt")

Astar(s, c)