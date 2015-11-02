print ("test")
import theano
import theano.tensor as T
import theano.tensor.nnet as Tann
import numpy as np
import mnist_basics as read
###
images, labels = read.load_mnist(dataset="training", digits=np.arange(10), path="datasets/")
print ("len of images",len(images))
print ("size of image",len(images[0]), len(images[0][0]))
for row in images[0]:
	print (row)
#print labels