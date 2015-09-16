from threading import Thread, Lock
import Tkinter as tk
from Tkinter import *
import time
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
set_5 = [ 20, 20, [0,0],  [19,13], [[4,0,4,16], [12,4,2,16], [16,8,4,4]]						   ]
set_6 = [ 100, 100, [0,0],  [99,99], [[4,4,40,50], [45,45,54,40], [44,4,45,3], [89,4,2,30], [4,44,3,50],[90, 50, 9, 50]] 						   ]

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
    f = None
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
		#print board[row-1], '\n'
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

def update_board_with_path(board, rot, goal_node, path):
	for cell in path:
		board[cell.x_pos][cell.y_pos] = 'P'
	board[rot.x_pos][rot.y_pos] = 'S'
	board[goal_node.x_pos][goal_node.y_pos] = 'G'
	return board

def draw_GUI(board):
	reverse_board = []
	for n in xrange( len(board)-1, -1, -1):
			reverse_board.append(board[n])
	for n in xrange(0, len(reverse_board)):
		for i in xrange(0, len(reverse_board[n])):
			#Label(text=reverse_board[n][i], width=5).grid(row=n, column=i)
			if reverse_board[n][i] == '-': Entry( bg="lavender", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'O': Entry(bg="blue", width=4).grid_configure(row=n, column=i)
			elif reverse_board[n][i] == 'B': Entry( bg="black", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'S': Entry( bg="yellow", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'P': Entry( bg="sky blue", width=4 ).grid(row=n, column=i)
			else: Entry( bg="green", width=4 ).grid(row=n, column=i)
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
		if debug: print 'x:', x, ' y:', y, ' width:', width, ' height:', height, '\n'
		#print "Goalnode: ", board[19][13]

		for h in xrange(0, height):#adding the barriers to the board with mark 'B'
			for w in xrange(0, width):
				#print "Y:",y+h, " X:",x+w
				board[y+h][x+w] = 'B'
	if debug:
		print '\n'
		for row in board:
			print row
		print '\n'
	return board	
def create_board(rows, cols, start_node, goal_node, Barriers):#Creates board using help functions
	board = create_empty_board(rows, cols)#create empty board
	board[ start_node[1] ][ start_node[0] ] = 'S'#add start node marked 'S'
	board[ goal_node[1] ][ goal_node[0] ] = 'G'#add goal node marked 'G'
	board = add_Barriers(board, Barriers)#add the barriers to the board
	
	if debug:
		print '\n'
		print "Rows: ", rows, "columns: ", cols
		for row in board:
			print row
		print '\n'
	#print_board(board)
	
	return board
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
				if row-1 > -1 and class_board[row-1][col] != 'B':
					class_board[row][col].children.append( class_board[row-1][col] )#add child nodes
					class_board[row-1][col].parent = class_board[row][col]#add parent
				
				if col-1 > -1 and class_board[row][col-1] != 'B':
					class_board[row][col].children.append( class_board[row][col-1] )#add child nodes
					class_board[row][col-1].parent = class_board[row][col]#add parent
				
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
	print "BFS start"
	queue = [[start_node]]
	visited = set()
	iterations = []
	#
	while queue:
		path = queue.pop(0)

		current_node = path[-1]
		#print "current_node:", current_node.x_pos, current_node.y_pos
		#board[current_node.x_pos][current_node.y_pos] = 'O'
		#
		if current_node == goal_node:
			#print "GGGGOOOOAAAAALLLL"
			return path, iterations
		elif current_node not in visited:
			if current_node != rot and current_node != goal_node:
				iterations.append( [current_node.x_pos, current_node.y_pos, 'O'] )
			for child in current_node.children:
				temp_path = list(path)
				#print 'temp_path: ', temp_path
				temp_path.append(child)
				#print 'temp_path 2.0: ', temp_path
				queue.append(temp_path)
				#print 'queue: ', queue
				#
			visited.add(current_node)
		#time.sleep(0.1)
			#print len(visited)
			#print '------------New iteration---------------'
#
#########---- DFS ----########			
def Depth_first_search(board, start_node):
	stack = []
	current = start_node
	visited = set()
	path = []
	#
	while True:
		if current.typ == 'G': return board
		#
		if current.children and current not in visited:
			stack.append(current)
			current = current.children.pop()#go down one level if possible
			#
			path.append(current)
			if current.typ == 'G': return board
			#update_board_cell(current, board, 'P')#update board cell
			#
		else:
			visited.add(current)
			#update_board_cell(current, board, 'O')#update board cellprint_board(board)
			current = stack.pop() #go up level if bottom level is reached
#
#########---- A* ----########
def Heuristic(node):
	heur = (abs(goal_node.y_pos - node.y_pos) + abs(goal_node.x_pos - node.x_pos) )
	#board[node.x_pos][node.y_pos] = str(node.g + heur)

	return (abs(goal_node.y_pos - node.y_pos) + abs(goal_node.x_pos - node.x_pos) )
#
def attach_and_eval(child,parent):
	child.parent = parent
	child.g = parent.g + 1
	child.h = Heuristic(child)
	child.f = child.h + child.g
#
def prop_path_imp(parent):
	for child in parent.children:
		if (parent.g + 1) < child.g:
			child.parent = parent
			child.g = parent.g + 1
			child.h = Heuristic(child)
			child.f = child.g + child.h
			prop_path_imp(child)
#
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j].f > items[j+1].f:
                items[j], items[j+1] = items[j+1], items[j]
#
def Astar(board, start_node, end_node):
	closed=[]
	open=[]
	current_node = start_node
	current_node.g = 0
	current_node.h = Heuristic(current_node)
	current_node.f = current_node.g + current_node.h
	open.append(current_node)
	while True:

		if len(open) < 1:
			return False
		current_node = open.pop(0)
		closed.append(current_node)
		if (current_node == end_node):
			findPath(start_node,end_node)
			return True
		succ = current_node.children
		for child in succ:

			if child not in open and child not in closed:

				attach_and_eval(child,current_node)
				open.append(child)
				board[child.x_pos][child.y_pos]="O"
				

				##################################

				#####################################
				bubble_sort(open)
			elif ((current_node.g + 1) < child.g):

				#print "FOUND CHEAPER PATH"
				#print '------4------'
				attach_and_eval(child,current_node)
				if child in closed:
					prop_path_imp(child)
#
def findPath(start_node, goal_node):
	coordinates = []
	current_node = goal_node
	board[goal_node.x_pos][goal_node.y_pos]="G"

	while True:
		if current_node == start_node:
			#print coordinates
			board[start_node.x_pos][start_node.y_pos]="S"
			return True
		else:
			coords = current_node.y_pos, current_node.x_pos
			coordinates.append(coords)
			current_node = current_node.parent
			board[current_node.x_pos][current_node.y_pos] = "P"
#
#board_size, start_node, goal_node, Barriers = user_input()
#board = create_board( set_0[0], set_0[1], set_0[2], set_0[3], set_0[4] )
#board = create_board( set_6[0], set_6[1], set_6[2], set_6[3], set_6[4] )
###################################################################
def draw(reverse_board, iterations):
	reverse_board [ len(reverse_board)-iterations[0][0]-1 ] [ iterations[0][1] ] = iterations[0][2]
	iterations.pop(0)
	for n in xrange(0, len(reverse_board)):
		for i in xrange(0, len(reverse_board[n])):
			#Label(text=reverse_board[n][i], width=5).grid(row=n, column=i)
			if reverse_board[n][i] == '-': Entry( bg="lavender", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'O': Entry( bg="blue", width=4).grid_configure(row=n, column=i)
			elif reverse_board[n][i] == 'B': Entry( bg="black", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'S': Entry( bg="yellow", width=4 ).grid(row=n, column=i)
			elif reverse_board[n][i] == 'P': Entry( bg="sky blue", width=4 ).grid(row=n, column=i)
			else: Entry( bg="green", width=4 ).grid(row=n, column=i)
	root.after( 500, draw, reverse_board, iterations )


#def GUI(board, iterations):
	

	

	#print iterations[0][2]
	#print reverse_board [ len(reverse_board)-iterations[0][0]-1 ] [ iterations[0][1] ]
	#draw(reverse_board)




	#root.mainloop()
###################################################################




'''print "Astar start"
boool = Astar(board, rot, goal_node)
print "Astar done"
print_board(board)
print "All done"'''
#print_board(board)
#print '\n\n'
#
#DFS_board = Depth_first_search(board, rot)
#
def update_iterations_with_path(iterations, path, board):
	for cell in path:
		#print "cell", cell
		if board[cell.x_pos][cell.y_pos] != 'S' and board[cell.x_pos][cell.y_pos] != 'G': iterations.append( [cell.x_pos, cell.y_pos, 'P'] )
	return iterations


board = create_board( set_5[0], set_5[1], set_5[2], set_5[3], set_5[4] )
rot, goal_node, class_board = create_linked_classes(board)
path, iterations = Breadth_first_search(board, rot, goal_node)

print "path: ", path[0]
iterations = update_iterations_with_path(iterations, path, board)


root = Tk()
reverse_board = []
for n in xrange( len(board)-1, -1, -1):
	reverse_board.append(board[n])
	
	

root.after( 500, draw, reverse_board, iterations )

print "after root.after"
root.mainloop()
#GUI(board, iterations)
#print "path: ", path
#board = update_board_with_path(board, rot, goal_node, path)
#print "BFS: \n"
#print_board(board)
'''
#
#print "\nDFS: \n"
#DFS_board = Depth_first_search(board, rot)
#print_board(board)'''






















'''Height = Label(frame1, text="Height", fg="black", font=("times", 15))#.grid(row=0, column=0)#.place(x=x, y=y)
Width = Label(frame1, text="Width", fg="black", font=("times", 15))#.grid(row=0, column=1)#.place(x=x+70, y=y+0)
start = Label(frame1, text="start point", fg="black", font=("times", 15))#.grid(row=0, column=2)#.place(x=x+140, y=y+0)
goal = Label(frame1, text="Goal point", fg="black", font=("times", 15))#.grid(row=0, column=3)#.place(x=x+240, y=y+0)
barriers = Label(frame1, text="Barriers", fg="black", font=("times", 15))#.grid(row=0, column=4)#.place(x=x+360, y=y+0)

height_entry = Entry(frame1, width=3)
width_entry = Entry(frame1, width=3)
start_entry = Entry(frame1, width=4)
goal_entry = Entry(frame1, width=4)
barriers_entry = Entry(frame1, width=40)

draw_board_button = Button(frame1, text="draw board", bg="sky blue", command=draw_GUI(board))

Height.pack()#grid(row=0, column=0)
height_entry.pack()#grid(row=0, column=1)
Width.pack()#grid(row=0, column=2)
width_entry.pack()#grid(row=0, column=3)
start.pack()#grid(row=0, column=4)
start_entry.pack()#grid(row=0, column=5)
goal.pack()#grid(row=0, column=6)
goal_entry.pack()#grid(row=0, column=7)
barriers.pack()#grid(row=0, column=8)
barriers_entry.pack()#grid(row=0, column=9)
draw_board_button.pack()#grid(row=0, column=10)
frame1.grid(row=0, rowspan=10, column=211, columnspan=10, sticky = W+E+N+S)'''