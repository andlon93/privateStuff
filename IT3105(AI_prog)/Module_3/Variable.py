import itertools
import copy
class Variable:

	domain = []
	is_row = None
	index = None
	#
	def __init__(self, is_row, index, blocks, length):
		#print "Creating variable, 111 is_row, index: ",is_row,index
		self.is_row = is_row
		self.index = index
		self.create_full_domain(blocks, length)
		#print "Creating variable, 222 is_row, index: ",is_row,index
	#
	def isValid(self,s,blocks,total_in_blocks):
		total_1s = s.count('1')
		if total_1s != total_in_blocks: # If there are more (or less) "1"s in the input string than there are supposed to, the string is invalid
			return False

		b = copy.deepcopy(blocks) # Blocks. e.g. [1,3,2]
		current_block = 0
		group_done = False
		group_started = False
		for c in s: #For character in string, aka 0 or 1
			if c == '1' and group_done == True:
				# Found a 1 when excepting a 0
				return False
			elif c == '0' and group_done == False and group_started == True:
				# Found a 0 when excpecting a 1
				return False
			elif c == '1' and group_done == False:
				# Found a 1, when looking for 1
				group_started = True
				b[current_block] = int (b[current_block]) - 1 # Decrease remaining number of 1's in the current block
				if b[current_block] == 0:			# If this is 0, it means all of the 1's in the current group has been found
					group_done    = True    		# This group of 1's is done
					group_started = False   		# There is currently no group of 1's active
					current_block += 1				# move to look for the next block of 1's
					if current_block > (len(b)-1):  # If all blocks have been found:
						return True
			elif c == '0' and group_done == True:
				# Found a 0 when excepting a 0
				group_done = False
		return True
	#
	def create_full_domain(self, blocks, n):#create the full domain
		domain = []
		total_in_blocks = 0
		for j in blocks:
			total_in_blocks += int(j)
		for x in xrange(2**n):
  			string =  ''.join(str((x>>i)&1) for i in xrange(n-1,-1,-1))
  			if self.isValid(string,blocks,total_in_blocks):
  				domain.append(string)
  		self.domain = domain

	##-- Getters --##
	def get_domain(self): return self.domain
	def get_is_row(self): return self.is_row
	def get_index(self): return self.index
