import numpy as np
#import State as S
def free_tiles(vector):
	antall=0
	for tile in vector:
		if tile==0: antall+=1
	return antall
#
def make_answer_vector(moves):
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
	state_6_free_tiles=[]
	moves_6_free_tiles=[]
	#
	state_4_free_tiles=[]
	moves_4_free_tiles=[]
	#
	state_3_free_tiles=[]
	moves_3_free_tiles=[]
	#
	state_2_free_tiles=[]
	moves_2_free_tiles=[]
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
		#
		if empty_tiles>11:
			state_12_free_tiles.append(temp_state)
			moves_12_free_tiles.append(temp_moves)
		if empty_tiles>9 and empty_tiles<12:
			state_10_free_tiles.append(temp_state)
			moves_10_free_tiles.append(temp_moves)
		if empty_tiles>7 and empty_tiles<10:
			state_8_free_tiles.append(temp_state)
			moves_8_free_tiles.append(temp_moves)
		if empty_tiles>5 and empty_tiles<8:
			state_6_free_tiles.append(temp_state)
			moves_6_free_tiles.append(temp_moves)
		if empty_tiles==4:
			state_4_free_tiles.append(temp_state)
			moves_4_free_tiles.append(temp_moves)
		if empty_tiles==3:
			state_3_free_tiles.append(temp_state)
			moves_3_free_tiles.append(temp_moves)
		if empty_tiles<3:
			state_2_free_tiles.append(temp_state)
			moves_2_free_tiles.append(temp_moves)
	#
	
	#
	'''labels = np.array(moves_7_free_tiles)
	labels = labels.flatten()
	label_vectors7 = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors7[np.arange(len(labels)),labels] = 1#the right answer has prob 1
	#
	labels = np.array(moves_4_free_tiles)
	labels = labels.flatten()
	label_vectors4 = np.zeros((len(labels),4))#init all vectors to zero
	label_vectors4[np.arange(len(labels)),labels] = 1#the right answer has prob 1'''
	label_vectors12=make_answer_vector(moves_12_free_tiles)
	label_vectors10=make_answer_vector(moves_10_free_tiles)
	label_vectors8=make_answer_vector(moves_8_free_tiles)
	label_vectors6=make_answer_vector(moves_6_free_tiles)
	label_vectors4=make_answer_vector(moves_4_free_tiles)
	label_vectors3=make_answer_vector(moves_3_free_tiles)
	label_vectors2=make_answer_vector(moves_2_free_tiles)
	#
	return(np.array(state_12_free_tiles),label_vectors12, 
		   np.array(state_10_free_tiles),label_vectors10,
		   np.array(state_8_free_tiles),label_vectors8,
		   np.array(state_6_free_tiles),label_vectors6,
		   np.array(state_4_free_tiles),label_vectors4,
		   np.array(state_3_free_tiles),label_vectors3,
		   np.array(state_2_free_tiles),label_vectors2,)
#
if __name__ == '__main__':
	print("GO")
	b12,m12,b10,m10,b8,m8,b6,m6,b4,m4,b3,m3,b2,m2 = readfile("2048training.txt")
	print (len(b12))
	#print (b11[0])
	print(len(b10))
	#print(b7[len(b7)-2])
	print(len(b8))
	print(len(b6))
	print(len(b4))
	print(len(b3))
	print(len(b2))
	#print(b4[len(b4)-3])
	#print(m7[37])
