# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 23:32:40 2017

@author: kshahzada
"""
import numpy

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense


# define baseline model
def baseline_model(num_DOF=64):
	# create model
	model = Sequential()
	model.add(Dense(num_DOF, input_dim=num_DOF, kernel_initializer='normal', activation='relu'))
	model.add(Dense(2, kernel_initializer='normal', activation='softmax'))
	return model

def loadModel(index):
    # load json and create model
#    json_file = open('CNN.json', 'rb')
#    loaded_model_json = json_file.read()
#    json_file.close()
#    loaded_model = model_from_json(loaded_model_json)
    try:
        model = load_model("CNN"+str(index)+".h5")
        print("Loaded model from disk")
    except Exception as e:
        model = baseline_model()
        print(e, "\nNo model found. Creating new CNN")
    return model

def saveModel(model, index):
    # serialize model to JSON
    model_json = model.to_json()
    with open("CNN.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save("CNN_"+str(index)+".h5")
    print("Saved model to disk")

# retrain model
def retrainModel(model, simData):
    seed = 1
    numpy.random.seed(seed)
    numpy.random.shuffle(simData)
    
    count = 0
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    
    for trial in simData:
        if(count<len(simData)*0.8):
            X_train.append(trial[0])
            y_train.append([(trial[1][0]>trial[1][1])*1,(trial[1][0]<trial[1][1])*1])
        else:
            X_test.append(trial[0])
            y_test.append([(trial[1][0]>trial[1][1])*1,(trial[1][0]<trial[1][1])*1])
        count+=1
    
    # load data
    
    X_train = numpy.asarray(X_train)
    y_train = numpy.asarray(y_train)
    X_test = numpy.asarray(X_test)
    y_test = numpy.asarray(y_test)
    
    
    # flatten 8*8 board to a 64 vector for board
    num_DOF = X_train.shape[1] * X_train.shape[2]
    X_train = X_train.reshape(X_train.shape[0], num_DOF).astype('float32')
    X_test = X_test.reshape(X_test.shape[0], num_DOF).astype('float32')
    
    # normalize inputs from 0-255 to 0-1
    X_train = (X_train + 1.0) / 2.0
    X_test = (X_test + 1.0) / 2.0
    
    # Fit the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=1)
    
    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=0)
    #print("Baseline Error: %.2f%%" % (100-scores[1]*100))
        
def trainIter(model, simData, index):       
    retrainModel(model,simData)
    saveModel(index)
        