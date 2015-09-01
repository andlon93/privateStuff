import copy
debug = False
#########---- Letters from the print ----########
'''
C = Closed
S = start
G = Goal
B = Barrier
P = path
O = Open
'''
#########---- Example sets ----########
#        row  col start    goal    Barriers
set_0 = [ 10, 10, [0,0],  [9,9],   [[2,3,5,5], [8,8,2,1]] 										   ]		
set_1 = [ 20, 20, [19,3], [2,18],  [[5,5,10,10], [1,2,4,1]] 									   ]
set_2 = [ 20, 20, [0,0],  [19,19], [[17,10,2,1], [14,4,5,2], [3,16,10,2], [13,7,5,3], [15,15,3,3]] ]
set_3 = [ 10, 10, [0,0],  [9,5],   [[3,0,2,7], [6,0,4,4], [6, 6, 2, 4]] 						   ]
set_4 = [ 10, 10, [0,0],  [9,9],   [[3,0,2,7], [6,0,4,4], [6, 6, 2, 4]] 						   ]
set_5 = [ 20, 20, [0,0],  [19,13], [[4,0,4,16], [12,4,2,16], [16,8,4,4]] 						   ]

#########---- Node Class ----########
class Node:
    children = None 
    typ = None
    parent = None
    x_pos = None
    y_pos = None
    #-- For A* --#
    g = None
    h = None
    def __init__(self):
        self.children = []

#########---- Print board methods ----########
def print_board(board):#prints board with 0,0 in bottom left corner  #Also generates a html file with the table
	htmlString='<head><link rel="stylesheet" type="text/css" href="theme.css"></head><table><body>'
	for row in range (len(board), 0, -1):
		htmlString = htmlString + "<tr>"
		for i in range (len(board[row-1])):
			if board[row-1][i]=="O":
				htmlString = htmlString + '<td class="O">' + board[row-1][i] + "</td>"
			elif board[row-1][i]=="G":
				htmlString = htmlString + '<td class="G">' + board[row-1][i] + "</td>"
			elif board[row-1][i]=="B":
				htmlString = htmlString + '<td class="B">' + board[row-1][i] + "</td>"
			elif board[row-1][i]=="S":
				htmlString = htmlString + '<td class="S">' + board[row-1][i] + "</td>"
			elif board[row-1][i]=="-":
				htmlString = htmlString + '<td class="-">' + board[row-1][i] + "</td>"
			elif board[row-1][i]=="P":
				htmlString = htmlString + '<td class="P">' + board[row-1][i] + "</td>"
			else:
				htmlString = htmlString + '<td>' + board[row-1][i] + "</td>"
		print board[row-1], '\n'
		htmlString = htmlString + "</tr>"
	htmlString = htmlString + "</table></body>"
	f = open('output.html','w')
	f.write(htmlString)
	f.close()

def update_board_cell(node, board, letter):
	x = node.x_pos
	y = node.y_pos
	board[x][y] = letter
	return board

def update_board_with_path(board, path):
	for cell in path:
		if board[cell.x_pos][cell.y_pos] != 'S' and board[cell.x_pos][cell.y_pos] != 'G': 
			board[cell.x_pos][cell.y_pos] = 'P'
	return board
	
#########---- Take input from user ----########
def user_input(): #get all input from user
	rows = int( raw_input("Height of board: ") )	#Board size
	cols = int( raw_input("Width of board: ") )	    #Board size
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
	return rows, cols, start_node, goal_node, Barriers

#########---- Create board ----########
def create_empty_board(rows, cols):#Initialaise an empty board
	board = []

	for row in xrange(0, rows):
		column = []
		for col in xrange(0, cols):
			column.append('-')
		board.append( column )


	return board
def add_Barriers(board, Barriers):#Add barreiers to the board
	for Barrier in Barriers:
		if debug: print Barrier
		#Position of lower left point in barrier

		x = int( Barrier[0] )
		y = int( Barrier[1] )
		#width and height of barrier(minimun 1)
		width = int( Barrier[2] )
		height = int( Barrier[3] )
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
def create_board(rows, cols, start_node, goal_node, Barriers):#Creates board using help functions
	board = create_empty_board(rows, cols)#create empty board
	board[ start_node[0] ][ start_node[1] ] = 'S'#add start node marked 'S'
	board[ goal_node[0] ][ goal_node[1] ] = 'G'#add goal node marked 'G'
	board = add_Barriers(board, Barriers)#add the barriers to the board
	
	if debug:
		print '\n'
		print "Rows: ", rows, "columns: ", cols
		for row in board:
			print row
		print '\n'
	
	return board
