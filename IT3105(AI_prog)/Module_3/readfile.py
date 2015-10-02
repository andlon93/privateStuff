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
	for i in range (rows_size):
		rows.append((f.readline().split()))
	for i in range (cols_size):
		cols.append((f.readline().split()))

	var_rows = []
	var_cols = []
	variable_rows = []
	variable_cols = []

	k = [None] * cols_size
	for i in range(cols_size):
		k[i] = Process(target=make_cols, args=(cols_size,rows_size,cols,i,qc,))
		k[i].start()
	for i in range(cols_size):
		variable_cols.append(qc.get())
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
	print "Threads done"

	variable_cols = bubble_sort(variable_cols)
	variable_rows = bubble_sort(variable_rows)

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
	#print "making cols"
	#variable_cols.append(Variable.Variable(False,i, cols[i], rows_size))
	#qc.cancel_join_thread()
	qc.put(Variable.Variable(False,i, cols[i], rows_size))
	return True

def make_rows(rows_size, cols_size,rows,i,qr):
	#print "making rows"
#	variable_rows.append( Variable.Variable(True,i, rows[i], cols_size) )
	#qr.cancel_join_thread()
	qr.put( Variable.Variable(True,i, rows[i], cols_size) )
	return True

def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	return cols_size,rows_size


if __name__ == '__main__':
	qc = Queue(maxsize=0)
	qr = Queue(maxsize=0)
	s = read_graph("nono-rabbit.txt",qc,qr)
	for rad in s.rows:
		print "DOmain: ",len(rad.domain)
