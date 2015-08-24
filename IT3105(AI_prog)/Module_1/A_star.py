import copy
debug = True
#debug = False
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



#board_size, start_node, goal_node, Barriers = user_input()

def create_board(board_size, start_node, goal_node, Barriers):
	board = create_empty_board(board_size)


	board[ int(start_node[0]) ][ int(start_node[-1]) ] = 'S'
	board[ int(goal_node[0]) ][ int(goal_node[-1]) ] = 'G'

	if debug:
		print '\n'
		print board_size
		for row in board:
			print row
		print '\n'

create_board(10, '0,0', '9,9', '2,2,2,2')