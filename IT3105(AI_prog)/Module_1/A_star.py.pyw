#!/usr/bin/env python
import sys
import random
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
debug = False

#

#LINK for Astar online: https://qiao.github.io/PathFinding.js/visual/

#########---- Letters from the print ----########
'''C = Closed.....S = start....G = Goal.....B = Barrier.....P = path.....O = Open'''
'''-1 = obstacle ..... 0 = none ..... 1 = opened ..... 2 = path ..... 3 = start ..... 4 = goal'''
#########---- Example sets ----########
#        row  col start    goal    Barriers
exapmle_sets = [
[ 10, 10, [0,0],  [9,9],   [[2,3,5,5], [8,8,2,1]]                                          ],
[ 20, 20, [19,3], [2,18],  [[5,5,10,10], [1,2,4,1]]                                        ],
[ 20, 20, [0,0],  [19,19], [[17,10,2,1], [14,4,5,2], [3,16,10,2], [13,7,5,3], [15,15,3,3]] ],
[ 10, 10, [0,0],  [9,5],   [[3,0,2,7], [6,0,4,4], [6, 6, 2, 4]]                            ],
[ 10, 10, [0,0],  [9,9],   [[3,0,2,7], [6,0,4,4], [6, 6, 2, 4]]                            ],
[ 20, 20, [0,0],  [19,13], [[4,0,4,16], [12,4,2,16], [16,8,4,4]]                           ],
                                                                                             ]
def run_sett(n): return exapmle_sets[n][0], exapmle_sets[n][1], exapmle_sets[n][2], exapmle_sets[n][3], exapmle_sets[n][4]
#########---- Node Class ----########
class Node:
    children = None
    typ = None
    parent = None
    x_pos = None
    y_pos = None
    reverse_y_pos = None
    reverse_x_pos = None
    #-- For A* --#
    g = None
    h = None
    f = None
    u = 2
    def __init__(self):
        self.children = []
#########---- Print board methods ----########
def update_board_cell(node, board, letter):
    x = node.x_pos
    y = node.y_pos
    board[x][y] = letter
    return board
#########---- Take input from user ----########
def user_input(): #get all input from user
    print '\n\n'
    done = False
    while not done:
        rows = int( raw_input("Height of board: ") )    #Board size
        cols = int( raw_input("Width of board: ") )     #Board size
        #start and end nodes
        start_node_Xpos = int( raw_input("X position of start node: ") )
        start_node_Ypos = int( raw_input("Y position of start node: ") )
        goal_node_Xpos = int( raw_input("X position of goal node: ") )
        goal_node_Ypos = int( raw_input("Y position of goal node: ") )
        #Barriers
        Barriers = []
        num_of_barriers = int( raw_input("Number of barriers: ") )
        for n in xrange(0, num_of_barriers):
            Barrier = []
            Barrier.append( int( raw_input("Enter barrier X-Left: ") ) )
            Barrier.append( int(raw_input("Enter barrier Y-Bottom: ") ))
            Barrier.append( int(raw_input("Enter barrier Width: ") ))
            Barrier.append( int(raw_input("Enter barrier height: ") ))
            Barriers.append(Barrier)
        #printing the input
        print "\n\nRows:", rows, " Columns:", cols
        print "Start node:   ", start_node_Xpos,",",start_node_Ypos, "    Goal node:   ", goal_node_Xpos,",",goal_node_Ypos
        for n in xrange( len(Barriers)):
            print "Barrier ", n, ":    ", Barriers[n][0], ",", Barriers[n][1], ",", Barriers[n][2], ",", Barriers[n][3]
        ##
        temp = False
        while not temp:
            user_done = str( raw_input("\n\nDo you want to retype the board?(y/n)") )
            if user_done == "n":
                done = True
                temp = True
            elif user_done == "y":
                done = False
                temp = True
            else:
                print "\n\nWrong input given. You have to answer 'y' or 'n'."
    if debug:
        print "board_size: ", board_size
        print "start_node, goal_node: ", start_node, goal_node
        print "Barriers: ", Barriers
        print '\n'
    return rows, cols, [start_node_Xpos, start_node_Ypos], [goal_node_Xpos, goal_node_Ypos], Barriers
