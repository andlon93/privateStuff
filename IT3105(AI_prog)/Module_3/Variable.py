class Variable:
	domain = []
	is_row = None
	index = None
	#
	def __init__(self, is_row, index, blocks, length):
		self.is_row = is_row
		self.index = index
		self.create_full_domain(blocks, length)
	#
	def create_full_domain(self, blocks, length):#create the full domain
		n = length
		for x in range(2**n):
  			string =  ''.join(str((x>>i)&1) for i in xrange(n-1,-1,-1))
  			for block in blocks:
  				


		'''max_start_index = length + 1
		for b in blocks:
			max_start_index = max_start_index - b - 1
		print "max_start_index", max_start_index

		for start_index in xrange(max_start_index+1):
			while len(templist) < length+1:
				for block in blocks:
					for additions in xrange(block):
						templist.append(True)
					templist.append(False)
		

		self.domain = [0]'''
	##-- Getters --##
	def get_domain(self): return self.domain
	def get_is_row(self): return self.is_row
	def get_index(self): return self.index
v = Variable(True, 0, [1, 2], 5)