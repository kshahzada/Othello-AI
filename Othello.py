# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 20:27:16 2017

@author: kshahzada
"""
import numpy as np
np.set_printoptions(precision=0, threshold = float('Inf'))

class othello:
    def __init__(self, size, verbose=True):
        self.size = size
        self.verbose = verbose
        if(self.verbose):
            print("Building "+str(size)+"x"+str(size)+" Othello Board")
            
        assert (size%2==0), "Board size must be an even number!"
            
        self.board = np.zeros(shape=(size,size))
        
        self.board[int(size/2)-1,int(size/2)-1] = 1
        self.board[int(size/2),int(size/2)] = 1
        self.board[int(size/2)-1,int(size/2)] = -1
        self.board[int(size/2),int(size/2)-1] = -1
        
        if(self.verbose):
            print("Board Built")
    
    
    def turn(self, x, y, val):
        assert abs(val)==1, "Invalid Player Selected!"
        assert self.board[x][y]==0, "Space is already taken!"
        self.board[x][y] = val
        self.checkAndFlip(1, 0, x, y, val)
        self.checkAndFlip(0, 1, x, y, val)
        self.checkAndFlip(-1, 0, x, y, val)
        self.checkAndFlip(0, -1, x, y, val)
        self.checkAndFlip(1, 1, x, y, val)
        self.checkAndFlip(-1, -1, x, y, val)
        self.checkAndFlip(1, -1, x, y, val)
        self.checkAndFlip(-1, 1, x, y, val)


        
        if(self.verbose):
            self.printBoard()
        
    def checkAndFlip(self, dirX, dirY, posX, posY, val):
        posX = posX + dirX
        posY = posY + dirY
        if((posX >= self.size or posX < 0) or (posY >= self.size or posY < 0) or (self.board[posX][posY]==0)):
            return False
        
        if(self.board[posX][posY] == val):
            return True
        
        if(self.checkAndFlip(dirX, dirY, posX, posY, val)):
            self.board[posX][posY] = val
            return True
        else:
            return False
        
    def getAvailableSpaces(self):
        return np.argwhere(self.board == 0)

    def isGameDone(self):
        return len(np.argwhere(self.board == 0))==0
    
    def getScore(self):
        return [len(np.argwhere(self.board == 1)),len(np.argwhere(self.board == -1))]
    
    def printBoard(self):          
        outString = ""
        for i in reversed(range(0, self.size)):
            for j in (range(0, self.size)):
                if(self.board[j][i]>-1):
                    outString += " "
                outString += " " '{0:g}'.format(self.board[j][i])+" "
            outString += "\n"
        print(outString)

                