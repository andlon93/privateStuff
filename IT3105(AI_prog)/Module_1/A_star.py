import copy
debug = False
'''
O = empty
S = start
G = Goal
B = Barrier
'''
def print_board(board):#prints board with 0,0 in bottom left corner
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

#board_size, start_node, goal_node, Barriers = user_input()
#create_board(board_size, start_node, goal_node, Barriers)
board = create_board(10, '0,0', '9,9', ['2,3,5,5', '8,8,2,1'])

print_board(board)
def Breadth_first_search(board):
	pass