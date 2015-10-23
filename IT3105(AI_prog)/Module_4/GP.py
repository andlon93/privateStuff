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
	for n in mutate: weights[n] = weights[n]*random.uniform(0.5, 1.5)
	return weights
#

def run_calculation(weight, queue2):
	'''try:
		sys.getwindowsversion() # Check if OS = Windows
	except:
		isWindows = False
	else:
		isWindows = True
	if isWindows:
		import win32api,win32process,win32con
        pid = win32api.GetCurrentProcessId()
        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
        win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS) # Set process-priority'''
	board = [[0,0,0,0],
		 	[0,0,0,0],
		 	[0,0,0,0],
		 	[0,0,0,0]]
	state = State.State(board)
	tempt_state = copy.deepcopy(state)
	tempt_state = AB.runAB(state, weight)
	h = tempt_state.get_highest_tile()
	if h > 2047:
		queue2.put(1)
	else:
		queue2.put(0)

def run_calculations(weight, queue, number_of_runs): # This method takes a set of weights, runs the game for number_of_runs, puts performance in queue
	print "Spawning processes *",number_of_runs
	queue2 = Queue(maxsize=0)
	n2048_or_more = 0
	sub_process = [None] * number_of_runs
	for n in range (number_of_runs):
		sub_process[n] = Process(target=run_calculation, args=(weight, queue2))
		sub_process[n].start()
	for n in range (number_of_runs):
		entry = queue2.get()
		if entry == 1:
			n2048_or_more += 1
	for n in range (number_of_runs):
		sub_process[n].join()
	performance = n2048_or_more/number_of_runs # Calculate a percentage
	temp_object = [performance,weight]
	queue.put(temp_object) # Puts the Performance, and weights used, in the Queue. This is retrieved when all processes are done

def main():
	print "inside main()"
	'''try:
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
    except:
		isWindows = False'''
	queue = Queue(maxsize=0)
	#weight = [0.5, 0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.1, 0.05]
	#weight = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
	weight = [0.39, 0.042, 0.045, 0.053, 0.05, 0.054, 0.124, 0.12, 0.05, 0.025]
	number_of_runs = 30
	weights = []
	performances = []
	#
	for n in xrange(5): #TODO change back to in xrange(5)
		weights.append(create_random_weights(copy.deepcopy(weight)))
	#
	best = []
	second_best = []
	third_best = []
	fourth_best = []
	fifth_best = []
	count = 0
	while True:
		print "Run number: ", count + 1
		count += 1
		process = [None] * len(weights)
		for w in xrange(len(weights)):
			process[w] = Process(target=run_calculations, args=(weights[w], queue, number_of_runs))
			process[w].start()
			performances.append(queue.get())
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
				if entry == best:
					continue
				if performance > best[0]:
					second_best = [copy.deepcopy(best[0]), copy.deepcopy(best[1])]
					best = [performance, w]
				else:
					second_best = [performance, w]
			elif len(third_best) == 0:
				if entry == best:
					continue
				if entry == second_best:
					continue
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
				if entry == best:
					continue
				if entry == second_best:
					continue
				if entry == third_best:
					continue
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
				if entry == best:
					continue
				if entry == second_best:
					continue
				if entry == third_best:
					continue
				if entry == fourth_best:
					continue
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
					if entry == best:
						continue
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [copy.deepcopy(second_best[0]), copy.deepcopy(second_best[1])]
					second_best = [performance, w]
				elif performance > third_best[0]:
					if entry == best:
						continue
					if entry == second_best:
						continue
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [copy.deepcopy(third_best[0]), copy.deepcopy(third_best[1])]
					third_best = [performance, w]
				elif performance > fourth_best[0]:
					if entry == best:
						continue
					if entry == second_best:
						continue
					if entry == third_best:
						continue
					fifth_best = [copy.deepcopy(fourth_best[0]), copy.deepcopy(fourth_best[1])]
					fourth_best = [performance, w]
				elif performance > fifth_best[0]:
					if entry == best:
						continue
					if entry == second_best:
						continue
					if entry == third_best:
						continue
					if entry == fourth_best:
						continue
					fifth_best = [performance, w]
		#
		weights = []
		for n in xrange(3):
			weights.append(create_random_weights(copy.deepcopy(best[1])))
		for n in xrange(2):
			weights.append(create_random_weights(copy.deepcopy(second_best[1])))
		for n in xrange(1):
			weights.append(create_random_weights(copy.deepcopy(third_best[1])))
		for n in xrange(1):
			weights.append(create_random_weights(copy.deepcopy(fourth_best[1])))
		for n in xrange(1):
			weights.append(create_random_weights(copy.deepcopy(fifth_best[1])))
		#
		###--- START Wrte data to file ---###
		fil = open("output.txt", 'w')
		streng1 = "Best: "+str(best[0])+" of "+str(number_of_runs)+"\n"+str(best[1])+"\n"
		streng2 = "Nest Best: "+str(second_best[0])+" of "+str(number_of_runs)+"\n"+str(second_best[1])+"\n"
		streng3 = "Tredje Best: "+str(third_best[0])+" of "+str(number_of_runs)+"\n"+str(third_best[1])+"\n"
		streng4 = "Fjerde Best: "+str(fourth_best[0])+" of "+str(number_of_runs)+"\n"+str(fourth_best[1])+"\n"
		streng5 = "Femte Best: "+str(fifth_best[0])+" of "+str(number_of_runs)+"\n"+str(fifth_best[1])+"\n"
		full_streng = streng1+"\n\n"+streng2+"\n\n"+streng3+"\n\n"+streng4+"\n\n"+streng5
		fil.write(full_streng)
		fil.close()
		###--- END Wrte data to file ---###
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
if __name__ == '__main__':
	print "GP running"
	main()
