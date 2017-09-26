# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 20:57:10 2017

@author: kshahzada
"""
from Othello import othello as O
import random
import pickle

sim = []

def runSim(gameNumber):
    global sim
    sim = []
    val = 1
    
    for i in range(gameNumber):
        game = O(8, False)
        snapshots = []
        while not game.isGameDone():
            snapshots.append(game.board)
            move = random.choice(game.getAvailableSpaces())
            game.turn(move[0], move[1], val)
            val*=-1
        for snapshot in snapshots:
            sim.append([snapshot, game.getScore()])
        if(i % 1000 == 0):
            print("Simulation: ", i)
   
def saveSim(filename='objs.pickle'):
    global sim
    with open(filename, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(sim, f)
        
def loadSim(filename='objs.pickle'):
    global sim
    with open(filename, 'rb') as f:  # Python 3: open(..., 'rb')
        sim = pickle.load(f)