import numpy as np
#import State as S
def free_tiles(vector):
	antall=0
	for tile in vector:
		if tile==0: antall+=1
	return antall
#
def make_vector(moves):
	labels = np.array(moves)
	labels = labels.flatten()
	label_vectors = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	return label_vectors
#
def readfile(filename):
	f = open(filename, 'r')
	#
	state_12_free_tiles=[]
	moves_12_free_tiles=[]
	#
	state_10_free_tiles=[]
	moves_10_free_tiles=[]
	#
	state_8_free_tiles=[]
	moves_8_free_tiles=[]
	#
	state_4_free_tiles=[]
	moves_4_free_tiles=[]
	#
	state_3_free_tiles=[]
	moves_3_free_tiles=[]
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
		empty_tiles=free_tiles(temp_state)
		if free_tiles(temp_state)>11:
			state_12_free_tiles.append(temp_state)
			moves_12_free_tiles.append(temp_moves)
			continue
		if empty_tiles>9 and empty_tiles<12:
			state_10_free_tiles.append(temp_state)
			moves_10_free_tiles.append(temp_moves)
			continue
		if empty_tiles>7 and empty_tiles<10:
			state_8_free_tiles.append(temp_state)
			moves_8_free_tiles.append(temp_moves)
			continue
		if empty_tiles>3 and empty_tiles<8:
			state_4_free_tiles.append(temp_state)
			moves_4_free_tiles.append(temp_moves)
			continue
		if empty_tiles<4:
			state_3_free_tiles.append(temp_state)
			moves_3_free_tiles.append(temp_moves)
			continue
	#
	label_vectors12=make_vector(moves_12_free_tiles)
	label_vectors10=make_vector(moves_10_free_tiles)
	label_vectors8=make_vector(moves_8_free_tiles)
	label_vectors4=make_vector(moves_4_free_tiles)
	label_vectors3=make_vector(moves_3_free_tiles)
	return(np.array(state_12_free_tiles),label_vectors12, 
		  np.array(state_10_free_tiles),label_vectors10, 
		  np.array(state_8_free_tiles),label_vectors8,
		  np.array(state_4_free_tiles),label_vectors4,
		  np.array(state_3_free_tiles),label_vectors3)
#
if __name__ == '__main__':
	print("GO")
	b12,m12,b10,m10,b8,m8,b4,m4,b3,m3= readfile("2048training_big.txt")
	print ("12:",len(b12))
	print("10:",len(b10))
	print("8:",len(b8))
	print("4:",len(b4))
	print("3:",len(b3))