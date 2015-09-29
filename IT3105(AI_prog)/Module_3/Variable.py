<<<<<<< HEAD
import itertools
=======
import copy
>>>>>>> b34ad89372ecbf1f98b8a947793d53900ea7c1ac
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
	def isValid(self,s,blocks):

		b = copy.deepcopy(blocks) # Blocks
		current_block = 0
		group_done = False
		group_started = False
		done = False
		#print ""
		#print s

		for c in s:

			if c == '1' and done == True:
				#print "1, DONE - return false"
				return False

			elif c == '1' and group_done == False:
				#print "1, false"
				group_started = True
				b[current_block] = b[current_block] - 1
				if b[current_block] == 0:
					group_done = True
					group_started = False
					current_block += 1
					if current_block > (len(b)-1):
						done = True

			elif c == '1' and group_done == True:
				# print "Fant 1, skulle vare 0"
				return False

			elif c == '0' and group_done == True:
				#print 'goup done: false og c == 0'
				group_done = False

			elif c == '0' and group_done == False and group_started == True:
				# print "c0 og group_done false"
				return False

		num_true = 0
		tot_true = 0
		for c in blocks:
			tot_true += c

		for c in s:
			if c == '1':
				num_true += 1

		#print "num_true, tot_true: ",num_true,tot_true
		if (tot_true!=num_true):
			return False
		return True
	#
	def create_full_domain(self, blocks, length):#create the full domain
		domain = []
		n = length
		for x in range(2**n):
  			string =  ''.join(str((x>>i)&1) for i in xrange(n-1,-1,-1))
  			if self.isValid(string,blocks):
  				domain.append(string)
  		print "Domain length", len(domain)
	##-- Getters --##
	def get_domain(self): return self.domain
	def get_is_row(self): return self.is_row
	def get_index(self): return self.index
v = Variable(True, 0, [1,2], 10)
