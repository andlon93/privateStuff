# Read from file
# vertices edges

import Node
import State
def read_graph(path):
	domain_size = 4 # Domain Size is now read from file
	#
	f = open(path, 'r')
	#
	domain_size = int(f.readline())
	print "domain size: ",domain_size

	vertices_and_edges =f.readline().split()#read number of vertices and edges
	vertices = int(vertices_and_edges[0])#number of vertices
	edges = int(vertices_and_edges[1])#number of edges
	#
	i=0 #iterate through all vertices and create Node objects of them
	Node_dict = {}
	while i < (vertices):
		temp = f.readline().split()
		node = Node.Node(int(temp[0]),temp[1],temp[2], domain_size)
		Node_dict[node.index] = node
		i = i + 1
	#Iterate through the constraints
	constraints = [] #indexes
	k=0
	while k < edges:
		temp2 = f.readline().split()
		constraints.append( (int(temp2[0]), int(temp2[1])) )
		k = k + 1
	#
	Start_State = State.State(Node_dict)
	return Start_State, constraints