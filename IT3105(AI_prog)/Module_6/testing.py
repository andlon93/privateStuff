import operator
def find_best_valid_move(moves):
	d={0:moves[0],1:moves[1],2:moves[2],3:moves[3]}
	sortert=sorted(d.items(), key=operator.itemgetter(1))
	for i in range(3,-1,-1):
		print(sortert[i][0], sortert[i][1])
		move=sortert[i][1]
		if state.is_valid_move(move):
			return move
print(find_best_valid_move([0.1, 0.3, 0.2, 0.4]))