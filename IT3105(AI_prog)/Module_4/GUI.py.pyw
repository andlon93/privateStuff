#!/usr/bin/env python
import State
import sys
import random
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
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

        self._numCols = 4
        self._numRows = 4

        self.setObjectName('mainObject')

        #random.seed()

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
    ###############################################################
    @QtCore.pyqtSlot()
    def setUp(self):
        print("Setting up the game.")

        for ii in xrange(16):
            self._tiles.append( TileData( 0 ) )
    #
    @QtCore.pyqtSlot()
    def temp(self, state):
        for move in xrange(3):
            state.move(move)
            for row in xrange(4):
                for col in xrange(4):
                    if state.board[row][col] == 0: break


    @QtCore.pyqtSlot()
    def make_some_moves(self, state):
        moves = [0,1,3,2]
        while state.can_make_a_move():
            for move in moves:
                state.move(move)
                for row in xrange(4):
                    for col in xrange(4):
                        if state.board[row][col] == 0: break

            self.setBoard(state.get_board())
            #time.sleep(2)
            state.spawn()
            self.setBoard(state.get_board())
            #time.sleep(1)
    @QtCore.pyqtSlot()
    def startGame(self):
        
        print "game started"
        
        state.spawn()
        self.setBoard(state.get_board())
        #time.sleep(2)
        self.make_some_moves(state)
        
        
        

        
    ################################################################
    @QtCore.pyqtSlot()
    def updateBoard(self):
        tiles = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        t = random.randint(0, len(tiles)-1)
        self.setStatusOfTile(random.randint(0, self._numRows-1), random.randint(0, self._numCols-1), tiles[t])
    #
    @QtCore.pyqtSlot()
    def setBoard(self, board):
        for r in xrange(4):
            for c in xrange(4):
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
    state = State.State(board)
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