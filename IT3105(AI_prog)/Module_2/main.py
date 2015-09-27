from __future__ import division
import Node
import State
import readfile
import time
import math
import Astar_GAC
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *

print "GO"
window_size_x = 800 # Window width
window_size_y = 600 # Window Height


def worker():
	sleeptime = 0.01
	try:
		while True:
			time.sleep(sleeptime)
			circles.update()
	except:
		print "Gui overload!"
		sleeptime = sleeptime * 5
t = Thread(target=worker)
t.start()

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
        for coords in constraints_coordinates:
        	paint.drawLine(    ((coords[0] + abs(lowest_x))*x_multi), ((coords[1]+ abs(lowest_y))*y_multi), ((coords[2]+ abs(lowest_x))*x_multi), ((coords[3]+ abs(lowest_y))*y_multi)    )
        paint.setPen(Qt.darkRed) # Color of the edges(lines)
        for circle in circle_matrix:
            center = QPoint( ( circle[0] * x_multi ) + abs(lowest_x)*x_multi , (( circle[1] ) * y_multi ) + abs(lowest_y)*y_multi)
            paint.setBrush(circle[2])
            paint.drawEllipse(center, 10, 10) # arguments 2 and 3 are the size of the circles, in x and y direction. Argument 1 is the placement, also containing x and y
        paint.end()

def findLowestAndHighestValues(circle_matrix):
    lowest_x = lowest_y = highest_x = highest_y = 0
    for node in circle_matrix:
        if node[0]>highest_x:
            highest_x = node[0]
        if node[0]<lowest_x:
            lowest_x = node[0]
        if node[1]>highest_y:
            highest_y = node[1]
        if node[1]<lowest_y:
            lowest_y = node[1]
    return lowest_x,lowest_y,highest_x,highest_y

def generate_circle_matrix(state):
	color = Qt.white
	circle_matrix = [[0 for x in xrange(4)] for x in xrange(len(state.nodes))]
	i = 0;
	for node in state.nodes:
		circle_matrix[i][0]=int(round(float(state.nodes[node].x)))
		circle_matrix[i][1]=int(round(float(state.nodes[node].y)))
		domain = state.nodes[node].domain
		if (len(domain) > 1):
			color=Qt.white
		else:
			if domain[0] == 0:
				color=Qt.red
			elif domain[0] == 1:
				color = Qt.darkGray
			elif domain[0] == 2:
				color = Qt.yellow
			elif domain[0] == 3:
				color = Qt.black
			elif domain[0] == 4:
				color = Qt.magenta
			elif domain[0] == 5:
				color = Qt.lightGray
		circle_matrix[i][2]=color
		i=i+1
	return circle_matrix

def generate_coordinates(state, cons):
	# This function makes a list containing the x and y coordinates of each pair of connected nodes
	constraints_coordinates=[[0 for x in xrange(4)] for x in xrange(len(cons))] # constraints_coordinates[0][0]= node 1 - x, [0][1] =node 1 - y, [0][2] = node 2 - x, [0][3] = node 2 -y
	k=0
	for cons_pair in cons:
		constraints_coordinates[k][0] = (int(round(float(state.nodes[cons_pair[0]].x))))
		constraints_coordinates[k][1] = (int(round(float(state.nodes[cons_pair[0]].y))))
		constraints_coordinates[k][2] = (int(round(float(state.nodes[cons_pair[1]].x))))
		constraints_coordinates[k][3] = (int(round(float(state.nodes[cons_pair[1]].y))))
		k=k+1
	return constraints_coordinates

state, cons = readfile.read_graph("graph6.txt")

# Setting up lists and variables used by the GUI to draw the graph
circle_matrix = generate_circle_matrix(state)
constraints_coordinates = generate_coordinates(state, cons)
lowest_x,lowest_y,highest_x,highest_y = findLowestAndHighestValues(circle_matrix)
y_multi = ((window_size_y-100)/highest_y)
x_multi = ((window_size_x-100)/highest_x)

app = QApplication([])
circles = Draw()
circles.show()
Astar_GAC.Astar(state,cons)
app.exec_()