#checkpoint_save.py
import os
import sys
sys.path.append(os.path.abspath("../"))
import keras
import env_settings as env
from keras.datasets import mnist
from keras.models import Sequential,model_from_json,load_model
from keras.layers import Dense, Dropout,Activation,BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import np_utils
from keras.optimizers import Adam,RMSprop
import GPy, GPyOpt
import random
#cross_validation
from sklearn.model_selection import cross_val_score,KFold,GridSearchCV,StratifiedShuffleSplit,StratifiedKFold
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from subprocess import check_output
import common_util
from numpy import newaxis
import numpy as np
from keras.utils import to_categorical
#data process common methods

# define the deep learning model, including the train and test data and model running....
class MNIST(): # model name
    def __init__(self, input_shape=(None,1), output_num=1,l1_out=512, l2_out=512, l1_drop=0.2, l2_drop=0.2, batch_size=100, epochs=10, 
                                validation_split=0.1,num_classes=10):
        self.__input_shape = input_shape
        self.__output_num = output_num
        self.l1_out = l1_out
        self.l2_out = l2_out
        self.l1_drop = l1_drop
        self.l2_drop = l2_drop
        #the followings are common part
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split
        self.num_classes=num_classes
        self.baseSaveDir =os.path.abspath(env.model_file_root_path+"/mnist_model_files/")
        self.model_file=self.baseSaveDir+"model.hdf5"
        self.model_arch=self.baseSaveDir+"model.json"
        self.best_model=self.baseSaveDir+"best_model.hdf5"
        self.best_arch=self.baseSaveDir+"best_model.json"
        self.redis_scan_ptn="bitflyer_bitcoin_price_[0-9]*"
        self.realtime_data_pd=None
        self.target_col=["time","buy_price"]
        self.__x_train=None
        self.__x_test=None
        self.__y_train=None
        self.__y_test=None
        self.__model = self.build_model()
        self.create_model_folder()
        print('model init process finished....')

    def create_model_folder(self):
        if not os.path.isdir(self.baseSaveDir):
            os.makedirs(self.baseSaveDir)

    # load mnist data from keras dataset
    def load_data(self):
        pd_data=common_util.load_realtime_data(self.redis_scan_ptn)
        #realtime_data_pd=pd_data.copy()
        realtime_data_pd=common_util.bitflyer_data_preprocess(pd_data,self.target_col)
        print('data length:',len(realtime_data_pd))
        print("realtime head data:",realtime_data_pd.head())
        ordered_pd=realtime_data_pd.sort_values(by=["time"])
        print('ordered data head:',ordered_pd.head())
        self.realtime_data_pd=ordered_pd

    def train_data_builder(self):
        self.load_data()
        train_data=self.realtime_data_pd['buy_price'].values
        dataX,dataY=common_util.create_dataset(train_data[:,newaxis],look_back=100)
        trainX = np.reshape(dataX, (dataX.shape[0], dataX.shape[1],1))
        #scaler = MinMaxScaler(feature_range=(0, 1))
        #scaled_data=scaler.fit_transform(ordered_pd.values)
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = train_test_split(trainX, dataY, test_size=self.validation_split, random_state=42)
        print('length of __x_train:',len(self.__x_train))
        print('length of __y_train:',len(self.__y_train))
        print('length of __x_test:',len(self.__x_test))
        print('length of __y_test:',len(self.__y_test))       
        print('shape of __x_train:',self.__x_train.shape)
        print('shape of __y_train:',self.__y_train.shape)

    def build_model(self):
        if os.path.exists(self.best_model):
            model=load_model(self.best_model)
        elif os.path.exists(self.model_file):
            model=load_model(self.model_file)
        else:
            model = Sequential()
            model.add(Dense(self.l1_out, input_shape=self.__input_shape))
            model.add(Activation('relu'))
            model.add(Dropout(self.l1_drop))
            model.add(Dense(self.l2_out))
            model.add(Activation('relu'))
            model.add(Dropout(self.l2_drop))
            model.add(Dense(self.__output_num))
            model.add(Activation('softmax'))
            model.compile(loss='categorical_crossentropy',optimizer=Adam(),metrics=['accuracy'])

        return model

    def model_fit(self,chkpt_file=None):

        es_cb = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
        if chkpt_file=="" or chkpt_file==None:
            chkpt_file = os.path.join(self.baseSaveDir, 'MNIST_.{epoch:02d}-{val_loss:.6f}.hdf5')

        cp_cb = ModelCheckpoint(filepath = chkpt_file, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
        self.__model.fit(self.__x_train,self.__y_train,
                        batch_size=self.batch_size,
                        epochs=self.epochs,
                        verbose=1,
                        validation_data=(self.__x_test,self.__y_test),
                        callbacks=[es_cb,cp_cb],
                        shuffle=True)

    def evaluate_model(self,chkpt_file):
        self.model_fit(chkpt_file)
        evaluation = self.__model.evaluate(self.__x_test, self.__y_test, batch_size=self.batch_size, verbose=0)
        return evaluation

def f_map(x):
    print(x)
    evaluation = model_training_process(
                l1_drop = float(x[:,1]), 
                l2_drop = float(x[:,2]), 
                l1_out = int(x[:,3]),
                l2_out = int(x[:,4]), 
                batch_size = int(x[:,5]), 
                epochs = int(x[:,6]), 
                validation_split = float(x[:,0]))
    print("loss:{0} \t\t accuracy:{1}".format(evaluation[0], evaluation[1]))
    print(evaluation)
    return evaluation[0]

def model_training_process(input_shape=(None,1), output_num=1,
    l1_out=512, l2_out=512, 
    l1_drop=0.2, l2_drop=0.2, 
    batch_size=100, epochs=10,
    validation_split=0.1,chkpt_file=None):

    _mnist = MNIST(input_shape=input_shape, output_num=output_num,
                                        l1_out=l1_out, l2_out=l2_out, 
                                        l1_drop=l1_drop, l2_drop=l2_drop, 
                                        batch_size=batch_size, epochs=epochs, 
                                        validation_split=validation_split)
    mnist_evaluation = _mnist.evaluate_model(chkpt_file)
    return mnist_evaluation


def gpyopt_process():
    gpy_bounds=[
                {'name': 'validation_split', 'type': 'continuous',  'domain': (0.0, 0.3)},
                {'name': 'l1_drop',          'type': 'continuous',  'domain': (0.0, 0.3)},
                {'name': 'l2_drop',          'type': 'continuous',  'domain': (0.0, 0.3)},
                {'name': 'l1_out',           'type': 'discrete',    'domain': (64, 128, 256, 512, 1024)},
                {'name': 'l2_out',           'type': 'discrete',    'domain': (64, 128, 256, 512, 1024)},
                {'name': 'batch_size',       'type': 'discrete',    'domain': (10, 100, 500)},
                {'name': 'epochs',           'type': 'discrete',    'domain': (5, 10, 20)}
            ]
    opt_mnist = GPyOpt.methods.BayesianOptimization(f=f_map, domain=gpy_bounds)
    # 最適なパラメータを探索します。
    opt_mnist.run_optimization(max_iter=1)
    print("optimized parameters: {0}".format(opt_mnist.x_opt))
    print("optimized loss: {0}".format(opt_mnist.fx_opt))
    x_opt_str=opt_mnist.x_opt
    #get the optimized model paramter, training the model
    #x_opt=[data_process_lib.parse_int()]
    #model_training_process(validation_split=x_opt[0],l1_drop=x_opt[1],l2_drop=x_opt[2],l1_out=x_opt[3],l2_out=x_opt[4],batch_size=x_opt[5],epochs=x_opt[6],chkpt_file="best_model.hdf5")


def main():
    print("testing .....")
    #gpyopt_process()
    lstm_model=MNIST()
    lstm_model.load_data()
    lstm_model.train_data_builder()
    lstm_model.model_fit()
    
if __name__=="__main__":
    main()