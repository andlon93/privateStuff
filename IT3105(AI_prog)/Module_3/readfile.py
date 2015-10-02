#!/usr/bin/python
# Read from file
# vertices edges
import Variable
import State

def read_graph(path):
	#
	f = open(path, 'r')
	# Lag "variabler med domener

	cols = []
	rows = []
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	for i in xrange (rows_size):
		rows.append((f.readline().split()))
	for i in xrange (cols_size):
		cols.append((f.readline().split()))

	variable_rows = []
	variable_cols = []
	for i in xrange (rows_size):
		variable_rows.append( Variable.Variable(True, i, rows[i], cols_size) )
	for i in xrange (cols_size):
		variable_cols.append( Variable.Variable(False, i, cols[i],rows_size) )
	Start_state = State.State(variable_rows, variable_cols, None)
	return Start_state

def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	return cols_size,rows_size

s = read_graph("nono-rabbit.txt")
for row in s.rows:
	print len(row.domain)
