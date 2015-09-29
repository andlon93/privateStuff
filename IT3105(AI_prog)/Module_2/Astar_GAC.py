import readfile as rf
import copy
import State
import time
import random
from collections import deque
#
algorithm_delay = 0
#
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
def generate_child_states2(state, constraints):
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
	if len(state.nodes[c[0]].domain) < 2:
		return len(state.nodes[c[0]].domain)
	elif c[0] == c[1][0] and len(state.nodes[c[1][1]].domain) == 1:
		check_node = state.nodes[c[1][1]].domain[0]
	elif c[0] == c[1][1] and len(state.nodes[c[1][0]].domain) == 1:
		check_node = state.nodes[c[1][0]].domain[0]
	else:
		return len(state.nodes[c[0]].domain)
	#
	for change_node in state.nodes[c[0]].domain:
		if change_node == check_node:
			state.nodes[c[0]].domain.remove(change_node)
			#print "changed node: ", state.nodes[c[0]].domain, "new len", len(state.nodes[c[0]].domain)
			return len(state.nodes[c[0]].domain)
	#
	return len(state.nodes[c[0]].domain)
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
	while queue:
		constraint = queue.popleft()#popper constraint fra ko
		length_pre_revise = len(state.nodes[constraint[0]].domain)
		length_post_revice = revice2(state, constraint)#kjorer revice paa constrainten som ble poppet
		if length_pre_revise > length_post_revice:#hvis domenet har blitt forkortet maa nye constarints inn i ko
			queue.extend( extend_queue(constraint[0], constraints) )
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
	print "Calculating..."
	start_time = time.time()
	if show_gui:
		import gui
	all_states = create_dictionary(start_state.get_heuristic())
	#
	start_state.set_assumption([0, 0])
	start_state.nodes[0].domain = [0]
	queue = create_GAC_constraint_queue(start_state.get_assumption()[0], constraints)
	Filter(start_state, queue, constraints)
	start_state.set_heuristic( start_state.calculate_heuristic() )
	all_states[start_state.get_heuristic()].append(start_state)
	#
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
				else:
					parent.nodes[new_state.get_assumption()[0]].domain.remove(new_state.get_assumption()[1])
			#
			if is_valid_state(parent, constraints):
				parent.set_heuristic(parent.calculate_heuristic())
				all_states[parent.get_heuristic()].append(parent)
			#
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
			#
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
#
show_gui = True
def run(delay):
	if not show_gui:
		s, c = rf.read_graph("graph6.txt")
		Astar(s, c)
	else:
		algorithm_delay = delay
