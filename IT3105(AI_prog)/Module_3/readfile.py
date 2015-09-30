#!/usr/bin/python
# Read from file
# vertices edges
import Variable
from threading import *
from multiprocessing import Process
import time

import State
variable_rows = []
variable_cols = []

cols_size = None
rows_size = None
k = None
t = None



def read_graph(path):
	start_time = time.time()
	#
	f = open(path, 'r')
	# Lag "variabler med domener

	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	cols = []
	rows = []
	for i in range (cols_size):
		cols.append((f.readline().split()))
	for i in range (rows_size):
		rows.append((f.readline().split()))


	# pool = Pool(processes=4)
	# r2 = pool.apply_async(make_rows(rows_size, cols_size))
	# r1 = pool.apply_async(make_cols(cols_size, rows_size))
	# print "her?"
	# a1 = r1.get()
	# a2 = r2.get()
	k = [None] * cols_size
	for i in range(cols_size):
		k[i] = Process(target=make_cols, args=(cols_size,rows_size,cols,i))
		k[i].start()

	for i in range (cols_size):
		k[i].join()

	t = [None] * rows_size
	for i in range(rows_size):
		t[i] = Process(target=make_rows, args=(rows_size,cols_size,rows,i))
		t[i].start()



	for i in range (rows_size):
		t[i].join()

	Start_state = State.State(variable_rows, variable_cols, None)
	print("--- %s seconds ---" % (time.time() - start_time))
	return Start_state

def make_cols(cols_size, rows_size,cols,i):
	print "making cols"
	variable_cols.append(Variable.Variable(False,i, cols[i], rows_size))
	return True

def make_rows(rows_size, cols_size,rows,i):
	print "making rows"
	variable_rows.append( Variable.Variable(True,i, rows[i], cols_size) )
	return True



def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	return cols_size,rows_size


if __name__ == '__main__':
    s = read_graph("nono-rabbit.txt")