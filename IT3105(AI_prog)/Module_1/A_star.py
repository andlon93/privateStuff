import copy
debug = True
'''
C = Closed
S = start
G = Goal
B = Barrier
P = path
O = Open
'''
class Node:
    children = None 
    typ = None
    parent = None

    def __init__(self):
        self.children = []


def print_board(board):#prints board with 0,0 in bottom left corner
	board = [] 
	for row in range (len(board), 0, -1):
		print board[row-1], '\n'

def user_input(): #get all input from user
	board_size = int( raw_input("Breadth and width of board: ") )	#Board size
	#start and end nodes
	start_node = str( raw_input("position of start node(x,y): ") )
	goal_node = str( raw_input("position of goal node(x,y): ") )
	#Barriers
	Barriers = []
	num_of_barriers = int( raw_input("Number of barriers: ") )
	for n in xrange(0, num_of_barriers):
		Barriers.append( raw_input("Enter barrier(x-left,y-bottom,width,height): ") )

	if debug:
		print "board_size: ", board_size
		print "start_node, goal_node: ", start_node, goal_node
		print "Barriers: ", Barriers
		print '\n'
	return board_size, start_node, goal_node, Barriers

def create_empty_board(board_size):#Initialaise an empty board
	board = []

	for row in xrange(0, board_size):
		column = []
		for col in xrange(0, board_size):
			column.append('C')
		board.append( column )


	return board

def add_Barriers(board, Barriers):#Add barreiers to the board
	for Barrier in Barriers:
		if debug: print Barrier
		#Position of lower left point in barrier
		x = int( Barrier[0] )
		y = int( Barrier[2] )
		#width and height of barrier(minimun 1)
		width = int( Barrier[4] )
		height = int( Barrier[6] )
		if debug: print 'x: ', x, 'y: ', y, 'width: ', width, 'height: ', height, '\n'

		for h in xrange(0, height):#adding the barriers to the board with mark 'B'
			for w in xrange(0, width):
				board[y+h][x+w] = 'B'
	if debug:
		print '\n'
		for row in board:
			print row
		print '\n'
	return board	

def create_board(board_size, start_node, goal_node, Barriers):#Creates board using help functions
	board = create_empty_board(board_size)#create empty board
	board[ int(start_node[0]) ][ int(start_node[-1]) ] = 'S'#add start node marked 'S'
	board[ int(goal_node[0]) ][ int(goal_node[-1]) ] = 'G'#add goal node marked 'G'
	board = add_Barriers(board, Barriers)#add the barriers to the board
	
	if debug:
		print '\n'
		print board_size
		for row in board:
			print row
		print '\n'
	
	return board

def create_linked_classes(board):
	class_board = []#matrix with each node as an object
	#fill in objects where there is not a B
	for row in xrange(0, len(board)):
		row_list = []
		for col in xrange(0, len(board)):
			if board[row][col] != 'B':
				node = Node()
				node.typ = board[row][col]
				row_list.append(node)
				if board[row][col] == 'S':
					rot = node
				#if node != rot:
				#	node.parent = 
			else:
				row_list.append('B')
		class_board.append(row_list)
	#
	#Fill in child lists on all nodes
	for row in xrange(0, len(class_board)):
		for col in xrange(0, len(class_board[row])):
			if class_board[row][col] != 'B':

				'''if debug: print 'node: ', class_board[row][col], '\n'''
				if row+1 < len(class_board[row]) and class_board[row+1][col] != 'B':
					class_board[row][col].children.append( class_board[row+1][col] )#add child nodes
					class_board[row+1][col].parent = class_board[row][col]#add parent
				if col+1 < len(class_board[row]) and class_board[row][col+1] != 'B':
					class_board[row][col].children.append( class_board[row][col+1] )#add child nodes
					class_board[row][col+1].parent = class_board[row][col] #add parent
	#
	if debug: 
		print "children: ", rot.children, '\n'
		print "rot", rot
		print "parent: ", rot.children[0].parent, '\n'
	return rot, class_board

def Breadth_first_search(board, start_node):
	queue = [start_node]
	while len(queue) != 0:
		current = queue.pop(0)
		if current.typ == 'G':
			while current.typ != 'S':
				if current != 'G': current.typ = 'P'
				current = current.parent
				return True
		for n in range(0, len(current.children)): 
			queue.append(current.children[n])


#board_size, start_node, goal_node, Barriers = user_input()
#create_board(board_size, start_node, goal_node, Barriers)
#board = create_board(10, '0,0', '9,9', ['2,3,5,5', '8,8,2,1'])
board = create_board(3, '0,0', '2,2', ['0,1,2,2'])
rot, class_board = create_linked_classes(board)


Breadth_first_search(board, rot)
