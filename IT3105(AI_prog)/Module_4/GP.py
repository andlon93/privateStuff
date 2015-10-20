from __future__ import division	
import random
import State
import AlfaBeta as AB
import copy
import time
#
def create_random_weights(weights):
	mutate = []
	while 1: 
		t = random.randint(0, len(weights)-1)
		if t not in mutate:
			mutate.append(t)
		if len(mutate) == 2: break
	for n in mutate: weights[n] = weights[n]*random.uniform(0.75, 1.25)
	return weights
#
def main():
	weight = [0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1]
	#weight = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
	number_of_runs = 25
	weights = []
	#
	for n in xrange(5): 
		weights.append(create_random_weights(copy.deepcopy(weight)))
	#
	best = []
	second_best = []
	third_best = []
	fourth_best = []
	fifth_best = []
	while True:
		for w in weights:			
			n1024 = 0
			n2048_or_more = 0
			for n in xrange(1, number_of_runs+1):
				board = [[0,0,0,0],
			 			[0,0,0,0],
			 			[0,0,0,0],
			 			[0,0,0,0]]
				state = State.State(board)
				tempt_state = copy.deepcopy(state)
				tempt_state = AB.runAB(state, w)
				h = tempt_state.get_highest_tile()
				if h > 2047: n2048_or_more += 1
			#
			performance = n2048_or_more/number_of_runs
			if len(best) == 0:
				#print "best not set"
				best = [performance, w]
			elif len(second_best) == 0:
				#print "not second best set"
				if performance > best[0]:
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				else:
					second_best = [performance, w]
			elif len(third_best) == 0:
				if performance > best[0]:
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				elif performance > second_best[0]:
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [performance, w]
				else:
					third_best = [performance, w]
			elif len(fourth_best) == 0:
				if performance > best[0]:
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				elif performance > second_best[0]:
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [performance, w]
				elif performance > third_best[0]:
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [performance, w]
				else:
					fourth_best = [performance, w]
			elif len(fifth_best) == 0:
				if performance > best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				elif performance > second_best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [performance, w]
				elif performance > third_best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [performance, w]
				elif performance > fourth_best:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [performance, w]
				else:
					fifth_best = [performance, w]
			else:
				if performance > best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				elif performance > second_best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [performance, w]
				elif performance > third_best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [performance, w]
				elif performance > fourth_best[0]:
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [performance, w]
				elif performance > fifth_best[0]:
					fifth_best = [performance, w]
		#
		weights = []
		for n in xrange(3):
			weights.append(create_random_weights(copy.deepcopy(best[1])))
		for n in xrange(3):
			weights.append(create_random_weights(copy.deepcopy(second_best[1])))
		for n in xrange(2): 
			weights.append(create_random_weights(copy.deepcopy(third_best[1])))
		for n in xrange(1): 
			weights.append(create_random_weights(copy.deepcopy(fourth_best[1])))
		for n in xrange(1): 
			weights.append(create_random_weights(copy.deepcopy(fifth_best[1])))
		#
		print "\n\nBest: ", best[0], "of", number_of_runs
		print best[1], '\n'
		print "nest Best: ",second_best[0], "of", number_of_runs
		print second_best[1], '\n'
		print "Tredje Best: ", third_best[0], "of", number_of_runs
		print third_best[1], '\n'
		print "Fjerde Best: ", fourth_best[0], "of", number_of_runs
		print fourth_best[1], '\n'
		print "Femte Best: ", fifth_best[0], "of", number_of_runs
		print fifth_best[1], '\n\n'
#
main()