#########---- Create board ----########
def create_empty_board(rows, cols):#Initialaise an empty board
    board = []

    for row in xrange(0, rows):
        column = []
        for col in xrange(0, cols):
            column.append(0)
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

        for h in xrange(0, height):#adding the barriers to the board with mark -1
            for w in xrange(0, width):
                #print "Y:",y+h, " X:",x+w
                board[y+h][x+w] = -1
    if debug:
        print '\n'
        for row in board:
            print row
        print '\n'
    return board
def create_board(rows, cols, start_node, goal_node, Barriers):#Creates board using help functions
    board = create_empty_board(rows, cols)#create empty board
    board[ start_node[1] ][ start_node[0] ] = 3 #add start node marked 3
    board[ goal_node[1] ][ goal_node[0] ] = 4 #add goal node marked 4
    board = add_Barriers(board, Barriers)#add the barriers to the board

    if debug:
        print '\n'
        print "Rows: ", rows, "columns: ", cols
        for row in board:
            print row
        print '\n'
    #print_board(board)

    return board
#########---- DFS ----########
def Depth_first_search(board, start_node):
    stack = []
    current = start_node
    visited = set()
    path = []
    #
    while True:
        if current.typ == 4: return board
        #
        if current.children and current not in visited:
            stack.append(current)
            current = current.children.pop()#go down one level if possible
            #
            path.append(current)
            if current.typ == 4: return board
            #update_board_cell(current, board, 2)#update board cell
            #
        else:
            visited.add(current)
            #update_board_cell(current, board, 1)#update board cellprint_board(board)
            current = stack.pop() #go up level if bottom level is reached
#########---- A* ----########
def Heuristic(node, goal_node):
    #f = (abs(goal_node.y_pos - node.y_pos) + abs(goal_node.x_pos - node.x_pos))
    #print f
    #print "Y: ", goal_node.y_pos," ", node.y_pos,"  X: ", goal_node.x_pos, node.x_pos
    #print "H(y): ", abs(goal_node.y_pos - node.y_pos), "  H(x): ", abs(goal_node.x_pos - node.x_pos), '\n'
    return  (abs(goal_node.y_pos - node.y_pos) + abs(goal_node.x_pos - node.x_pos))
#
def attach_and_eval(child, parent, end_node, is_dfs):
    child.parent = parent
    child.g = parent.g + 1
    child.h = Heuristic(child, end_node)
    if is_dfs:
        child.f = child.h
    else:
        child.f = child.h + child.g
    #print " X:",child.y_pos ," Y:",  child.x_pos, " F:", child.f
#
def prop_path_imp(parent, end_node):
    for child in parent.children:
        if (parent.g + 1) < child.g:
            child.parent = parent
            child.g = parent.g + 1
            child.h = Heuristic(child, end_node)
            child.f = child.g + child.h
            prop_path_imp(child)
#
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items)-1-i):
            if items[j].f > items[j+1].f:
                items[j], items[j+1] = items[j+1], items[j]
#
def Astar(board, start_node, end_node, is_dfs):
    closed=[]
    open_list=[]

    current_node = start_node
    current_node.g = 0
    current_node.h = Heuristic(current_node, end_node)
    current_node.f = current_node.g + current_node.h
    open_list.append(current_node)

    while True:
        if len(open_list) < 1:
            return False

        current_node = open_list.pop(0)
        game.algorithm_update_GUI(current_node, start_node, end_node, 1)#Write to GUI
        closed.append(current_node)

        if (current_node == end_node):
            print "open_list", len(open_list)
            print "closed_list", len(closed)
            return True
        succ = current_node.children

        for child in succ:
            if child not in open_list and child not in closed:
                game.algorithm_update_GUI(child, start_node, end_node, 5) #Write to GUI

                attach_and_eval(child, current_node, end_node, is_dfs)
                open_list.append(child)
                bubble_sort(open_list)
            elif ((current_node.g + 1) < child.g):
                attach_and_eval(child, current_node, end_node, is_dfs)
                if child in closed and not is_dfs:
                    prop_path_imp(child, end_node)
#
def findPath(start_node, goal_node):
    current_node = goal_node
    path = []
    #
    while True:
        if current_node == start_node:
            for i in xrange( len(path)-1, -1, -1 ): game.algorithm_update_GUI(path[i], start_node, goal_node, 2)
            return True
        else:
            current_node = current_node.parent
            path.append(current_node)
    return False
