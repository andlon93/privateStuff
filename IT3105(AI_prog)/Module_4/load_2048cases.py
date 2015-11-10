def readfile(filename):
	f = open(filename, 'r')
	states = []
	moves = []
	for line in f.readlines():
		arr = line.split(',')
		states.append(map(int, arr[0:16]))
		moves.append(map(int, arr[16:]))
	return(states,moves)

if __name__ == '__main__':
	b,m = readfile("2048training.txt")
	print (m)
