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
import math
#
class ANN:
    def __init__(self, lr, layers):
        self.num_layers = len(layers)
        #print ("Antall lag: ",self.num_layers+1)
        self.lr = lr
        self.train_data_11,self.train_answers_11, self.train_data_7,self.train_answers_7, self.train_data_4,self.train_answers_4=load.readfile('2048training.txt')
        #print (self.train_data_11)
        self.test_data_11,self.test_answers_11, self.test_data_7,self.test_answers_7, self.test_data_4,self.test_answers_4=load.readfile('2048test.txt')
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
    def test_testset(self,test_data,test_answers):
        return np.mean(np.argmax(test_answers, axis=1) == self.predict(test_data))
    #
    def test_trainset(self,train_data,train_answers):
    	return np.mean(np.argmax(train_answers, axis=1) == self.predict(train_data))
    #
    def training(self,skip,numer_of_runs,train_data,train_answers,test_data,test_answers):
        #skip = 1
        for i in range(numer_of_runs):
            start_time2=time.time()
            for start, end in zip(range(0, len(train_data), skip), range(skip, len(train_data), skip)):
                cost = self.train(train_data[start:end], train_answers[start:end])
            score=self.test_testset(test_data,test_answers)
            #print("Iterasjon: ",i)
            #print("Score paa test_set: ", score)
            if score>0.55 and self.lr < 0.049:
                self.lr=self.lr*3
            elif score>0.6 and self.lr < 0.149:
                self.lr=self.lr*2
        print("Score paa test set: ", self.test_testset(test_data,test_answers))
        print("Score paa training set: ",self.test_trainset(train_data,train_answers),"\n")
    #
#
def find_best_valid_move(state, moves):
    d={0:moves[0],1:moves[1],2:moves[2],3:moves[3]}
    sortert=sorted(d.items(), key=operator.itemgetter(1))
    for i in range(3,-1,-1):
        move=sortert[i][0]
        if state.is_valid_move(move): return move
#
def play_random():
    state = S.State([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    state.spawn()
    while state.can_make_a_move():
        moves = [0, 1, 2, 3]
        valid_moves=[]
        for move in moves:
            if state.is_valid_move(move):
                valid_moves.append(move)
        #
        move=valid_moves[int(round(np.random.uniform(0,len(valid_moves)-1)))]
        state.move(move)
        state.spawn()
    return state.get_highest_tile()
#
def play(random):
    if random: return play_random()
    state = S.State([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
    state.spawn()
    #
    while state.can_make_a_move():
        ###########################################################
        matrix=[]
        free_tiles=0
        for i in range(2):
            vector = []
            for row in state.get_board():
                for tile in row:
                    vector.append(tile)
                    if tile==0: free_tiles+=1
            h=max(vector)
            vector=np.array(vector)
            vector=np.divide(vector,h)
            matrix.append(np.array(vector))
        ###########################################################
        #b=nn.predict_a_move(np.array(matrix))
        if free_tiles>10: b=nn_11.predict_a_move(np.array(matrix))
        elif free_tiles>6: b=nn_7.predict_a_move(np.array(matrix))
        else: b=nn_4.predict_a_move(np.array(matrix))
        move = find_best_valid_move(state,b[0])
        #
        state.move(move)#make the move   
        state.spawn()#spawn a new tile
    #    
    highest_tile = state.get_highest_tile()
    #print("Can not make more moves...\n", "Highest tile achieved: ", highest_tile)
    return highest_tile
#
def main(n, random):
    n32_ = 0
    n64_ = 0
    n128_ = 0
    n256_ = 0
    n512_ = 0
    n1024_ = 0
    n2048_ = 0
    results=[]
    for iii in range(1,n+1):
        highest_tile = play(random)
        results.append(highest_tile)
        if highest_tile == 32: n32_ += 1
        elif highest_tile == 64: n64_ += 1
        elif highest_tile == 128: n128_ += 1
        elif highest_tile == 256: n256_ += 1
        elif highest_tile == 512: n512_ += 1
        elif highest_tile == 1024: n1024_ += 1
        elif highest_tile > 2047: n2048_ += 1
        #
    print (n, " runs:")
    print("32: ", 100.0*float(n32_)/n, "%")
    print ("64: ", 100.0*float(n64_)/n, "%")
    print ("128: ", 100.0*float(n128_)/n, "%")
    print ("256: ", 100.0*float(n256_)/n, "%")
    print ("512: ", 100.0*float(n512_)/n, "%")
    print ("1024: ", 100.0*float(n1024_)/n, "%")
    print (">2047: ", 100.0*float(n2048_)/n, "%\n")
    return results
#
if __name__ == '__main__':
    print("starting up")
    #
    tot_score = 0
    epochs=100
    learningRate=0.05
    #
    n0=0
    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    n6=0
    n7=0
    #
    for qqq in range(1,141):
        #
        training_time=time.time()
        nn_11=ANN(0.05,[(16,500),(500,4)])
        print("\nTrener nn_11:")
        nn_11.training(1,epochs,nn_11.train_data_11,nn_11.train_answers_11,nn_11.test_data_11,nn_11.test_answers_11)
        #
        nn_7=ANN(0.05,[(16,500),(500,4)])
        print("Trener nn_7:")
        nn_7.training(3,epochs,nn_7.train_data_11,nn_7.train_answers_11,nn_7.test_data_11,nn_7.test_answers_11)
        #
        nn_4=ANN(0.05,[(16,500),(500,4)])
        print("Trener nn_4:")
        nn_4.training(6,epochs,nn_4.train_data_11,nn_4.train_answers_11,nn_4.test_data_11,nn_4.test_answers_11)
        print("It took",time.time()-training_time," to train the networks")
        #
        print("\nNeural Net: ")
        nn_results=main(50,False)
        #
        print("\nRandom player: ")
        random=main(50,True)
        #
        p_value = stats.ttest_ind(nn_results,random,equal_var=False)[1]
        poeng = max(0, min(7, math.ceil(-math.log(p_value,10))))
        #
        print("\nAntall runs: ",qqq)
        print("p-value:",p_value," Points:",poeng,"\n\n")
        #
        tot_score += poeng
        if poeng==0: n0+=1
        elif poeng==1: n1+=1
        elif poeng==2: n2+=1
        elif poeng==3: n3+=1
        elif poeng==4: n4+=1
        elif poeng==5: n5+=1
        elif poeng==6: n6+=1
        elif poeng==7: n7+=1
        #
        #
        p_n0="Sans for 0 poeng: "+str(100*n0/qqq)+"%\n"
        p_n1="Sans for 1 poeng: "+str(100*n1/qqq)+"%\n"
        p_n2="Sans for 2 poeng: "+str(100*n2/qqq)+"%\n"
        p_n3="Sans for 3 poeng: "+str(100*n3/qqq)+"%\n"
        p_n4="Sans for 4 poeng: "+str(100*n4/qqq)+"%\n"
        p_n5="Sans for 5 poeng: "+str(100*n5/qqq)+"%\n"
        p_n6="Sans for 6 poeng: "+str(100*n6/qqq)+"%\n"
        p_n7="Sans for 7 poeng: "+str(100*n7/qqq)+"%"
        fil=open("results_multiple_ANNs.txt","w")
        result="Antall runs:"+str(qqq)+"\n"+p_n0+p_n1+p_n2+p_n3+p_n4+p_n5+p_n6+p_n7
        print(result)
        fil.write(result)
        fil.close()