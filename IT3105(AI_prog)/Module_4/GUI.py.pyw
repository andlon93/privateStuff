#!/usr/bin/env python
import State as S
import AlfaBeta as AB
import sys
import random
import time
from PyQt4 import QtCore, QtGui, QtDeclarative
import copy
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
    def startGame(self):

        print "game started"
        state = S.State(board)
        state.spawn()
        ##
        self.setBoard(state.get_board())
        #time.sleep(0.5)
        ##
        depth = 3
        while state.can_make_a_move():
            #for n in range(10):
            #print "new iteration"
            #val = ab_prun(state, 3, -1, 101, True)
            best_move = None
            best_val = -1
            all_vals = []
            if depth < 4 and state.get_highest_tile() == 256:
                print "256"
                depth = 4
            elif depth < 5 and state.get_highest_tile() == 512:
                print "512"
                depth = 5
            for move in state.all_valid_moves():
                temp_state = copy.deepcopy(state)
                temp_state.move(move)
                #for r in temp_state.get_board():
                #   print r
                #print '\n\n\n'
                val = AB.ab_prun(temp_state, depth, -1, 101, False)
                all_vals.append(val)
                if val > best_val:
                    best_val = val
                    best_move = move
                #break
            #print all_vals
            #print best_val, best_move
            #if best_val == 0:
            #   for r in state.get_board():
            #       print r
            #   print '\n\n'
            state.move(best_move)
            ##
            self.setBoard(state.get_board())
            #time.sleep(0.3)
            ##
            #break
            state.spawn()
            ##
            self.setBoard(state.get_board())
            #time.sleep()


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

    game = Game()
    #
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    engine = view.engine()
    #
    game.setUp()

    engine.rootContext().setContextObject(game)
    view.setSource(QtCore.QUrl.fromLocalFile('grid.qml'))
    view.show()
    #
    sys.exit(app.exec_())