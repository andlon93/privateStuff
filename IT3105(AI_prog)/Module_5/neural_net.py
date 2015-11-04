import theano
from theano import tensor as T
import numpy as np
#from load import mnist
#from foxhound.utils.vis import grayscale_grid_vis, unit_scale
from scipy.misc import imsave
import mnist_basics as MNIST
#
def floatX(X):
    return np.asarray(X, dtype=theano.config.floatX)
#
def init_weights(shape):
    return theano.shared(floatX(np.random.randn(*shape) * 0.01))

def sgd(cost, params, lr=0.05):
    grads = T.grad(cost=cost, wrt=params)
    updates = []
    for p, g in zip(params, grads):
        updates.append([p, p - g * lr])
    return updates
#
def model(X, w_h1, w_h2, w_o):
    h1 = T.nnet.sigmoid(T.dot(X, w_h1))
    h2 = T.nnet.sigmoid(T.dot(h1, w_h2))
    pyx = T.nnet.softmax(T.dot(h2, w_o))
    return pyx
#
#trX, teX, trY, teY = mnist(onehot=True)
trX, trY = MNIST.readfile('training')
teX, teY = MNIST.readfile('testing')
#
X = T.fmatrix()
Y = T.fmatrix()
#
layer_1 = 625
layer_2 = 300
w_h1 = init_weights((784, layer_1))
w_h2 = init_weights((layer_1, layer_2))
w_o = init_weights((layer_2, 10))
#
py_x = model(X, w_h1, w_h2, w_o)
y_x = T.argmax(py_x, axis=1)
#
cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
params = [w_h1, w_h2, w_o]
updates = sgd(cost, params)
#
train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
#
for i in range(100):
    for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
        cost = train(trX[start:end], trY[start:end])
    print (np.mean(np.argmax(teY, axis=1) == predict(teX)))