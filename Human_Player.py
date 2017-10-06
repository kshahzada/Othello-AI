# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:10:47 2017

@author: kshahzada
"""

class player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
    
    def move(self, game):
        move = []
        game.printBoard()
        moves = game.getAvailableSpaces(self.playerNum)
        self.printMoves(moves)
        move = moves[int(input("Pick a move (type index): "))]
        return move
    
    def printMoves(self, moves):
        print("Moves Available:")
        for move in moves:
            print(move[0], ", ", move[1])