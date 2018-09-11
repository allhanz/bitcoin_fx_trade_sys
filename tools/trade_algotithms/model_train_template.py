#template.py
#the model define template and the
import os
import sys
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout,Activation,BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import np_utils
from keras.optimizers import Adam,RMSprop
import GPy, GPyOpt
import random
#cross_validation
from sklearn.model_selection import cross_val_score,KFold,GridSearchCV,StratifiedShuffleSplit,StratifiedKFold
#GridSearchCV
from sklearn import preprocessing

 class model_name():
    def __init__(self,*params):
        self.init_param1=None
        self.init_param1=None
        self.init_param1=None
        self.init_param1=None
        self.init_param1=None
        self.init_param1=None
        #common param of the deep learning model
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split
        self.model_file=None
        self.baseSaveDir=__name__
        self.best_model="best_model.hdf5"
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = self.load_data()
        self.__model = self.build_model()


    def load_data(self,*params):
        #define the data preprocess
        pass

    def build_model(self,*params):
        #define the model achitectire
        # if self.model_file, load the model file

    def model_fit(self,chkpt_file=None):
    #not changeable
        es_cb = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
        if chkpt_file=="" or chkpt_file==None:
            chkpt_file = os.path.join(baseSaveDir, 'MNIST_.{epoch:1000d}-{val_loss:.6f}.hdf5')

        cp_cb = ModelCheckpoint(filepath = chkpt_file, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
        self.__model.fit(self.__x_train,self.__y_train,
                        batch_size=self.batch_size,
                        epochs=self.epochs,
                        verbose=1,
                        validation_data=(self.__x_test,self.__y_test),
                        callbacks=[es_cb,cp_cb],
                        shuffle=True)

    def evaluate_model(self,chkpt_file):
    # not changeable
        self.model_fit(chkpt_file)
        evaluation = self.__model.evaluate(self.__x_test, self.__y_test, batch_size=self.batch_size, verbose=0)
        return evaluation


def model_training_process(*params,chkpt_file=None):
#define the model class
    $_model_name = model_name(*params)
    $model_evaluation = $_model_name.evaluate_model(chkpt_file)
    return $model_evaluation

def f_map(x):
#parameter optimization function
    print(x)
    evaluation = model_training_process(
    #gpyopt_bounds mapping ))
    print("loss:{0} \t\t accuracy:{1}".format(evaluation[0], evaluation[1]))
    print(evaluation)
    return evaluation[0]

def gpyopt_process():
    gpy_bounds=[
                {'name': '??', 'type': 'continuous/discrete',  'domain': (XX, XX)},
                {'name': '??', 'type': 'continuous/discrete',  'domain': (XX, XX)},
                {'name': '??', 'type': 'continuous/discrete',  'domain': (XX, XX)},
                ]
    opt_mnist = GPyOpt.methods.BayesianOptimization(f=f_map, domain=gpy_bounds)
    # 最適なパラメータを探索します。
    opt_mnist.run_optimization(max_iter=1)
    print("optimized parameters: {0}".format(opt_mnist.x_opt))
    print("optimized loss: {0}".format(opt_mnist.fx_opt))
    x_opt=opt_mnist.x_opt
    #get the optimized model paramter, training the model
    model_training_process(validation_split=x_opt[0],
                l1_drop=x_opt[1],
                l2_drop=x_opt[2],
                l1_out=x_opt[3],
                l2_out=x_opt[4],
                batch_size=x_opt[5],
                epochs=x_opt[6]),
                chkpt_file="best_model.hdf5")


def main():
    print("testing .....")
    gpyopt_process()

if __name__=="__main__":
    main()
