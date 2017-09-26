# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 23:32:40 2017

@author: kshahzada
"""

import pickle
import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils

with open('randSim_1.pickle', 'rb') as f:
    sim = pickle.load(f)

# fix random seed for reproducibility
seed = 1
numpy.random.seed(seed)
numpy.random.shuffle(sim)

count = 0
X_train = []
y_train = []
X_test = []
y_test = []

for trial in sim:
    if(count<len(sim)*0.8):
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


# flatten 28*28 images to a 784 vector for each image
num_DOF = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_DOF).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_DOF).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = (X_train +1.0)/2.0
X_test = (X_test+1.0) / 2.0

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(num_DOF, input_dim=num_DOF, kernel_initializer='normal', activation='relu'))
	model.add(Dense(2, kernel_initializer='normal', activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# build the model
model = baseline_model()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("CNN_LARGER.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("CNN_LARGER.h5")
print("Saved model to disk")