#
#########---- Class that represent the different tiles in the UI ----########
class TileData(QtCore.QObject):

    statusChanged = QtCore.pyqtSignal(int)

    def __init__(self, status):
        super(TileData, self).__init__()
        self._status = status

    # Gettere and settere
    @QtCore.pyqtProperty(int, notify=statusChanged)
    def status(self):
        return self._status

    def setStatus(self, status):
        if self._status != status:
            self._status = status
            self.statusChanged.emit(self._status)
            app.processEvents()

#########---- Class that represent all the tiles in the UI ----########
class Game(QtCore.QObject):
    numColsChanged = QtCore.pyqtSignal()
    numRowsChanged = QtCore.pyqtSignal()

    def __init__(self):
        super(Game, self).__init__()

        print("A new game is initiated.")

        self._numCols = 0
        self._numRows = 0

        self.setObjectName('mainObject')

        random.seed()

        self._tiles = []
    ######## Create objects ##########
    @QtCore.pyqtSlot(list)
    def create_linked_classes(self, board):
        class_board = []#matrix with each node as an object
        #fill in objects where there is not a B
        for row in xrange(0, len(board)):
            row_list = []
            for col in xrange(0, len(board[row])):
                if board[row][col] != -1:
                    node = Node()
                    node.typ = board[row][col]
                    node.x_pos = row
                    node.y_pos = col
                    #Easy to print with (0,0) in nottom left corner
                    node.reverse_x_pos = len(initialBoard)-row-1
                    #
                    row_list.append(node)
                    if board[row][col] == 3:
                        rot = node
                    if board[row][col] == 4:
                        goal = node
                    #if node != rot:
                    #node.parent =
                else:
                    row_list.append(-1)
            class_board.append(row_list)
        #
        #Fill in child lists on all nodes
        ##################################print "zzzz:  ", len(class_board)
        for row in xrange(0, len(class_board)):
            ##################################print "xxxx:  ", len(class_board[row])
            for col in xrange(0, len(class_board[row])):
                if class_board[row][col] != -1:

                    '''if debug: print 'node: ', class_board[row][col], '\n'''
                    if row-1 > -1 and class_board[row-1][col] != -1:
                        class_board[row][col].children.append( class_board[row-1][col] )#add child nodes
                        class_board[row-1][col].parent = class_board[row][col]#add parent

                    if col-1 > -1 and class_board[row][col-1] != -1:
                        class_board[row][col].children.append( class_board[row][col-1] )#add child nodes
                        class_board[row][col-1].parent = class_board[row][col]#add parent

                    if row+1 < len(class_board) and class_board[row+1][col] != -1:
                        class_board[row][col].children.append( class_board[row+1][col] )#add child nodes
                        class_board[row+1][col].parent = class_board[row][col]#add parent

                    if col+1 < len(class_board[row]) and class_board[row][col+1] != -1:
                        class_board[row][col].children.append( class_board[row][col+1] )#add child nodes
                        class_board[row][col+1].parent = class_board[row][col] #add parent
    #
        if debug:
            print "children: ", rot.children, '\n'
            print "rot", rot, 'pos: ', rot.x_pos, rot.y_pos
            print "parent: ", rot.children[0].parent, '\n'
            print "goal: ", goal.typ
        return rot, goal, class_board

    ######### BFS #############
    @QtCore.pyqtSlot(list, object, object, list)
    def BFS_update_board_with_path(self, board, start_node, goal_node, path):
        for cell in path:
            if (cell != start_node and cell != goal_node ): self.algorithm_update_GUI(cell, start_node, goal_node, 2)
            #
    @QtCore.pyqtSlot(list, object, object)
    def Breadth_first_search(self, board, start_node, goal_node):
        print "BFS start"
        queue = [[start_node]]
        visited = set()
        iterations = []
        #
        #nodes_generated = 0
        #nodes_popped_from_queue = 0
        while queue:
            path = queue.pop(0)
            #nodes_popped_from_queue +=
            current_node = path[-1]
            ##-- Write to GUI --##
            game.algorithm_update_GUI(current_node, start_node, goal_node, 1)
            #
            #board[current_node.x_pos][current_node.y_pos] = 1
            if current_node == goal_node:
                return path, board
            elif current_node not in visited:
                for child in current_node.children:
                    temp_path = list(path)
                    temp_path.append(child)
                    queue.append(temp_path)
                visited.add(current_node)
    ###########################

    # Gettere and settere
    @QtCore.pyqtProperty(QtDeclarative.QPyDeclarativeListProperty, constant=True)
    def tiles(self): return QtDeclarative.QPyDeclarativeListProperty(self, self._tiles)

    @QtCore.pyqtProperty(int, notify=numColsChanged)
    def numCols(self): return self._numCols
