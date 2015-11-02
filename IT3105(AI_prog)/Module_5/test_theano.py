import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np
from theano import pp
####--- Logistic function ---####
def log(m):
	x = T.dmatrix('x')
	print x.type
	s = 1 / (1 + T.exp(-x))
	logistic = theano.function([x], s)
	#
	s2 = (1 + T.tanh(x / 2)) / 2
	logistic2 = theano.function([x], s2)
	#
	print logistic(m)
	print logistic2(m)
#log([[0, 1], [-1, -2]])
####--- computing several outputs ---####
def multiple_outputs():
	a, b = T.dmatrices('a', 'b')
	diff = a - b
	abs_diff = abs(diff)
	diff_squared = diff**2
	f = theano.function([a, b], [diff, abs_diff, diff_squared])
	print f([[1, 1], [1, 1]], [[2, 2], [2, 2]])
#multiple_outputs()
####---  ---####
print np.random.uniform(-.1,.1,size=(0,10))
w1 = T.dscalar()
z = w1*1
f = theano.function([w1], [z])
print f([[0.1]])
#print type(w1)
#print w1.type