import theano
from theano import tensor as T
import numpy as np
#from load import mnist
#from foxhound.utils.vis import grayscale_grid_vis, unit_scale
from scipy.misc import imsave
import mnist_basics as MNIST
#
class ANN:
    def __init__(self, lr, layers):
        self.num_layers = len(layers)
        print (self.num_layers)
        self.lr = lr
        self.trX, self.trY = MNIST.readfile('training')
        self.teX, self.teY = MNIST.readfile('testing')
        self.make_nn(layers)
    #
    def makeparamlist(self,w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10):
        if self.num_layers==10: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10]
        elif self.num_layers==9: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9]
        elif self.num_layers==8: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8]
        elif self.num_layers==7: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7]
        elif self.num_layers==6: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6]
        elif self.num_layers==5: return [w_h1, w_h2, w_h3, w_h4, w_h5]
        elif self.num_layers==4: return [w_h1, w_h2, w_h3, w_h4]
        elif self.num_layers==3: return [w_h1, w_h2, w_h3]
        elif self.num_layers==2: return [w_h1, w_h2]
        else: return [w_h1]
    #
    def init_weights(self,layers):
        if self.num_layers==10:
            return (theano.shared(np.random.uniform(-.1,.1,size=layers[0])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[1])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[2])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[3])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[4])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[5])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[6])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[7])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[8])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[9])))
        elif self.num_layers==9:
            return (theano.shared(np.random.uniform(-.1,.1,size=layers[0])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[1])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[2])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[3])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[4])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[5])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[6])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[7])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[8])),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))))
        elif self.num_layers==8:
            return (theano.shared(np.random.uniform(-.1,.1,size=layers[0])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[1])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[2])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[3])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[4])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[5])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[6])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[7])),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))))
        elif self.num_layers==7:
            return (theano.shared(np.random.uniform(-.1,.1,size=layers[0])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[1])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[2])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[3])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[4])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[5])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[6])),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))))
        elif self.num_layers==6:
            return (theano.shared(np.random.uniform(-.1,.1,size=layers[0])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[1])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[2])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[3])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[4])),
                theano.shared(np.random.uniform(-.1,.1,size=layers[5])),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))),
                theano.shared(np.random.uniform(-.1,.1,size=(1,1))))
        elif self.num_layers==5:
            return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=layers[1])),theano.shared(np.random.uniform(-.1,.1,size=layers[2])),theano.shared(np.random.uniform(-.1,.1,size=layers[3])),theano.shared(np.random.uniform(-.1,.1,size=layers[4])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
        elif self.num_layers==4:
            return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=layers[1])),theano.shared(np.random.uniform(-.1,.1,size=layers[2])),theano.shared(np.random.uniform(-.1,.1,size=layers[3])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
        elif self.num_layers==3:
            return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=layers[1])),theano.shared(np.random.uniform(-.1,.1,size=layers[2])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
        elif self.num_layers==2:
            return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=layers[1])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
        return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
    #
    def sgd(self,cost, params):
        grads = T.grad(cost=cost, wrt=params)
        updates = []
        for p, g in zip(params, grads):
            updates.append([p, p - g * self.lr])
        return updates
    #
    def model(self,X,w_h1,w_h2,w_h3,w_h4,w_h5,w_h6,w_h7,w_h8,w_h9,w_h10):
        if self.num_layers==10:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            h5 = T.nnet.sigmoid(T.dot(h4, w_h5))
            h6 = T.nnet.sigmoid(T.dot(h5, w_h6))
            h7 = T.nnet.sigmoid(T.dot(h6, w_h7))
            h8 = T.nnet.sigmoid(T.dot(h7, w_h8))
            h9 = T.nnet.sigmoid(T.dot(h8, w_h9))
            pyx = T.nnet.softmax(T.dot(h9, w_h10))
        elif self.num_layers==9:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            h5 = T.nnet.sigmoid(T.dot(h4, w_h5))
            h6 = T.nnet.sigmoid(T.dot(h5, w_h6))
            h7 = T.nnet.sigmoid(T.dot(h6, w_h7))
            h8 = T.nnet.sigmoid(T.dot(h7, w_h8))
            pyx = T.nnet.softmax(T.dot(h8, w_h9))
        elif self.num_layers==8:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            h5 = T.nnet.sigmoid(T.dot(h4, w_h5))
            h6 = T.nnet.sigmoid(T.dot(h5, w_h6))
            h7 = T.nnet.sigmoid(T.dot(h6, w_h7))
            pyx = T.nnet.softmax(T.dot(h7, w_h8))
        elif self.num_layers==7:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            h5 = T.nnet.sigmoid(T.dot(h4, w_h5))
            h6 = T.nnet.sigmoid(T.dot(h5, w_h6))
            pyx = T.nnet.softmax(T.dot(h6, w_h7))
        elif self.num_layers==6:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            h5 = T.nnet.sigmoid(T.dot(h4, w_h5))
            pyx = T.nnet.softmax(T.dot(h5, w_h6))
        elif self.num_layers==5:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            h4 = T.nnet.sigmoid(T.dot(h3, w_h4))
            pyx = T.nnet.softmax(T.dot(h4, w_h5))
        elif self.num_layers==4:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            h3 = T.nnet.sigmoid(T.dot(h2, w_h3))
            pyx = T.nnet.softmax(T.dot(h3, w_h4))
        elif self.num_layers==3:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
            pyx = T.nnet.softmax(T.dot(h1, w_h3))
        elif self.num_layers==2:
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            pyx = T.nnet.softmax(T.dot(h1, w_h2))
        else:
            pyx = T.nnet.softmax(T.dot(X, w_h1))
        return pyx
    #
    #
    def make_nn(self, layers):
        X = T.fmatrix()
        Y = T.fmatrix()
        #
        w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10 = self.init_weights(layers)
        #
        py_x = self.model(X, w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10)
        y_x = T.argmax(py_x, axis=1)
        #
        cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
        params = self.makeparamlist(w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10)
        print (len(params))
        updates = self.sgd(cost, params)
        #
        self.train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
        #
        for i in range(2):
            for start, end in zip(range(0, len(self.trX), 128), range(128, len(self.trX), 128)):
                cost = self.train(self.trX[start:end], self.trY[start:end])
            print (np.mean(np.argmax(self.teY, axis=1) == self.predict(self.teX)))
nn=ANN(0.1, [(784,20),(20,30),(30,40),(40,20),(20,15),(15,11),(11,11),(11,10),(10,10),(10,10)])