#b = create_board( set_0[0], set_0[1], set_0[2], set_0[3], set_0[4] )
#print_board(b)
#########---- Create the nodes ----########
def create_linked_classes(board):
	class_board = []#matrix with each node as an object
	#fill in objects where there is not a B
	for row in xrange(0, len(board)):
		row_list = []
		for col in xrange(0, len(board[row])):
			if board[row][col] != 'B':
				node = Node()
				node.typ = board[row][col]
				node.x_pos = row
				node.y_pos = col
				row_list.append(node)
				if board[row][col] == 'S':
					rot = node
				if board[row][col] == 'G':
					goal = node
				#if node != rot:
				#node.parent = 
			else:
				row_list.append('B')
		class_board.append(row_list)
	#
	#Fill in child lists on all nodes
	##################################print "zzzz:  ", len(class_board)
	for row in xrange(0, len(class_board)):
		##################################print "xxxx:  ", len(class_board[row])
		for col in xrange(0, len(class_board[row])):
			if class_board[row][col] != 'B':

				'''if debug: print 'node: ', class_board[row][col], '\n'''
				if row+1 < len(class_board) and class_board[row+1][col] != 'B':
					class_board[row][col].children.append( class_board[row+1][col] )#add child nodes
					class_board[row+1][col].parent = class_board[row][col]#add parent
				if col+1 < len(class_board[row]) and class_board[row][col+1] != 'B':
					class_board[row][col].children.append( class_board[row][col+1] )#add child nodes
					class_board[row][col+1].parent = class_board[row][col] #add parent
	#
	if debug: 
		print "children: ", rot.children, '\n'
		print "rot", rot, 'pos: ', rot.x_pos, rot.y_pos
		print "parent: ", rot.children[0].parent, '\n'
		print "goal: ", goal.typ
	return rot, goal, class_board

#########---- BFS ----########
def Breadth_first_search(board, start_node, goal_node):
	queue = [[start_node]]
	visited = set()

	while queue:
		path = queue.pop(0)

		current_node = path[-1]

		if current_node == goal_node:
			return path
		elif current_node not in visited:
			for child in current_node.children:
				temp_path = list(path)
				#print 'temp_path: ', temp_path
				temp_path.append(child)
				#print 'temp_path 2.0: ', temp_path
				queue.append(temp_path)
				#print 'queue: ', queue

			visited.add(current_node)
		#print '------------New iteration---------------'

#########---- DFS ----########			
def Depth_first_search(board, start_node):
	stack = []
	current = start_node

	while True:
		if current.typ == 'G':
			return board
		if len(current.children) > 0:
			stack.append(current)
			current = current.children.pop()#go down one level if possible
			if current.typ != 'G': board = update_board_cell(current, board, 'P')#update board cell
		else:
			current = stack.pop()#go up level if bottom level is reached
			update_board_cell(current, board, 'O')#update board cell
		pass
	pass

#########---- A* ----########
def Heuristic():

	pass
def Astar(board, start_node, end_node):

	pass


#board_size, start_node, goal_node, Barriers = user_input()
#create_board(board_size, start_node, goal_node, Barriers)
#board = create_board(10, '0,0', '9,9', ['2,3,5,5', '8,8,2,1'])
	
#board = create_board(3, 4, [0,0], [2,2], [[0,1,2,2]])
board = create_board( set_0[0], set_0[1], set_0[2], set_0[3], set_0[4] )
#print_board(board)
rot, goal_node ,class_board = create_linked_classes(board)

#print_board(board)
#print '\n\n'
path = Breadth_first_search(board, rot, goal_node)



board = update_board_with_path(board, path)
#DFS_board = Depth_first_search(board, rot)
print_board(board)
#print '\n\n'
