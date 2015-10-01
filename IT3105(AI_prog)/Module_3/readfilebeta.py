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



def read_graph(path,qc,qr):
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
	var_rows = []
	var_cols = []


	print "for process"
	k = Process(target=make_cols, args=(cols_size,rows_size,cols,i,qc))
	t = Process(target=make_rows, args=(rows_size,cols_size,rows,i,qr))
	print "Under process"
	k.start()
	t.start()
	print "etter process"
	t.join()
	k.join()

	variable_rows = []
	variable_cols = []
	for i in range(cols_size):
		variable_cols.append(qc.get())
	for i in range(rows_size):
		variable_rows.append(qr.get())

	variable_cols = bubble_sort(variable_cols)
	variable_rows = bubble_sort(variable_rows)

	for i in range(len(variable_cols)):
		print "index",variable_cols[i].index

	Start_state = State.State(variable_rows, variable_cols, None)

	print("--- %s seconds ---" % (time.time() - start_time))
	return Start_state

def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j].index > items[j+1].index:
                items[j], items[j+1] = items[j+1], items[j]
    return items

def make_cols(cols_size, rows_size,cols,i,qc):
	print "start making cols"
	for i in range(cols_size):
		print "making cols"
		qc.put((Variable.Variable(False,i, cols[i], rows_size)),True)
	return True

def make_rows(rows_size, cols_size,rows,i,qr):
	print "start making rows"
	for i in range(rows_size):
		print "making rows"
		qr.put(( Variable.Variable(True,i, rows[i], cols_size) ),True)
	return True

def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	return cols_size,rows_size

if __name__ == '__main__':
	print "GO"
	qc = Queue()
	qr = Queue()
	print "Queues done"
	s = read_graph("nono-cat.txt",qc,qr)
	print "done?"
	for rad in s.rows:
		print "DOmain: ",len(rad.domain)