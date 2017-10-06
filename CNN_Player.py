# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:52:21 2017

@author: kshahzada
"""
import random
import numpy
from Othello import othello as O
import CNN_Trainer

class player:
    def __init__(self, playerNum, index, learningRate = 0.1):
        self.playerNum = playerNum
        self.model = CNN_Trainer.loadModel(index)
        self.learningRate = learningRate
        
    
    def move(self, game):
        maxMovePred = 0
        move = []
        moves = game.getAvailableSpaces(self.playerNum)
        # pick move
        if(len(moves)==0):
            move = []
        elif((len(moves)>0) and (random.random() < self.learningRate)):
            move = random.choice(moves)
        else:
            # Find next best move
            move = moves[0]
            for option in moves[1:]:
                #print(option)
                tempBoard = O(8, False)
                tempBoard.board = game.board.copy()
                tempBoard.turn(option[0], option[1], self.playerNum)
                X = numpy.asarray(tempBoard.board).reshape(1,64)
                if(self.playerNum == 1):
                    Y = (self.model.predict(X))[0][0]
                    #print(Y)
                else:
                    Y = (self.model.predict(X))[0][1]
                if(maxMovePred < Y):
                    move = option
                    maxMovePred = Y
        #print(val, move)
        return move