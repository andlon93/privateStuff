import theano
from theano import tensor as T
import numpy as np
from scipy.misc import imsave
import mnist_basics as MNIST
import time
#
class ANN:
    def __init__(self, lr, layers):
        self.num_layers = len(layers)
        print ("Antall lag: ",self.num_layers+1)
        self.lr = lr
        self.trX, self.trY = MNIST.readfile('training')
        #print (self.trY[0])
        self.teX, self.teY = MNIST.readfile('testing')
        #print (self.teX[0])
        self.make_nn(layers)
    #
    def floatX(self,X): return np.asarray(X, dtype=theano.config.floatX)
    #
    def makeparamlist(self,w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10,b1,b2):
        if self.num_layers==10: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10]
        elif self.num_layers==9: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9]
        elif self.num_layers==8: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8]
        elif self.num_layers==7: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7]
        elif self.num_layers==6: return [w_h1, w_h2, w_h3, w_h4, w_h5, w_h6]
        elif self.num_layers==5: return [w_h1, w_h2, w_h3, w_h4, w_h5]
        elif self.num_layers==4: return [w_h1, w_h2, w_h3, w_h4]
        elif self.num_layers==3: return [w_h1, w_h2, w_h3]
        elif self.num_layers==2: return [w_h1, b1, w_h2, b2]
        else: return [w_h1]
    #
    def init_weights(self,layers):
        if self.num_layers==10:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[5]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[6]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[7]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[8]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[9]) * 0.01)))
        elif self.num_layers==9:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[5]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[6]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[7]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[8]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==8:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[5]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[6]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[7]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==7:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[5]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[6]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==6:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[5]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==5:
        	return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[4]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==4:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[3]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==3:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[2]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))
        elif self.num_layers==2:
            return (theano.shared(self.floatX(np.random.randn(*layers[0]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*layers[1]) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)),
                theano.shared(self.floatX(np.random.randn(*(1,1)) * 0.01)))

        return theano.shared(np.random.uniform(-.1,.1,size=layers[0])),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1))),theano.shared(np.random.uniform(-.1,.1,size=(1,1)))
    #
    def sgd(self,cost, params):
        grads = T.grad(cost=cost, wrt=params)
        updates = []
        for p, g in zip(params, grads):
            updates.append([p, p - g * self.lr])
        return updates
    #
    def sigmoid_model(self,X,w_h1,w_h2,w_h3,w_h4,w_h5,w_h6,w_h7,w_h8,w_h9,w_h10,b1,b2):
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
            pyx = T.nnet.softmax(T.dot(h2, w_h3))
        elif self.num_layers==2:
            print("using bias nodes")
            h1 = T.nnet.sigmoid(T.dot(X, w_h1)+b1)
            pyx = T.nnet.softmax(T.dot(h1, w_h2)+b2)
        else: pyx = T.nnet.softmax(T.dot(X, w_h1))
        return pyx
    def tanh_model(self,X,w_h1,w_h2,w_h3,w_h4,w_h5,w_h6,w_h7,w_h8,w_h9,w_h10, b1, b2):
        if self.num_layers==10:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            h5 = T.tanh(T.dot(h4, w_h5))
            h6 = T.tanh(T.dot(h5, w_h6))
            h7 = T.tanh(T.dot(h6, w_h7))
            h8 = T.tanh(T.dot(h7, w_h8))
            h9 = T.tanh(T.dot(h8, w_h9))
            pyx = T.nnet.softmax(T.dot(h9, w_h10))
        elif self.num_layers==9:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            h5 = T.tanh(T.dot(h4, w_h5))
            h6 = T.tanh(T.dot(h5, w_h6))
            h7 = T.tanh(T.dot(h6, w_h7))
            h8 = T.tanh(T.dot(h7, w_h8))
            pyx = T.nnet.softmax(T.dot(h8, w_h9))
        elif self.num_layers==8:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            h5 = T.tanh(T.dot(h4, w_h5))
            h6 = T.tanh(T.dot(h5, w_h6))
            h7 = T.tanh(T.dot(h6, w_h7))
            pyx = T.nnet.softmax(T.dot(h7, w_h8))
        elif self.num_layers==7:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            h5 = T.tanh(T.dot(h4, w_h5))
            h6 = T.tanh(T.dot(h5, w_h6))
            pyx = T.nnet.softmax(T.dot(h6, w_h7))
        elif self.num_layers==6:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            h5 = T.tanh(T.dot(h4, w_h5))
            pyx = T.nnet.softmax(T.dot(h5, w_h6))
        elif self.num_layers==5:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            h4 = T.tanh(T.dot(h3, w_h4))
            pyx = T.nnet.softmax(T.dot(h4, w_h5))
        elif self.num_layers==4:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            h3 = T.tanh(T.dot(h2, w_h3))
            pyx = T.nnet.softmax(T.dot(h3, w_h4))
        elif self.num_layers==3:
            h1 = T.tanh(T.dot(X, w_h1))
            h2 = T.tanh(T.dot(h1, w_h2))
            pyx = T.nnet.softmax(T.dot(h2, w_h3))
        elif self.num_layers==2:
            h1 = T.tanh(T.dot(X, w_h1)+b1)
            pyx = T.nnet.softmax(T.dot(h1, w_h2)+b2)
        else: pyx = T.nnet.softmax(T.dot(X, w_h1))
        return pyx
    #
    def make_nn(self, layers):
        X = T.fmatrix()
        Y = T.fmatrix()
        #
        w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10 = self.init_weights(layers)
        b1=theano.shared(self.floatX(np.random.uniform(-.1,.1,size=(layers[0][1]))))
        b2=theano.shared(self.floatX(np.random.uniform(-.1,.1,size=(layers[1][1]))))
        #
        py_x = self.tanh_model(X, w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10, b1, b2)
        #py_x = self.sigmoid_model(X, w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10, b1, b2)
        y_x = T.argmax(py_x, axis=1)
        #
        cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
        params = self.makeparamlist(w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10, b1, b2)
        updates = self.sgd(cost, params)
        #
        self.train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
        #
    #
    def test_testset(self):
    	return np.mean(np.argmax(self.teY, axis=1) == self.predict(self.teX))
    #
    def test_trainset(self):
    	return np.mean(np.argmax(self.trY, axis=1) == self.predict(self.trX))
    #
    def training(self,numer_of_runs):
        skip = 128
        #for i in range(numer_of_runs):
        x=True
        i=1
        while x:
            for start, end in zip(range(0, len(self.trX), skip), range(skip, len(self.trX), skip)):
                cost = self.train(self.trX[start:end], self.trY[start:end])
            score=self.test_testset()
            print("Training phase #",i," score on test-set: ", score)
            i+=1
            if score >0.97:
                x=False
        print("\n")
        print("score on test-set: ", self.test_testset())
        print("score on train-set: ", self.test_trainset())
    #
    def blind_test(self, cases):
        nn_answers = []
        cases = np.array(cases)
        cases = np.divide(cases,255)
        svar = self.predict(cases)
        for n in svar:
            nn_answers.append(n)
        print(nn_answers)
        return nn_answers
#
def main():
    training_acc = 0
    testing_acc = 0
    total_time = 0
    number_of_nets = 20
    #
    for i in range(number_of_nets):
    	training_time = time.time()
    	print ("Network #",i)
    	nn=ANN(0.05, [(784,10)])
    	nn.training(500)
    	print ("One hidden layer-> 100 nodes")
    	training_acc += nn.test_trainset()
    	testing_acc += nn.test_testset()
    	print("Test set accuracy: ", nn.test_testset())
    	print("Train set accuracy: ", nn.test_trainset())
    	total_time += (time.time() - training_time)
    print(" ")
    print("average accuracies: ")
    print("Training set: ", (training_acc/number_of_nets))
    print("Testing set: ", (testing_acc/number_of_nets))
    print("Average compute time: ", (total_time/number_of_nets))
#
nn=ANN(0.1,[(784,100),(100,10)])
start=time.time()
nn.training(50)
print("det tok: ",time.time()-start," aa trene nettet.")
MNIST.minor_demo(nn)
#blind_cases = MNIST.read_demo_file("demo_prep")
#nn.blind_test(blind_cases)