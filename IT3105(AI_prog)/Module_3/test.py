import itertools
l = [True, True , False]
newlist = list(itertools.permutations(l))
for i in newlist:
	print i