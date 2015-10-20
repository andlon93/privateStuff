#!/usr/bin/env python
import State as S
import AlfaBeta as AB
import Expectimax as EX
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
        weight = [0.5, 0.05, 0.05, 0.045, 0.05, 0.05, 0.15, 0.11, 0.05]
        print "game started"
        state = S.State(board)
        state.spawn()
        ##
        self.setBoard(state.get_board())
        #time.sleep(0.5)
        ##

        original_depth = 2
        depth = copy.deepcopy(original_depth)
        while state.can_make_a_move():
            best_move = None
            best_val = -1
            depth = original_depth
            if state.get_highest_tile() == 512:
                depth = original_depth + 1
            if state.get_highest_tile() == 1024:
                depth = original_depth + 2
           # if state.number_of_empty_tiles() < 5:
           #     depth = original_depth + 2
            if state.number_of_empty_tiles() < 4:
                depth = original_depth + 2
            if state.number_of_empty_tiles() < 3:
                depth = original_depth + 3
            if state.calculate_utility(weight) < 30:
                depth += 1
            print "Depth: ", depth
            for move in state.all_valid_moves():
                temp_state = copy.deepcopy(state)
                temp_state.move(move)
                #for r in temp_state.get_board():
                #   print r
                #print '\n\n\n'
                val = AB.ab_prun(temp_state, depth, best_val, 101, False, weight)
                #all_vals.append(val)
                if val > best_val:
                    best_val = val
                    best_move = move
            state.move(best_move)


            print "free tiles :", state.free_tiles_utility()
            print "Highest_tile :", state.highest_tile_utility()
            print "largest in corner :", state.largest_tile_corner_util()
            print "cluster_score :", state.cluster_score()
            print "Number of same: ", state.number_of_same()
            print "brute method: ", state.brute_method()
            print "Brute line2: ", state.brute_line2()
            print "Upper vs lower: ", state.sum_greater_upper()
            print "First over Seconds: ", state.first_over_second()
            print "utility score: ", state.calculate_utility(weight)
            #print "highest numbers: ", state.highest_four()
            ##
            self.setBoard(state.get_board())
            #time.sleep(0.1)
            ##
            #break
            state.spawn()
            ##
            self.setBoard(state.get_board())



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