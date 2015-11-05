import theano
from theano import tensor as T
import numpy as np
#from load import mnist
#from foxhound.utils.vis import grayscale_grid_vis, unit_scale
from scipy.misc import imsave
import mnist_basics as MNIST
#
class ANN:
    def __init__(self):
        self.trX, self.trY = MNIST.readfile('training')
        self.teX, self.teY = MNIST.readfile('testing')
        self.make_nn()
    def floatX(self,X):
        return np.asarray(X, dtype=theano.config.floatX)
    #
    def init_weights(self,shape):
        return theano.shared(self.floatX(np.random.randn(*shape) * 0.01))

    def sgd(self,cost, params, lr=0.05):
        grads = T.grad(cost=cost, wrt=params)
        updates = []
        for p, g in zip(params, grads):
            updates.append([p, p - g * lr])
        return updates
    #
    def model(self,X, w_h1, w_h2, w_o):
        h1 = T.nnet.sigmoid(T.dot(X, w_h1))
        h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
        pyx = T.nnet.softmax(T.dot(h2, w_o))
        return pyx
    #
    def make_nn(self):
        X = T.fmatrix()
        Y = T.fmatrix()
        #
        layer_1 = 625
        layer_2 = 300
        w_h1 = self.init_weights((784, layer_1))
        w_h2 = self.init_weights((layer_1, layer_2))
        w_o = self.init_weights((layer_2, 10))
        #
        py_x = self.model(X, w_h1, w_h2, w_o)
        y_x = T.argmax(py_x, axis=1)
        #
        cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
        params = [w_h1, w_h2, w_o]
        updates = self.sgd(cost, params)
        #
        #print("hey")
        self.train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
        #print("heyhey")
        
        for i in range(100):
            for start, end in zip(range(0, len(self.trX), 128), range(128, len(self.trX), 128)):
                cost = self.train(self.trX[start:end], self.trY[start:end])
            print (np.mean(np.argmax(self.teY, axis=1) == self.predict(self.teX)))
nn=ANN()