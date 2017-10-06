# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:30:58 2017

@author: kshahzada
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 15:52:21 2017

@author: kshahzada
"""
import random

class player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
        
    
    def move(self, game):
        move = []
        moves = game.getAvailableSpaces(self.playerNum)
        if(len(moves)>0):
            move = random.choice(game.getAvailableSpaces(self.playerNum))
        return move