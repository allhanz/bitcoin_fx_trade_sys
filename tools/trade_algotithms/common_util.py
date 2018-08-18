import os
import sys
from sklearn.cross_validation import train_test_split

def data_preprocess(array_X,array_Y):
    (X_train, X_test, y_train, y_test)= train_test_split( array_X, array_Y, test_size = 0.3, random_state = 100)
    return (X_train, X_test, y_train, y_test)

def main():
    print("not tested....")

if __name__=="__name__":
    main()