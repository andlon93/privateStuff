print "GO"
import Node
import State
import readfile
import time
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *

window_size_x = 500 # Window width
window_size_y = 500 # Window Height

def changeColor(circle_matrix,index,color):
	circle_matrix[index][2] = color
	return circle_matrix

def worker():
    print "sleeping 1 sec from thread"
    time.sleep(2)
    changeColor(circle_matrix,3,Qt.black)
    changeColor(circle_matrix,1,Qt.black)
    changeColor(circle_matrix,5,Qt.black)
    circles.update()

t = Thread(target=worker)
t.start()


class Draw(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height) - places and sizes the windows
        self.setGeometry(300, 100, window_size_x, window_size_y)
        self.setWindowTitle('Draw circles')
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 10
        rady = 10
        # draw red circles
        paint.setPen(Qt.red)
        for i in range (len(constraints_coordinates)):
            paint.drawLine((constraints_coordinates[i][0]*x_multi)+ abs(lowest_x)*x_multi, (constraints_coordinates[i][1]*y_multi)+ abs(lowest_y)*y_multi , (constraints_coordinates[i][2]*x_multi)+ abs(lowest_x)*x_multi , (constraints_coordinates[i][3]*y_multi)+ abs(lowest_y)*y_multi)
        
        for circle in circle_matrix:
            center = QPoint( ( circle[0] * x_multi ) + abs(lowest_x)*x_multi , (( circle[1] ) * y_multi ) + abs(lowest_y)*y_multi      ) 
            print center
            paint.setBrush(circle[2])
            paint.drawEllipse(center, radx, rady)
        paint.end()

def findLowestAndHighestValue(circle_matrix):
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
	circle_matrix = [[0 for x in xrange(3)] for x in xrange(len(state.nodes))]
	i = 0;
	for nodee in state.nodes:
		circle_matrix[i][0]=int(round(float(state.nodes[nodee].x)))
		circle_matrix[i][1]=int(round(float(state.nodes[nodee].y)))
		circle_matrix[i][2]=Qt.red
		i=i+1
	return circle_matrix
def generate_coordinates(state, cons):
	constraints_coordinates=[[0 for x in xrange(4)] for x in xrange(len(cons))] # constraints_coordinates[0][0]= node 1 - x, [0][1] =node 1 - y, [0][2] = node 2 - x, [0][3] = node 2 -y
	k=0
	for cons_pair in cons:
		constraints_coordinates[k][0] = (int(round(float(state.nodes[cons_pair[0]].x))))
		constraints_coordinates[k][1] = (int(round(float(state.nodes[cons_pair[0]].y))))
		constraints_coordinates[k][2] = (int(round(float(state.nodes[cons_pair[1]].x))))
		constraints_coordinates[k][3] = (int(round(float(state.nodes[cons_pair[1]].y))))
		k=k+1
	return constraints_coordinates

state, cons = readfile.read_graph("graph1.txt")


# Setting up lists and variables used by the GUI to draw the graph
circle_matrix = generate_circle_matrix(state)
constraints_coordinates = generate_coordinates(state, cons)
lowest_x,lowest_y,highest_x,highest_y = findLowestAndHighestValue(circle_matrix)
y_multi = ((window_size_y-100)/highest_y) 
x_multi = ((window_size_x-100)/highest_x) 


print y_multi,x_multi
print findLowestAndHighestValue(circle_matrix)


app = QApplication([])
circles = Draw()
circles.show()
app.exec_()