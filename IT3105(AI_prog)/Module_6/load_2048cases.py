import numpy as np
import State as S
W = [
    [  [  10,    9,  7.6, 7.4],
	   [ 7.4,  6.4,  5.7, 5.3],
	   [ 4.5,  4.1,  2.7, 1.2],
	   [0.09, 0.07, 0.04, 0.02] ]   ]
#
def utility(nboard):
	board=[nboard[0:4],nboard[4:8],nboard[8:12],nboard[12:16]]
	'''max_score = 0
	for W_matrix in W:
		temp = 0
		for r in range(4):
			for c in range(4):
				temp += W_matrix[r][c]*board[r][c]
		if temp > max_score:
			max_score = temp
	#'''
#
def readfile(filename):
	f = open(filename, 'r')
	states = []
	moves = []
	for line in f.readlines():
		arr = line.split(',')
		states.append([float(i)/2048 for i in arr[:16]])
		moves.append([int(i) for i in arr[16:]])
		h=max(states[-1])
		states[-1]=np.array(states[-1])
		states[-1]=np.divide(states[-1],h)
	#
	labels = np.array(moves)
	labels = labels.flatten()
	label_vectors = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	#
	return(np.array(states),label_vectors)
#
if __name__ == '__main__':
	print("GO")
	b,m = readfile("2048training.txt")
	print (len(b[78]))
	print (b[78])
