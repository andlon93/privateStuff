#!/usr/bin/env python
from __future__ import division
from multiprocessing import Process, Queue
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
    @QtCore.pyqtSlot()
    def startGame(self):
        time_0 = time.time()
        #weight = [0.5, 0.04331720843381177, 0.05, 0.0525487188507247, 0.05, 0.05437746849658362, 0.186889932111141, 0.11081454380077221, 0.05]
        '''
        weight = [0.5, 0.05, 0.05, 0.045, 0.05, 0.05, 0.15, 0.11, 0.05]
        weight = [0.5, 0.043, 0.05, 0.053, 0.05, 0.054, 0.19, 0.11, 0.05, 0.1]
        weight = [0.5, 0.043, 0.05, 0.053, 0.05, 0.054, 0.19, 0.11, 0.05, 0.05]
        '''
        #print "game started"
        state = S.State(board)
        state.spawn()
        ##
        self.setBoard(state.get_board())
        highest = 0
        moves = 0
        ##
        process = [None] * 4
        queue = Queue(maxsize=0)
        rand = 0
        while state.can_make_a_move():
            best_move = 0
            if rand >= 30:
                best_move = random.randint(0,4)
                rand += 1
                print("RANDOMS")
                if rand == 40:
                    rand = 0
            else:
                #rand += 1
                start_time = time.time()
                depth = 1
                best_move = None
                best_val = -1
                #
                if state.number_of_empty_tiles() < 2:
                    depth +=1
                if state.get_highest_tile() > 511:
                    depth += 1
                #
                vals_moves = []
                valid_moves = state.all_valid_moves()
                for move in valid_moves:
                    process[move] = Process(target=makeMove, args=(move, depth, state, queue))
                    process[move].start()
                if time.time() - start_time < 0.095:
                    time.sleep(0.095-(time.time() - start_time))
                #print "move to spawn", ("--- %s seconds ---" % (time.time() - start_time))
                self.setBoard(state.get_board())
                start_time = time.time()
                for move in valid_moves:
                    vals_moves.append(queue.get())
                for move in valid_moves:
                    process[move].join()
                for val_move in vals_moves:
                    if val_move[0] > best_val:
                        best_val = val_move[0]
                        best_move = val_move[1]
                #
            state.move(best_move)
            moves += 1
            if state.get_highest_tile() > highest:
                highest = state.get_highest_tile()
                print ("hoyeste oppnaadd:", highest, " trekk:", moves," seconds:",time.time() - time_0,  " Time per move:", (time.time() -time_0)/moves)
            #
            # if time.time() - start_time < 0.095:
            #     time.sleep(0.095-(time.time() - start_time))
            #print "spawn to move", ("--- %s seconds ---" % (time.time() - start_time))
            self.setBoard(state.get_board())
            ##
            state.spawn()
        self.setBoard(state.get_board())
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