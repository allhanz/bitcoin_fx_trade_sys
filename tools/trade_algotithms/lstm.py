import os
import sys
import pandas as pd
import random
from datetime import datetime
import time

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers import Dropout,Flatten
from keras.layers.recurrent import LSTM
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

model_layers = [6, 50, 100, 1]

def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(input_dim=6,output_dim=model_layers[1],return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(model_layers[2],return_sequences=False))
    model.add(Dropout(0.2))
    #model.add(Flatten())
    model.add(Dense(model_layers[3]))
    #model.add(Activation("softmax"))
    model.add(Activation("linear"))
    start = time.time()
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])
    #model.compile(loss="mse", optimizer="rmsprop")
    print("Compilation Time : ", time.time() - start)
    return model

#not finished
def model(n_hidden,input_shape,in_out_neurons):
    model = Sequential()
    model.add(LSTM(n_hidden, batch_input_shape=(None, length_of_sequence, in_out_neurons), return_sequences=False))
    model.add(Dense(in_out_neurons))
    model.add(Activation("linear"))
    optimizer = Adam(lr=0.001)
    model.compile(loss="mean_squared_error", optimizer=optimizer)
    return model

"""
def model2():
    model = Sequential()
    model.add(Embedding(vocabulary, hidden_size, input_length=num_steps))
    model.add(LSTM(hidden_size, return_sequences=True))
    model.add(LSTM(hidden_size, return_sequences=True))
    if use_dropout:
        model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(vocabulary)))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    return model
"""