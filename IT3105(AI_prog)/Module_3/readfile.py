# Read from file
# vertices edges

def read_graph(path):
	#
	f = open(path, 'r')
	#

	cols = []
	rows = []
	cols_and_rows_size =f.readline().split()
	cols_size = int(cols_and_rows_size[0])
	rows_size = int(cols_and_rows_size[1])
	for i in range (cols_size):
		cols.append((f.readline().split()))
	for i in range (rows_size):
		rows.append((f.readline().split()))
	return cols_size, rows_size, cols, rows

read_graph("nono-heart.txt")