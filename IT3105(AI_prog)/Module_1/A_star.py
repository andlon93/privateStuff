def user_input():
	board_size = int( raw_input("Breadth and width of board: ") )	#Board size
	#start and end nodes
	start_node = str( raw_input("position of start node(x,y): ") )
	goal_node = str( raw_input("position of goal node(x,y): ") )
	#Barriers
	Barriers = []
	num_of_barriers = int( raw_input("Number of barriers: ") )
	for n in xrange(0, num_of_barriers):
		Barriers.append( raw_input("Enter barrier(x-left,y-bottom,width,height): ") )

	print board_size
	print start_node, goal_node
	print Barriers

user_input()