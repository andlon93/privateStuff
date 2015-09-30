import itertools
import copy
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
		for c in s: #For character in string, aka 0 or 1

			if c == '1' and done == True:
				# Found a 1 after we are supposed to have found them all.
				return False

			elif c == '1' and group_done == False:
				# Found a 1, while looking for 1
				group_started = True
				b[current_block] = int (b[current_block]) - 1 # Decrease remaining number of 1's in the current block
				if b[current_block] == 0:			# If this is 0, it means all of the 1's in the current group has been found
					group_done    = True    		# This group of 1's is done
					group_started = False   		# There is currently no group of 1's
					current_block += 1				# move to look for the next block of 1's
					if current_block > (len(b)-1):  # If all blocks have been found:
						done = True # If we find another 1 after done == True, there are too many.

			elif c == '1' and group_done == True:
				# Found a 1 when excepting a 0
				return False

			elif c == '0' and group_done == True:
				# Found a 0 when excepting a 0
				group_done = False

			elif c == '0' and group_done == False and group_started == True:
				# Found a 0 when excpecting a 1
				return False

		num_true = 0
		tot_true = 0
		for c in blocks:
			tot_true += int(c)
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
  		self.domain = domain



	##-- Getters --##
	def get_domain(self): return self.domain
	def get_is_row(self): return self.is_row
	def get_index(self): return self.index
#v = Variable(True, 0, [3,1,2], 10)
