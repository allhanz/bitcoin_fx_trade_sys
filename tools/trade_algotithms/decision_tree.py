import os
import sys
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
#website
#http://dataaspirant.com/2017/02/01/decision-tree-algorithm-python-with-scikit-learn/

def gini_model():
    #Decision Tree Classifier with criterion gini index
    clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,max_depth=3, min_samples_leaf=5)
    return clf_gini

def entroy_model():
    #Decision Tree with Information Gain Output
    #clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,max_depth=3, min_samples_leaf=5)

    clf_entroy=DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=3,max_features=None, max_leaf_nodes=None, min_samples_leaf=5,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=100, splitter='best')
    return clf_entroy
    
##训练模型
def model_train(model_obj,x_train,y_train):
    model_obj.fit(x_train,y_train)
    return model

def trade_process():
    # 计算调仓数量
    change = {}
    for stock in account.universe:
        if y_predict>0 and stock not in account.valid_secpos:
            p = account.referencePrice[stock]
            order(stock,int(c / p))
        if y_predict==0 and stock in account.valid_secpos:
            order_to(stock,0)
    #print today,x_predict[3],y_predict

def main():
    #for test 
    print("not tested....")

if __name__=="__main__":
    main()

