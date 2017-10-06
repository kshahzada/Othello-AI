# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 20:57:10 2017

@author: kshahzada
"""
from Othello import othello as O
import CNN_Player
import CNN_Trainer
import pickle
import Human_Player
import Random_Player
import datetime

def playGame(player_1, player_2, verbose=False):
    val = 1
    snapshots = []
    game = O(8, False)
    while not game.isGameDone():
        if(val==1):
            move = player_1.move(game)
        else:
            move = player_2.move(game)
            
        if(len(move)>0):
            game.turn(move[0], move[1], val)    
            if(verbose):
                print("Player " + str(val) + "\t Move: ", str(move))
        elif(verbose):
            print("No move available to player " + str(val))
            
        val*=-1
        snapshots.append(game.board)
        
    
    snaps = []
    for snapshot in snapshots:
        snaps.append([snapshot, game.getScore()])
    
    winner=0
    if(game.getScore()[0]>game.getScore()[1]):
        winner = 1
    else:
        winner = -1
    return {'winner':winner, 'snaps':snaps}

def runSim(player_1, player_2, gameNumber, verbose = False):
    print("\nRunning Game Simulations")
    
    sim = []
    winCount = 0
    
    for i in range(gameNumber):
        
        gameResult = playGame(player_1, player_2, verbose)
        for snap in gameResult['snaps']:
            sim.append(snap)
            
        if(gameResult['winner']==1):
            winCount +=1
                
        print("\rSimulation Completion: " + str("{0:.2f}".format((i+1)/gameNumber*100)) + "%\tWins: " + str("{0:.2f}".format(winCount/(i+1)*100)) + "%        ", end="")         
    print("\rSimulation Completion: " + str("{0:.2f}".format((i+1)/gameNumber*100)) + "%\tWins: " + str("{0:.2f}".format(winCount/(i+1)*100)) + "%        ")
    
    return {'sim':sim, 'winCount':winCount}

def saveSim(index, sim):
    with open("simulation_"+str(index)+".pickle", 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(sim, f)
        
def loadSim(index):
    with open("simulation_"+str(index)+".pickle", 'rb') as f:  # Python 3: open(..., 'rb')
        sim = pickle.load(f)
    return sim

def trainer(startNum = 1, endNum = 40, trainSize = 500, evalSize = 50):
    evalPerc = 0.5
    print("------Trainer Started--------")
    for index in range(startNum, endNum):
        startTime = datetime.datetime.now()
        print("\n\n-------- Training Round:", str(index), "---------")
        print("\nTraining Against Self")
        player_1 = CNN_Player.player(1, index-1, learningRate = 0.1)
        player_2 = CNN_Player.player(-1, index-1, learningRate = 0.1)
        
        simData = runSim(player_1, player_2, trainSize, False)['sim']
        
        saveSim(index, simData)
        CNN_Trainer.trainIter(player_1.model, simData, index)
        
        print("\nEvaluate Against Random Player")
        player_2 = Random_Player.player(-1)
        evalWins = runSim(player_1, player_2, evalSize, False)['winCount']
        
        print("\nPerfomance Stats " 
              + "\nRound Time: " + str("{0:.2f}".format((datetime.datetime.now()-startTime).seconds/60)) 
              + "m\nIncrease in winning performance: " + str("{0:.2f}".format((evalWins/evalSize-evalPerc)*100)) +"%")
        evalPerc = evalWins/evalSize
