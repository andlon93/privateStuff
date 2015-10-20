from __future__ import division
from multiprocessing import Process, Queue
import random
import State
import AlfaBeta as AB
import copy
import time
import sys
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
def run_calculations(weight, queue, number_of_runs): # This method takes a set of weights, and runs the game for number_of_runs
	n2048_or_more = 0
	for n in range (number_of_runs):
		board = [[0,0,0,0],
			 	[0,0,0,0],
			 	[0,0,0,0],
			 	[0,0,0,0]]
		state = State.State(board)
		tempt_state = copy.deepcopy(state)
		tempt_state = AB.runAB(state, weight)
		h = tempt_state.get_highest_tile()
		if h > 2047: n2048_or_more += 1 # Count the times 1024 or better was achieved
	performance = n2048_or_more/number_of_runs # Calculate a percentage
	temp_object = [performance,weight]
	queue.put(temp_object) # Puts the Performance, and weights used, in the Queue. This is retrieved when all processes are done

def main():
	try:
		sys.getwindowsversion() # Check if OS = Windows
	except:
		isWindows = False
	else:
		isWindows = True
	if isWindows:
		import win32api,win32process,win32con
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS) # Set process-priority

	queue = Queue(maxsize=0)
	weight = [0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1, 0.05]
	#weight = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
	number_of_runs = 2
	weights = []
	performances = []
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
		'''
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
		'''
		process = [None] * len(weights)
		for w in xrange(len(weights)):
			process[w] = Process(target=run_calculations, args=(weights[w], queue, number_of_runs))
			process[w].start()
		for w in xrange(len(weights)):
			performances.append(queue.get())
		for w in xrange(len(weights)):
			process[w].join()
		for entry in performances:
			performance = entry[0]
			w = entry[1]
			#
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
		print "Start-Weights:  [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]"
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
if __name__ == '__main__':
	main()
