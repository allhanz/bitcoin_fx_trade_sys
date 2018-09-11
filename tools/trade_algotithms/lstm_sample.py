#checkpoint_save.py
import os
import sys
sys.path.append(os.path.abspath("../"))
import keras
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
#data process common methods




# define the deep learning model, including the train and test data and model running....
class MNIST(): # model name
    def __init__(self, first_input=784, last_output=10,l1_out=512, l2_out=512, l1_drop=0.2, l2_drop=0.2, batch_size=100, epochs=10, 
                                validation_split=0.1,num_classes=10):
        self.__first_input = first_input
        self.__last_output = last_output
        self.l1_out = l1_out
        self.l2_out = l2_out
        self.l1_drop = l1_drop
        self.l2_drop = l2_drop
        #the followings are common part
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split
        self.num_classes=num_classes
        self.baseSaveDir = "./mnist_model_files/"
        self.model_file=self.baseSaveDir+"model.hdf5"
        self.model_arch=self.baseSaveDir+"model.json"
        self.best_model=self.baseSaveDir+"best_model.hdf5"
        self.best_arch=self.baseSaveDir+"best_model.json"
        
        self.__x_train, self.__x_test, self.__y_train, self.__y_test = self.mnist_data()
        self.__model = self.build_model()
    
    def create_model_folder(self):
        if not os.path.isdir(self.baseSaveDir):
            os.makedirs(self.baseSaveDir)
    
    # load mnist data from keras dataset
    def mnist_data(self):
        # the data, shuffled and split between train and test sets
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = x_train.reshape(60000, 784)
        x_test = x_test.reshape(10000, 784)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train,self.num_classes)
        y_test = keras.utils.to_categorical(y_test,self.num_classes)
        return x_train, x_test, y_train, y_test

    def build_model(self):
        if self.best_model:
            model=load_model(self.best_model)
        elif self.model_file:
            model=load_model(self.model_file)
        else:
            model = Sequential()
            model.add(Dense(self.l1_out, input_shape=(self.__first_input,)))
            model.add(Activation('relu'))
            model.add(Dropout(self.l1_drop))
            model.add(Dense(self.l2_out))
            model.add(Activation('relu'))
            model.add(Dropout(self.l2_drop))
            model.add(Dense(self.__last_output))
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

def model_training_process(first_input=784, last_output=10,
    l1_out=512, l2_out=512, 
    l1_drop=0.2, l2_drop=0.2, 
    batch_size=100, epochs=10,
    validation_split=0.1,chkpt_file=None):

    _mnist = MNIST(first_input=first_input, last_output=last_output,
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
    gpyopt_process()

if __name__=="__main__":
    main()