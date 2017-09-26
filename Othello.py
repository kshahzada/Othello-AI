# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:27:16 2017

@author: kshahzada
"""
import numpy as np
np.set_printoptions(precision=0, threshold = float('Inf'))

class othello:
    def __init__(self, size, verbose=True):
        if(verbose):
            print("Building "+str(size)+"x"+str(size)+" Othello Board")
            
        assert (size%2==0), "Board size must be an even number!"
            
        self.board = np.zeros(shape=(size,size))
        
        self.board[int(size/2)-1,int(size/2)-1] = 1
        self.board[int(size/2),int(size/2)] = 1
        self.board[int(size/2)-1,int(size/2)] = -1
        self.board[int(size/2),int(size/2)-1] = -1
        
        if(verbose):
            print("Board Built")
    
    
    def turn(self, x, y, val):
        assert self.board[x][y]==0, "Space is already taken!"
        self.board[x][y] = val
        
    def checkAndFlip(self, dirX, dirY, posX, posY, val):
        #### needs dev
        
    def getAvailableSpaces(self):
        return np.argwhere(self.board == 0)

    def isGameDone(self):
        return len(np.argwhere(self.board == 0))==0
    
    def getScore(self):
        return [len(np.argwhere(self.board == 1)),len(np.argwhere(self.board == -1))]