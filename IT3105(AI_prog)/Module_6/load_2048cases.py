import numpy as np
def readfile(filename):
	f = open(filename, 'r')
	states = []
	moves = []
	for line in f.readlines():
		arr = line.split(',')
		states.append([float(i)/2048 for i in arr[:16]])
		moves.append([int(i) for i in arr[16:]])
	return(np.array(states),np.array(moves))

if __name__ == '__main__':
	b,m = readfile("2048training.txt")
	print (b[0])
