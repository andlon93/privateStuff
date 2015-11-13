import numpy as np
#import State as S
def free_tiles(vector):
	antall=0
	for tile in vector:
		if tile==0: antall+=1
	return antall
#
def readfile(filename):
	f = open(filename, 'r')
	#
	state_11_free_tiles=[]
	moves_11_free_tiles=[]
	#
	state_7_free_tiles=[]
	moves_7_free_tiles=[]
	#
	state_4_free_tiles=[]
	moves_4_free_tiles=[]
	#
	for line in f.readlines():
		arr = line.split(',')
		temp_state=[float(i) for i in arr[:16]]
		temp_moves=([int(i) for i in arr[16:]])
		#
		h=max(temp_state)
		temp_state=np.array(temp_state)
		temp_state=np.divide(temp_state,h)
		#
		if free_tiles(temp_state)>10:
			state_11_free_tiles.append(temp_state)
			moves_11_free_tiles.append(temp_moves)
			#print(state_11_free_tiles)
			#print(moves_11_free_tiles)
		elif free_tiles(temp_state)>6:
			state_7_free_tiles.append(temp_state)
			moves_7_free_tiles.append(temp_moves)
		else:
			state_4_free_tiles.append(temp_state)
			moves_4_free_tiles.append(temp_moves)
	#
	labels = np.array(moves_11_free_tiles)
	labels = labels.flatten()
	label_vectors11 = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors11[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	#
	labels = np.array(moves_7_free_tiles)
	labels = labels.flatten()
	label_vectors7 = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors7[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	#
	labels = np.array(moves_4_free_tiles)
	labels = labels.flatten()
	label_vectors4 = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors4[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	return(np.array(state_11_free_tiles),label_vectors11, np.array(state_7_free_tiles),label_vectors7, np.array(state_4_free_tiles),label_vectors4,)
#
if __name__ == '__main__':
	print("GO")
	b11,m11,b7,m7,b4,m4 = readfile("2048training.txt")
	print (len(b11))
	#print (b11[0])
	print(len(b7))
	#print(b7[len(b7)-2])
	print(len(b4))
	#print(b4[len(b4)-3])
	#print(m7[37])
