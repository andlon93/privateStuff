import readfile as rf
import State
import random
#import collections as c
#all_states = collections.OrderedDict(sorted(all_states.items()))



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
def generate_child_states(state):
	#update childstates with assumption
	var_list = range()
	return s
#
def get_best_state(all_states):	#iterates and returns one state from the list with lowest heuristic
	for index in all_states:
		if all_states[index]: return all_states[index][ random.randint(0, len(all_states[index])-1) ]
#
def create_GAC_constraint_queue(assumption, constraints):
	queue = []
	#create queue of all constraints with assuption variable in it
	# every element of queue == [var som ikke er assumption, constraints[n] ]
	return queue
#
def Filter(s, q):
	#iterate over q
	#run revice on all elements of q
		#everytime one changes state --> push new constraints on q

	pass
#

#
def Astar(start_state, constraints):
	all_states = create_dictionary( start_state.get_heuristic() )#dict over alle states som ses paa. Nokkel er heurestikkverdier(heltall)
	print "dict laget: ", len(all_states), '\n'
	
	all_states[start_state.get_heuristic()].append(start_state) #adding start_state into dictionary
	print "start state lagt inn i dict: ", all_states[start_state.get_heuristic()], '\n'
	
	current_state = get_best_state(all_states)
	print "funnet beste state: ", current_state, '\n'
	


	while True:
		new_states = generate_child_states( get_best_state(all_states), constraints )
		all_states = add_states_to_dict( new_states, all_states )

		current_state = get_best_state(all_states)#Staten som analyseres naa er alltid current_state
		

		queue = create_GAC_constraint_queue(current_state.get_assumption(), constraints)

		#Check whether new state is contrdictory, either in filtering loop or after it
		Filter(current_state, queue)
		#Check whether new state is contrdictory, either in filtering loop or after it

		current_state.set_heuristic( current_state.calculate_heuristic() )

		if current_state.get_heuristic() == 0: print True
		#else:

			#update the states position in all_states 
		


		pass
	pass


s, c = rf.read_graph("graph1.txt")

Astar(s, c)
