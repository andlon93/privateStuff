# Read from file
# vertices edges

def read_graph(path):
	#
	f = open(path, 'r')
	# Lag "variabler med domener

	cols = []
	rows = []
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	for i in range (cols_size):
		cols.append((f.readline().split()))
	for i in range (rows_size):
		rows.append((f.readline().split()))
	variable_rows = []
	variable_cols = []
	for i in range (cols_size):
		variable_cols.append( Variable.Variable(False, i, cols[i],rows_size) )
		print ( (False, i, cols[i],rows_size) )
	for i in range (rows_size):
		variable_rows.append( Variable.Variable(True, i, rows[i], cols_size) )
		print ( (True, i, cols[i],rows_size) )
	Start_state = State.State(variable_rows,variable_cols)
	return Start_state

def getSizes(path): #Just for GUI debug
	f = open(path, 'r')
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	return cols_size,rows_size


read_graph("nono-chick.txt")