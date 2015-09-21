print "GO"
import Node
import State
import readfile
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

window_size_x = 1000
window_size_y = 1000

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
            paint.setBrush(Qt.yellow)
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

steit, cons = readfile.read_graph("graph5.txt")
circle_matrix = [[0 for x in xrange(2)] for x in xrange(len(steit.nodes))]

constraints_coordinates=[[0 for x in xrange(4)] for x in xrange(len(steit.nodes)*10)] # HVORFOR 10???? gange med seg selv? kan jo ikke vare mer enn noder * noder
# constraints_coordinates[0][0]= node 1 - x, [0][1] =node 1 - y, [0][2] = node 2 - x, [0][3] = node 2 -y

i = 0;
for nodee in steit.nodes:
	circle_matrix[i][0]=int(round(float(steit.nodes[nodee].x)))
	circle_matrix[i][1]=int(round(float(steit.nodes[nodee].y)))
	i=i+1

lowest_x,lowest_y,highest_x,highest_y = findLowestAndHighestValue(circle_matrix)
y_multi = ((window_size_y-100)/highest_y) 
x_multi = ((window_size_x-100)/highest_x) 
print y_multi,x_multi
print findLowestAndHighestValue(circle_matrix)


k=0
for cons_pair in cons:
	constraints_coordinates[k][0] = (int(round(float(steit.nodes[cons_pair[0]].x))))
	constraints_coordinates[k][1] = (int(round(float(steit.nodes[cons_pair[0]].y))))
	constraints_coordinates[k][2] = (int(round(float(steit.nodes[cons_pair[1]].x))))
	constraints_coordinates[k][3] = (int(round(float(steit.nodes[cons_pair[1]].y))))
	k=k+1
#print constraints_coordinates

app = QApplication([])
circles = Draw()
circles.show()
app.exec_()