#!/usr/bin/env python
from __future__ import division
from multiprocessing import Process, Queue
import State as S
import sys
import random
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
import copy
import neural_net as ann
import numpy as np
import operator
#
W = [
    [  [  10,    9,  7.6, 7.4],
       [ 7.4,  6.4,  5.7, 5.3],
       [ 4.5,  4.1,  2.7, 1.2],
       [0.09, 0.07, 0.04, 0.02] ],

    [  [  10,  7.4,  4.5, 0.09],
       [   9,  6.4,  4.1, 0.07],
       [ 7.6,  5.7,  2.7, 0.04],
       [ 7.4,  5.3,  1.2, 0.02] ],   ]
#
def utility(board):
    #board=[nboard[0:4],nboard[4:8],nboard[8:12],nboard[12:16]]
    max_score = 0
    for W_matrix in W:
        temp = 0
        for r in range(4):
            for c in range(4):
                temp += W_matrix[r][c]*board[r][c]
        if temp > max_score:
            max_score = temp
    return max_score
#########---- Class that represent the different tiles in the UI ----########
def makeMove(move, depth, state, queue):
    temp_state = copy.deepcopy(state) # Copy the current state
    temp_state.move(move) # Simulate moving in the given direction
    queue.put([EX.expectimax(temp_state, depth),move]) # Calculate score of move, and put in the queue

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

        self._numCols = 4
        self._numRows = 4

        self.setObjectName('mainObject')


        self._tiles = []
    ######## Create objects ##########
    # Gettere and settere
    @QtCore.pyqtProperty(QtDeclarative.QPyDeclarativeListProperty, constant=True)
    def tiles(self): return QtDeclarative.QPyDeclarativeListProperty(self, self._tiles)
    #
    @QtCore.pyqtProperty(int, notify=numColsChanged)
    def numCols(self): return self._numCols
    #
    def setNumCols(self, nCols):
        if self._numCols != nCols:
            self._numCols = nCols
            self.numColsChanged.emit()
    #
    @QtCore.pyqtProperty(int, notify=numRowsChanged)
    def numRows(self): return self._numRows
    #
    def setNumCols(self, nRows):
        if self._numRows != nRows:
            self._numRows = nRows
            self.numRowsChanged.emit()
    # Public member functions
    @QtCore.pyqtSlot(int, int, int)
    def setStatusOfTile(self, row, col, status):
        t = self._tile(row, col)
        if t is None:
            return False
        else:
            t.setStatus(status)
            return True
    #
    @QtCore.pyqtSlot()
    def setUp(self):
        print("Setting up the game.")
        for ii in range(16):
            self._tiles.append( TileData( 0 ) )
    #
    #@QtCore.pyqtSlot(list)
    def find_best_valid_move(self,state, moves):
        d={0:moves[0],1:moves[1],2:moves[2],3:moves[3]}
        sortert=sorted(d.items(), key=operator.itemgetter(1))
        for i in range(3,-1,-1):
            move=sortert[i][0]
            #print(move)
            if state.is_valid_move(move): return move
    #
    @QtCore.pyqtSlot()
    def startGame(self):
        time_0 = time.time()
        print ("game started")
        '''
        init an ANN
        train the ANN
        '''
<<<<<<< HEAD
        nn=ann.ANN(0.05,[(16, 100),(100,4)])
        nn.training(2)
        #me
=======
        nn=ann.ANN(0.01,[(17, 100),(100,4)])
        nn.training(2)
        #
>>>>>>> 715fa3e3683e7c9422a7ad7b25a54f88d6b596f9
        state = S.State(board)
        state.spawn()
        ##
        self.setBoard(state.get_board())
        highest = 0
        moves = 0
        ##
        while state.can_make_a_move():
            '''
            moves = ANN.something()
            move = find_best_valid_move(moves)

            '''
            ###########################################################
            matrix=[]
            for i in range(2):
                vector = []
                for row in state.get_board():
                    for tile in row:
                        vector.append(tile)
                vector.append(utility(state.get_board()))
                print("regnet utility")
                matrix.append(np.array(vector))
            ###########################################################
            b=nn.predict_a_move(np.array(matrix))
            print("prob dist: ",b[0])
            move = self.find_best_valid_move(state,b[0])
            print ("Move: ", move,"\n")

            #
            state.move(move)#make the move
            self.setBoard(state.get_board())#update board with the move
            #
            state.spawn()#spawn a new tile
            time.sleep(0.15)
            self.setBoard(state.get_board())#update board with the spawn
        self.setBoard(state.get_board())
        print("Can not make more moves...\n", "Highest tile achieved: ", state.get_highest_tile())
    #
    @QtCore.pyqtSlot()
    def setBoard(self, board):
        for r in range(4):
            for c in range(4):
                self.setStatusOfTile(r, c, board[r][c])
    # Private member functions
    def _onBoard(self, row, col):
        return (row >= 0 and row < self._numRows and col >= 0 and col < self._numCols)
    #
    def _tile(self, row, col):
        if self._onBoard(row, col):
            return self._tiles[col + self._numRows * row]
        return None
#
#
if __name__ == '__main__':
    #
    board = [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
    #
    game = Game()
    #
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    engine = view.engine()
    #
    game.setUp()
    #
    engine.rootContext().setContextObject(game)
    view.setSource(QtCore.QUrl.fromLocalFile('grid.qml'))
    view.show()
    #
    sys.exit(app.exec_())