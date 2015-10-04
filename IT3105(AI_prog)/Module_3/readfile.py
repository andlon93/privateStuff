#!/usr/bin/python
# Read from file
# vertices edges
import Variable
from threading import *
from multiprocessing import Process, Queue
import time
import State
from functools import partial

cols_size = None
rows_size = None
k = None
t = None

def read_graph(path):
	qc = Queue(maxsize=0) #Queues are used to retrieve data from spawned subprocesses
	qr = Queue(maxsize=0) #Queues are used to retrieve data from spawned subprocesses
	start_time = time.time()
	f = open(path, 'r')

	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0]) #Number of colums
	rows_size = int(cols_and_rows_size[1]) #Number of rows

	cols = [] #List to hold lists of constraints per column
	rows = [] #List to hold lists of constraints per row
	for i in range (rows_size):
		rows.append((f.readline().split()))
	rows = list(reversed(rows)) # Reversing because rows are read from bottom up in the file Index 0 will now be the most upper row

	for i in range (cols_size):
		cols.append((f.readline().split()))

	f.close() # Closing the open file

	var_rows = []
	var_cols = []
	variable_rows = []
	variable_cols = []

	# These lines spawn a process per column(k), and row (t), and generates all possible domains
	k = [None] * cols_size
	for i in range(cols_size):
		k[i] = Process(target=make_cols, args=(cols_size,rows_size,cols,i,qc,))
		k[i].start()
	for i in range(cols_size):
		variable_cols.append(qc.get()) # Subprocesses put the computed row/column in the Queue (qr/qc), and the main process retrieves them here
	for i in range (cols_size):
		k[i].join()

	t = [None] * rows_size
	for i in range(rows_size):
		t[i] = Process(target=make_rows, args=(rows_size,cols_size,rows,i,qr,))
		t[i].start()
	for i in range(rows_size):
		variable_rows.append(qr.get())
	for i in range (rows_size):
		t[i].join()

	variable_cols = bubble_sort(variable_cols)	# Because the processes don't always finish in the correct order, the lists are sorted here
	variable_rows = bubble_sort(variable_rows)

	Start_state = State.State(variable_rows, variable_cols, None)
	print ""
	print("--- Domains generated in %s seconds ---" % (time.time() - start_time))
	return Start_state

def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j].index > items[j+1].index:
                items[j], items[j+1] = items[j+1], items[j]
    return items

def make_cols(cols_size, rows_size,cols,i,qc):
	qc.put(Variable.Variable(False,i, cols[i], rows_size))
	return True

def make_rows(rows_size, cols_size,rows,i,qr):
	qr.put( Variable.Variable(True,i, rows[i], cols_size) )
	return True

def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	f.close()
	return cols_size,rows_size


if __name__ == '__main__':
	s = read_graph("nono-rabbit.txt")
	# for rad in s.rows:
	# 	print "DOmain: ",len(rad.domain)
