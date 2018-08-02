# the example for study
# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from read_csv_to_pandas import *
f_model="./ML_model"

def build_ML_model():

    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)

    # load pima indians dataset
    dataset = np.loadtxt("./test_data/pima-indians-diabetes.csv", delimiter=",")
    print()
    # split into input (X) and output (Y) variables
    X = dataset[:,0:8]
    Y = dataset[:,8]

    # create model
    model = Sequential()
    model.add(Dense(20, input_dim=8, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(X, Y, nb_epoch=200, batch_size=10,  verbose=2)

    # evaluate the model
    scores = model.evaluate(X, Y)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    # calculate predictions
    predictions = model.predict(X)

    # round predictions
    #rounded = [round(x) for x in predictions]
    rounded = np.round(predictions)
    print(len(rounded))

def save_trained_ML_model(model_data,file_name):

def load_ML_model(model_data,file_name):
    print("not implemented!!")

if __name__=="__main__":
    build_ML_model()
