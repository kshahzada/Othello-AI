# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 20:57:10 2017

@author: kshahzada
"""
from Othello import othello as O
import CNN_Trainer
import random
import pickle
import numpy

def runIter(gameNumber, model, learning_rate = 0.05):
    sim = []
    val = 1
    winCount = 0
    
    for i in range(gameNumber):
        game = O(8, False)
        snapshots = []
        
        while not game.isGameDone():            
            # Player move
            snapshots.append(game.board)
            count = 0
            max_i = 0
            prevMax = 0
            # Find next best move
            for option in game.getAvailableSpaces():
                tempBoard = O(8, False)
                tempBoard.board = game.board.copy()
                tempBoard.turn(option[0], option[1], 1)
                X = numpy.asarray((tempBoard.board+1)/2.0).reshape(1,64)
                Y = (model.predict(X))[0][int((val+1)/2)]
                if(prevMax < Y):
                    max_i = count
                    prevMax = Y
                count+=1
                
            # pick move
            if(random.random() < learning_rate):
                move = random.choice(game.getAvailableSpaces())
            else:
                move = (game.getAvailableSpaces())[max_i]
            
            # make move
            game.turn(move[0], move[1], val)
            
            # cycle player turn
            val*=-1
            
        for snapshot in snapshots:
            sim.append([snapshot, game.getScore()])
            
        if(game.getScore()[0]>game.getScore()[1]):
            winCount +=1
                
        if(i % 500 == 0):
            print("Simulation: ", i,"\tWin Count: ", winCount)
    print("Overall Win %: ", winCount/gameNumber)
    return sim

def evalAgainstRand(model, gameNumber):
    winCount = 0
    for i in range(gameNumber):
        game = O(8, False)
        snapshots = []
        
        while not game.isGameDone():            
            # Player move
            snapshots.append(game.board)
            count = 0
            max_i = 0
            prevMax = 0
            # Find next best move
            for option in game.getAvailableSpaces():
                tempBoard = O(8, False)
                tempBoard.board = game.board.copy()
                tempBoard.turn(option[0], option[1], 1)
                X = numpy.asarray((tempBoard.board+1)/2.0).reshape(1,64)
                Y = (model.predict(X))[0][0]
                if(prevMax < Y):
                    max_i = count
                    prevMax = Y
                count+=1
                
            #always choose best    
            move = (game.getAvailableSpaces())[max_i]
    
            # make move
            game.turn(move[0], move[1], 1)
            
            # random move for player 2
            move = random.choice(game.getAvailableSpaces())
            game.turn(move[0], move[1], -1)
            
            
        if(game.getScore()[0]>game.getScore()[1]):
            winCount +=1
                
        if(i % 10 == 0):
            print("Evalulation Against Random: ", i,"\tWin Count: ", winCount)
    print("Overall Win %: ", winCount/gameNumber)


def saveSim(index, sim):
    with open("simulation_"+str(index)+".pickle", 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(sim, f)
        
def loadSim(index):
    with open("simulation_"+str(index)+".pickle", 'rb') as f:  # Python 3: open(..., 'rb')
        sim = pickle.load(f)
    return sim

def trainer(startNum = 1, endNum = 100):
    print("------Trainer Started--------")
    for index in range(startNum, endNum):
        print("-------- Training Round:", str(index), "---------")
        model = CNN_Trainer.loadModel(index)
        simData = runIter(50, model)
        saveSim(index, simData)
        CNN_Trainer.trainIter(model, simData, index)
        evalAgainstRand(model, 100)
        del model, simData