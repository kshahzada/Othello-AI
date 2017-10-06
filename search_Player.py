# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:34:03 2017

@author: kshahzada
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:52:21 2017

@author: kshahzada
"""
from Othello import othello as O
import CNN_Trainer

class player:
    def __init__(self, playerNum, index, learningRate = 0.1):
        self.playerNum = playerNum
        self.model = CNN_Trainer.loadModel(index)
        self.learningRate = learningRate
        
    def move(self, game):
        maxMoveScore = 0
        move = [];
        for option in game.getAvailableSpaces(self.playerNum):
            tempBoard = O(8, False)
            tempBoard.board = game.board.copy()
            tempBoard.turn(option[0], option[1], self.playerNum)
            curMoveScore = tempBoard.getScore()
            if(maxMoveScore < curMoveScore):
                move = option
                maxMoveScore = curMoveScore
        return move