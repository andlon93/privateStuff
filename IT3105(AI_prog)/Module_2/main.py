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
fit_to_windows = False

def worker():
    while True:
    	time.sleep(0.01) # This, for some reason, is how often the GUI will be drawn. processEvent() is required in the algorithm to make this work...
    	circles.update()
t = Thread(target=worker)
t.start()

class Draw(QWidget):
	# All the GUI stuff is done within this class
	# paintEvent is the function that draws the GUI - this is called by the "worker" thread
	# The "worker" thread also needs "processEvents()" to be called by the algorithm, this makes the GUI thread work
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height) - places and sizes the windows
        self.setGeometry(300, 100, window_size_x, window_size_y)
        self.setWindowTitle('Astar_GAC')

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing) # AA makes lines smooth
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect()) # make a white drawing background
        paint.setPen(Qt.red) # Color of the edges(lines)
        for i in range (len(constraints_coordinates)):
        	paint.drawLine((constraints_coordinates[i][0]*x_multi)+ abs(lowest_x)*x_multi, (constraints_coordinates[i][1]*y_multi)+ abs(lowest_y)*y_multi , (constraints_coordinates[i][2]*x_multi)+ abs(lowest_x)*x_multi , (constraints_coordinates[i][3]*y_multi)+ abs(lowest_y)*y_multi)
			#paint.drawLine(constraints_coordinates[i][0], constraints_coordinates[i][1], constraints_coordinates[i][2], constraints_coordinates[i][3]) # To remove the scaling of the gui, replace the line above with this
        for circle in circle_matrix:
            center = QPoint( ( circle[0] * x_multi ) + abs(lowest_x)*x_multi , (( circle[1] ) * y_multi ) + abs(lowest_y)*y_multi) 
            #center = QPoint( ( circle[0]), (( circle[1] )))  # To remove the scaling of the gui, replace the line above with this
            paint.setBrush(circle[2]) 
            paint.drawEllipse(center, 10, 10) # arguments 2 and 3 are the size of the circles, in x and y direction. Argument 1 is the placement, also containing x and y
        paint.end()

def findLowestAndHighestValues(circle_matrix):
    lowest_x = 0
    lowest_y = 0
    highest_x = 0
    highest_y = 0
    for node in circle_matrix:
        if (node[0])>highest_x:
            highest_x = node[0]
        if ( node[0]<lowest_x):
            lowest_x = node[0]
        if (node[1])>highest_y:
            highest_y = node[1]
        if ( node[1]<lowest_y):
            lowest_y = node[1]
    return lowest_x,lowest_y,highest_x,highest_y

def generate_circle_matrix(state):
	color = Qt.white
	circle_matrix = [[0 for x in xrange(3)] for x in xrange(len(state.nodes))]
	i = 0;
	for node in state.nodes:
		circle_matrix[i][0]=int(round(float(state.nodes[node].x)))
		circle_matrix[i][1]=int(round(float(state.nodes[node].y)))
		domain = state.nodes[node].domain
		if (len(domain) > 1):
			color=Qt.white
		elif (len(domain)==1):
			if domain[0] == 0:
				color=Qt.red
			elif domain[0] == 1:
				color = Qt.magenta
			elif domain[0] == 2:
				color = Qt.yellow
			elif domain[0] == 3:
				color = Qt.black
			elif domain[0] == 4:
				color = Qt.gray
			elif domain[0] == 5:
				color = Qt.darkBlue
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

state, cons = readfile.read_graph("graph5.txt")

# Setting up lists and variables used by the GUI to draw the graph
circle_matrix = generate_circle_matrix(state)
constraints_coordinates = generate_coordinates(state, cons)
lowest_x,lowest_y,highest_x,highest_y = findLowestAndHighestValues(circle_matrix)
y_multi = ((window_size_y-100)/highest_y) 
x_multi = ((window_size_x-100)/highest_x) 

print x_multi,y_multi
print lowest_x,lowest_y,highest_x,highest_y

#PyQt stuff
app = QApplication([])
circles = Draw()
circles.show()

Astar_GAC.Astar(state,cons)
app.exec_()
# sys.exit(app.exec_())