#
    def setNumCols(self, nCols):
        if self._numCols != nCols:
            self._numCols = nCols
            self.numColsChanged.emit()

    @QtCore.pyqtProperty(int, notify=numRowsChanged)
    def numRows(self): return self._numRows

    def setNumCols(self, nRows):
        if self._numRows != nRows:
            self._numRows = nRows
            self.numRowsChanged.emit()

    # Public member functions
    @QtCore.pyqtSlot(object, object, object, int)
    def algorithm_update_GUI(self, current_node, start_node, goal_node, status):
        if (current_node != start_node and current_node != goal_node ):
            time.sleep(sleep_dur)
            t = self._tile(current_node.reverse_x_pos, current_node.y_pos)
            if t is None:
                return False
            else:
                t.setStatus(status)
                return True

    @QtCore.pyqtSlot()
    def setUp(self):
        print("The game has started.")

        self._numRows = len(initialBoard)
        self._numCols = len(initialBoard[0])

        # initialise board
        for ii in xrange(self._numRows * self._numCols):
            self._tiles.append( TileData( initialBoard[len(initialBoard)-(ii/self._numRows)-1] [ii - ii/self._numRows*self._numCols] ) )

    @QtCore.pyqtSlot()
    def startGame(self):
        rot, goal_node, class_board = self.create_linked_classes(initialBoard)
        if choose_algorithm == 0:
            ##--Astar--##
            found_path = Astar(initialBoard, rot, goal_node, False)
            if found_path: findPath(rot, goal_node)
            else: print 'Path not found'
        elif choose_algorithm == 1:
            ##--Astar--##
            path, board = self.Breadth_first_search(initialBoard, rot, goal_node)
            self.BFS_update_board_with_path(board, rot, goal_node, path)
        elif choose_algorithm == 2:
            ##--DFS--##
            found_path = Astar(initialBoard, rot, goal_node, True)
            if found_path: findPath(rot, goal_node)
            else: print 'Path not found'

    @QtCore.pyqtSlot()
    def updateBoard(self):
        game.setStatusOfTile(random.randint(0, self._numRows-1), random.randint(0, self._numCols-1), random.randint(-1, 4))

    @QtCore.pyqtSlot()
    def resetBoard(self):
        for r in range (self._numRows):
            for c in range(self._numCols):
                self.setStatusOfTile(r, c, initialBoard[r][c])

    # Private member functions
    def _onBoard(self, row, col):
        return (row >= 0 and row < self._numRows and col >= 0 and col < self._numCols)

    def _tile(self, row, col):
        if self._onBoard(row, col):
            return self._tiles[col + self._numRows * row]
        return None


if __name__ == '__main__':
    right = False
    #run_example_set = None
    #choose_algorithm = None
    while not right:
        print "Do you want to run a predefined board or do you wish to create your own board?"
        run_example_set = int( raw_input("predefined: '0',   Create your own: '1'") )
        if run_example_set == 1 or run_example_set == 0: right = True

        print "Which algorithm do you want to run?"
        choose_algorithm = int( raw_input("Astar: '0',   BFS: '1',  DFS: 2") )
        if choose_algorithm == 1 or choose_algorithm == 0 or choose_algorithm == 2: right = True

        if not right: print "some input given was wrong. We will start again\n\n"

    if run_example_set == 1:
        rows, cols, start_node, goal_node, Barriers = user_input()
    else:
        print "which predefined set do you wish to run?"
        for n in xrange(len(exapmle_sets)):
            print n, ":  ", exapmle_sets[n][0], exapmle_sets[n][1], exapmle_sets[n][2], exapmle_sets[n][3], exapmle_sets[n][4], "\n"
        sett = int( raw_input("Type in the number of the set you wish to run:  ") )
        rows, cols, start_node, goal_node, Barriers = run_sett(sett)

    ###################################################################
    initialBoard = create_board(rows, cols, start_node, goal_node, Barriers)
    sleep_dur = 0.01
    game = Game()

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    engine = view.engine()

    game.setUp()

    engine.rootContext().setContextObject(game)
    view.setSource(QtCore.QUrl.fromLocalFile('grid.qml'))
    view.show()

    sys.exit(app.exec_())