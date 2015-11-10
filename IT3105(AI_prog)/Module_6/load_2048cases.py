import numpy as np
def readfile(filename):
	f = open(filename, 'r')
	states = []
	moves = []
	for line in f.readlines():
		arr = line.split(',')
		states.append([float(i) for i in arr[:16]])
		moves.append([int(i) for i in arr[16:]])
	labels = np.array(moves)
	labels = labels.flatten()
	label_vectors = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors[np.arange(len(labels)),labels] = 1#the right answer is 1
	return(states,label_vectors)

if __name__ == '__main__':
	print("GO")
	b,m = readfile("2048training.txt")
	print (m[1])
