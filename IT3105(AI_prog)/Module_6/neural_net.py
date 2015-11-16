import theano
from theano import tensor as T
import numpy as np
import load_2048cases as load
from scipy import stats
from scipy.misc import imsave
import time
import State as S
import operator
import random
#
class ANN:
    def __init__(self, lr, layers):
        self.num_layers = len(layers)
        print ("Antall lag: ",self.num_layers)
        self.lr = lr
        self.trX, self.trY = load.readfile('2048training.txt')
        #print (self.trY)
        self.teX, self.teY = load.readfile('2048test.txt')
        self.make_nn(layers)
    #
    def floatX(self,X): return np.asarray(X, dtype=theano.config.floatX)
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
    def sigmoid_model(self,X,w_h1,w_h2,w_h3,w_h4,w_h5,w_h6,w_h7,w_h8,w_h9,w_h10):
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
            h1 = T.nnet.sigmoid(T.dot(X, w_h1))
            pyx = T.nnet.softmax(T.dot(h1, w_h2))
        else: pyx = T.nnet.softmax(T.dot(X, w_h1))
        return pyx
    def tanh_model(self,X,w_h1,w_h2,w_h3,w_h4,w_h5,w_h6,w_h7,w_h8,w_h9,w_h10):
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
            h1 = T.tanh(T.dot(X, w_h1))
            pyx = T.nnet.softmax(T.dot(h1, w_h2))
        else: pyx = T.nnet.softmax(T.dot(X, w_h1))
        return pyx
    #
    def make_nn(self, layers):
        X = T.fmatrix()
        Y = T.fmatrix()
        #
        w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10 = self.init_weights(layers)
        #
        #py_x = self.tanh_model(X, w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10)
        py_x = self.sigmoid_model(X, w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10)
        y_x = T.argmax(py_x, axis=1)
        #
        cost = T.mean(T.nnet.categorical_crossentropy(py_x, Y))
        params = self.makeparamlist(w_h1, w_h2, w_h3, w_h4, w_h5, w_h6, w_h7, w_h8, w_h9, w_h10)
        updates = self.sgd(cost, params)
        #
        self.train = theano.function(inputs=[X, Y], outputs=cost, updates=updates, allow_input_downcast=True)
        self.predict = theano.function(inputs=[X], outputs=y_x, allow_input_downcast=True)
        self.predict_a_move = theano.function(inputs=[X], outputs=py_x, allow_input_downcast=True)
        #
    #
    def test_testset(self):
        return np.mean(np.argmax(self.teY, axis=1) == self.predict(self.teX))
    #
    def test_trainset(self):
        return np.mean(np.argmax(self.trY, axis=1) == self.predict(self.trX))
    #
    def training(self,numer_of_runs):
        skip = 64
        for i in range(numer_of_runs):
            start_time2=time.time()
            for start, end in zip(range(0, len(self.trX), skip), range(skip, len(self.trX), skip)):
                cost = self.train(self.trX[start:end], self.trY[start:end])
            print("--- One iteration through training set in %s seconds ---" % (time.time() - start_time2))
            score=self.test_testset()
            print("Training phase #",i," score on test-set: ", score)
            if score>41 and self.lr < 0.049:
                self.lr=self.lr*3
            elif score>0.44 and self.lr < 0.149:
                self.lr=self.lr*2
            score=self.test_trainset()
            print("Training phase #",i," score on training-set: ", score)
    #
#
def find_best_valid_move(state, moves):
    d={0:moves[0],1:moves[1],2:moves[2],3:moves[3]}
    sortert=sorted(d.items(), key=operator.itemgetter(1))
    for i in range(3,-1,-1):
        move=sortert[i][0]
        #print(move)
        if state.is_valid_move(move): return move
#
def play_random():
    state = S.State([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    state.spawn()
    while state.can_make_a_move():
        moves = [0, 1, 2, 3]
        for move in moves:
            valid_moves=[]
            if state.is_valid_move(move):
                valid_moves.append(move)
        move=moves[random.randint(0,len(moves)-1)]
        #print("move found ", move)
        state.move(move)
        state.spawn()
        #time.sleep(0.2)
    return state.get_highest_tile()
#
def play(random):
    if random:
        return play_random()
    state = S.State([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    state.spawn()
    ##
    #highest = 0
    #moves = 0
    ##
    while state.can_make_a_move():
        '''
        moves = ANN.something()
        move = find_best_valid_move(moves)
        '''
        ###########################################################
        matrix=[]
        for i in range(2):
            vector = []
            for row in state.get_board():
                for tile in row:
                    vector.append(tile)
            h=max(vector)
            vector=np.array(vector)
            vector=np.divide(vector,h)
            matrix.append(np.array(vector))
        ###########################################################
        b=nn.predict_a_move(np.array(matrix))
        #print("prob dist: ",b[0])
        move = find_best_valid_move(state,b[0])
        #print ("Move: ", move,"\n")
        #
        state.move(move)#make the move
        #
        state.spawn()#spawn a new tile
    #
    highest_tile = state.get_highest_tile()
    #print("Can not make more moves...\n", "Highest tile achieved: ", highest_tile)
    return highest_tile
#
def main(n, random):
    n64_ = 0
    n128_ = 0
    n256_ = 0
    n512_ = 0
    n1024_ = 0
    n2048_ = 0
    results=[]
    for iii in range(1,n+1):
        #state = S.State(board)
        highest_tile = play(random)
        results.append(highest_tile)
        if highest_tile == 64: n64_ += 1
        if highest_tile == 128: n128_ += 1
        elif highest_tile == 256: n256_ += 1
        elif highest_tile == 512: n512_ += 1
        elif highest_tile == 1024: n1024_ += 1
        elif highest_tile > 2047: n2048_ += 1
        #
        if iii%10 == 0:
            print (iii, " runs:")
            print ("64: ", 100.0*float(n64_)/iii, "%")
            print ("128: ", 100.0*float(n128_)/iii, "%")
            print ("256: ", 100.0*float(n256_)/iii, "%")
            print ("512: ", 100.0*float(n512_)/iii, "%")
            print ("1024: ", 100.0*float(n1024_)/iii, "%")
            print (">2047: ", 100.0*float(n2048_)/iii, "%\n")
    print (n, " runs:")
    print ("64: ", 100.0*float(n64_)/n, "%")
    print ("128: ", 100.0*float(n128_)/n, "%")
    print ("256: ", 100.0*float(n256_)/n, "%")
    print ("512: ", 100.0*float(n512_)/n, "%")
    print ("1024: ", 100.0*float(n1024_)/n, "%")
    print (">2047: ", 100.0*float(n2048_)/n, "%\n")
    return results

if __name__ == '__main__':
    print("starting up")
    runs = 50
    epochs=500
    learningRate=0.05
    #
    nn=ANN(learningRate,[(16,500),(500,4)])
    nn.training(epochs)
    #
    nn_results=main(runs,False)
    random=main(runs,True)
    print("random: ",len(random), "verdier")
    print(random)
    print("\nnevralt nett: ", len(nn_results), "verdier")
    print(nn_results,"\n")
    t_test = stats.ttest_ind(nn_results,random,equal_var=False)[1]
    poeng=-np.log10(t_test)
    print("t_test: ",t_test)
    print("Antall poeng: ",poeng)