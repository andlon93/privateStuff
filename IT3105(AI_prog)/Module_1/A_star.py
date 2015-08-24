import copy
debug = True
#debug = False
'''
O = empty
S = start
G = Goal
B = Barrier
'''

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
			column.append('O')
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
#board_size, start_node, goal_node, Barriers = user_input()

def create_board(board_size, start_node, goal_node, Barriers):
	board = create_empty_board(board_size)#create empty board

	board[ int(start_node[0]) ][ int(start_node[-1]) ] = 'S'#add start node marked 'S'
	board[ int(goal_node[0]) ][ int(goal_node[-1]) ] = 'G'#add goal node marked 'G'

	if debug:
		print '\n'
		print board_size
		for row in board:
			print row
		print '\n'
	add_Barriers(board, Barriers)
	return False

create_board(3, '0,0', '2,2', ['0,2,2,1'])