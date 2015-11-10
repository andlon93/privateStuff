#!/usr/bin/env python
from __future__ import division
from multiprocessing import Process, Queue
import State as S
import sys
import random
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
import copy
#
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
    def find_best_valid_move(self, moves):
        d={0:moves[0],1:moves[1],2:moves[2],3:moves[3]}
        sortert=sorted(d.items(), key=operator.itemgetter(1))
        for i in range(3,-1,-1):
            move=sortert[i][1]
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
            #
            state.move(move)#make the move
            self.setBoard(state.get_board())#update board with the move
            #
            state.spawn()#spawn a new tile
            time.sleep(0.3)
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