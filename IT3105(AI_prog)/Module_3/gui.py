from __future__ import division

import readfile
import time
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from multiprocessing import Queue
from threading import *
import AstarGac

window_size_x = 500 # Window width
window_size_y = 400 # Window Height

board = []

def worker():
	sleeptime = 0.2
	try:
		while True:
			time.sleep(sleeptime)
			circles.update()
	except:
		print "Gui overload!"
		sleeptime = sleeptime * 5


class Draw(QWidget):
	# All the GUI stuff is done within this class
	# paintEvent is the function that draws the GUI - this is called by the "worker" thread
	# The "worker" thread also needs "processEvents()" to be called by the algorithm, this makes the GUI thread work
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(300, 100, window_size_x, window_size_y) # setGeometry(x_pos, y_pos, width, height) - places and sizes the windows
        self.setWindowTitle('Astar_GAC')

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing) # AA makes lines smooth
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect()) # make a white drawing background
        paint.setPen(Qt.red) # Color of the edges(lines)
        rectMatrix = generate_rectMatrix(generate_color_matrix(AstarGac.current_state.make_board()))
        for tile in rectMatrix:
        	print "farge: ",tile[4]
        	paint.setBrush(tile[4])
        	paint.drawRect(tile[0],tile[1],tile[2],tile[3])
        paint.setPen(Qt.darkRed) # Color of the edges(lines)
        paint.end()

def calculate_size(cols_size,rows_size): #Calculates pixels per col/row
	cols_px = window_size_x / cols_size
	rows_px = window_size_y / rows_size
	return cols_px, rows_px


def generate_rectMatrix(color_matrix):
	for c in range(cols_size):
		for r in range(rows_size):
			rectMatrix.append( ((c*cols_px),(r*rows_px),((c+1)*cols_px),((r+1)*rows_px), color_matrix[r][c]))
	return rectMatrix


def generate_board(state):
	rows = state.rows
	cols = state.cols
	board = [[-1 for x in xrange(cols_size)] for x in xrange(rows_size)]
	for i in range (len(rows)):
		if len(rows[i].domain)==1:
			for k in range(len(rows[i].get_domain())):
				board[i][k] = int(rows[i].get_domain()[0][k])
		else:
			for k in range(len(rows[i].get_domain()[0])):
				board[i][k] = -1
	return board


def generate_color_matrix(board):
	color_matrix = [[None for x in xrange(len(board[0]))] for x in xrange(len(board))]
	print "col/rows_size", cols_size, rows_size
	for c in range(len(board)):
		for r in range(len(board[c])):
			if board[c][r] == '2':
				print "gray"
				color_matrix[c][r] = (Qt.gray)
			elif board[c][r] == '0':
				print "white"
				color_matrix[c][r] = (Qt.white)
			elif board[c][r] == '1':
				color_matrix[c][r] = (Qt.blue)
			#print color_matrix[c][r]
	for row in color_matrix:
		print row
	return color_matrix

def initialise_color_matrix():
	color_matrix = [[Qt.blue for x in xrange(cols_size)] for x in xrange(rows_size)]
	# for c in range(cols_size):
	# 	for r in range(rows_size):
	# 		print "c,r: ",c,r
	# 		color_matrix[c][r] = (Qt.blue)
	return color_matrix

color_matrix = []
rectMatrix = []
graph = "nono-heart.txt"
cols_size, rows_size = readfile.getSizes(graph)
cols_px, rows_px = calculate_size(cols_size, rows_size)

color_matrix = initialise_color_matrix()

app = QApplication([])





if __name__ == '__main__':

	circles = Draw()
	rectMatrix = generate_rectMatrix(color_matrix)

	t = Thread(target=worker)
	t.start()
	circles.show()
	start_state, rows, cols = readfile.read_graph("nono-heart.txt")
	#k = Thread(target=AstarGac.Astar, args=(start_state,rows,cols))
	#k.start()
	AstarGac.Astar(start_state,rows,cols)
	app.exec_()
	print ("Scenario:")
	# graph = "nono-"
	# graph += raw_input("")
	# graph += ".txt"





