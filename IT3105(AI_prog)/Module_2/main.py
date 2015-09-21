print "GO"
import Node
import State
import readfile
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Draw(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 100, 650, 650)
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
        for circle in circle_matrix:
            center = QPoint(circle[0],circle[1])
            paint.setBrush(Qt.yellow)
            paint.drawEllipse(center, radx, rady)
        for i in range (len(constraints_coordinates)):
        	paint.drawLine(constraints_coordinates[i][0],constraints_coordinates[i][1],constraints_coordinates[i][2],constraints_coordinates[i][3])
        paint.drawLine(20,40,250,40)
        paint.end()


steit, cons = readfile.read_graph("graph2.txt")
circle_matrix = [[0 for x in xrange(2)] for x in xrange(len(steit.nodes))]
constraints_coordinates=[[0 for x in xrange(4)] for x in xrange(len(steit.nodes)*2)]
# constraints_coordinates[0][0]= node 1 - x, [0][1] =node 1 - y, [0][2] = node 2 - x, [0][3] = node 2 -y
multi = 7
i = 0;
for nodee in steit.nodes:
	circle_matrix[i][0]=int(round(float(steit.nodes[nodee].x)))*multi
	circle_matrix[i][1]=int(round(float(steit.nodes[nodee].y)))*multi
	i=i+1

k=0
for cons_pair in cons:
	constraints_coordinates[k][0] = int(round(float(steit.nodes[cons_pair[0]].x)))*multi
	constraints_coordinates[k][1] = int(round(float(steit.nodes[cons_pair[0]].y)))*multi
	constraints_coordinates[k][2] = int(round(float(steit.nodes[cons_pair[1]].x)))*multi
	constraints_coordinates[k][3] = int(round(float(steit.nodes[cons_pair[1]].y)))*multi
	k=k+1
print constraints_coordinates

app = QApplication([])
circles = Draw()
circles.show()
app.exec_()