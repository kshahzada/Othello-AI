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
    print("\nRunning Game Simulations")
    sim = []
    val = 1
    winCount = 0
    for i in range(gameNumber):
        game = O(8, False)
        snapshots = []
        
        while not game.isGameDone():     
            if(val==1):
                # Model move for player 1
                move = modelMove(model, game, val, learning_rate)
            else:
                move = modelMove(model, game, val, learning_rate)

                #move = randMove(game, val)
                
            if(len(move)>0):
                game.turn(move[0], move[1], val)      
            val*=-1
            snapshots.append(game.board)
            #else:
               #print("No moves available for player ",(val))
            #print(move, val)
           # print("-------------")
            #print(game.board)
            #print(val)
            #cycle active player
            
        for snapshot in snapshots:
            sim.append([snapshot, game.getScore()])
            
        if(game.getScore()[0]>game.getScore()[1]):
            winCount +=1
                
        if(i % 100 == 0):
            print("Simulation: ", i,"\tWin Count: ", winCount)
            #sys.stdout.write("\rSimulation: "+str(i)+"\tWin Count: "+str(winCount))
            #sys.stdout.flush()
        del game
        
#def update_progress(progress):
#    print '\r[{0}] {1}%'.format('#'*(progress/10), progress)
    print("Overall Win %: ", "{0:.2f}".format(winCount/gameNumber*100))
    return sim

def evaluate(model, gameNumber):
    print("\nEvaluating Against Random Move Player")
    winCount = 0
    for i in range(gameNumber):
        game = O(8, False)
        
        while not game.isGameDone():            
            # Model move for player 1
            move = modelMove(model, game, 1)
            if(len(move)>0):
                game.turn(move[0], move[1], 1)  
            #else:
                #print("No moves available for player ",1)
    
            # random move for player 2
            move = randMove(game, -1)
            if(len(move)>0):
                game.turn(move[0], move[1], -1)  
            #else:
                #print("No moves available for player ",2)
                
            
        if(game.getScore()[0]>game.getScore()[1]):
            winCount +=1
            
        del game
                
    print("Overall Win %: ", "{0:.2f}".format(winCount/gameNumber*100))
    
    print("\nEvaluating Against Greedy Move Player")
    winCount = 0
    for i in range(gameNumber):
        game = O(8, False)
        
        while not game.isGameDone():            
            # Model move for player 1
            move = modelMove(model, game, 1)
            if(len(move)>0):
                game.turn(move[0], move[1], 1)  
            #else:
                #print("No moves available for player ",1)         
    
            # random move for player 2
            move = randMove(game, -1)
            if(len(move)>0):
                game.turn(move[0], move[1], -1)  
            #else:
                #print("No moves available for player ",2)   
            
        if(game.getScore()[0]>game.getScore()[1]):
            winCount +=1
            
        del game

    print("Overall Win %: ", "{0:.2f}".format(winCount/gameNumber*100))

def modelMove(model, game, val, learning_rate = 0.1):
    maxMovePred = 0
    moves = game.getAvailableSpaces(val)
    # pick move
    if(len(moves)==0):
        move = []
    elif((len(moves)>0) and (random.random() < learning_rate)):
        move = random.choice(moves)
    else:
        # Find next best move
        move = moves[0]
        for option in moves[1:]:
            #print(option)
            tempBoard = O(8, False)
            tempBoard.board = game.board.copy()
            tempBoard.turn(option[0], option[1], val)
            X = numpy.asarray(tempBoard.board).reshape(1,64)
            if(val == 1):
                Y = (model.predict(X))[0][0]
                #print(Y)
            else:
                Y = (model.predict(X))[0][1]
            if(maxMovePred < Y):
                move = option
                maxMovePred = Y
    #print(val, move)
    return move
    
def randMove(game, val):
    move = []
    moves = game.getAvailableSpaces(val)
    if(len(moves)>0):
        move = random.choice(game.getAvailableSpaces(val))
    return move

def greedyMove(game, val):
    maxMoveScore = 0
    move = [];
    for option in game.getAvailableSpaces(val):
        tempBoard = game(8, False)
        tempBoard.board = game.board.copy()
        tempBoard.turn(option[0], option[1], val)
        curMoveScore = tempBoard.getScore()
        if(maxMoveScore < curMoveScore):
            move = option
            maxMoveScore = curMoveScore
    return move

def saveSim(index, sim):
    with open("simulation_"+str(index)+".pickle", 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(sim, f)
        
def loadSim(index):
    with open("simulation_"+str(index)+".pickle", 'rb') as f:  # Python 3: open(..., 'rb')
        sim = pickle.load(f)
    return sim

def trainer(startNum = 1, endNum = 40):
    print("------Trainer Started--------")
    for index in range(startNum, endNum):
        print("\n\n-------- Training Round:", str(index), "---------")
        model = CNN_Trainer.loadModel(index-1)
        simData = runIter(500, model)
        saveSim(index, simData)
        CNN_Trainer.trainIter(model, simData, index)
        evaluate(model, 25)
        del model, simData