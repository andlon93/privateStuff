# Read from file

# vertices edges


def createNode(index, x_pos, y_pos):
	print 'createnode: ' + index,x_pos,y_pos

def read_graph(path):
	f = open(path, 'r')

	vertices_and_edges =f.readline().split()
	vertices = int(vertices_and_edges[0])
	edges = int(vertices_and_edges[1])

	i=0
	while i < (vertices):
		temp = f.readline().split()
		createNode(temp[0],temp[1],temp[2])
		i    = i + 1

	constraints = []
	k=0
	while k<edges:
		temp2 = f.readline().split()
		constraints.append((temp2[0],temp2[1]))
		k     = k + 1



