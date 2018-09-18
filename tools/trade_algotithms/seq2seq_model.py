import sys
import os
import keras
import seq2seq #extend fro keras
from seq2seq.models import AttentionSeq2Seq
from seq2seq.models import Seq2Seq
from seq2seq.models import SimpleSeq2Seq
sys.path.append(os.path.abspath("../"))
import env_settings as env
import redis_datatabase_api
import GPy,GPyOpt
import gpyopt_for_keras

# website
#https://github.com/farizrahman4u/seq2seq.git
class simple_seq2seq():
    def __init__(self,
        input_dim,
        input_length,
        output_dim,
        hidden_dim,
        output_length,
        depth,
        batch_size,
        epochs,
        validation_split,
        num_classes):
        
        self.input_dim=input_dim
        self.input_length=input_length
        self.hidden_dim=hidden_dim
        self.output_dim=output_dim
        self.output_length=output_length
        self.depth=depth
        self.loss_func_name="mse"
        self.optimizer_name="rmsprop"
        self.test_rate=0.2
        #the followings are common part
        self.batch_size = batch_size
        self.epochs = epochs
        self.validation_split = validation_split
        self.num_classes=num_classes
        self.baseSaveDir = env.model_file_root_path+"/simple_seq2seq_model_files/"
        self.model_file=self.baseSaveDir+"model.hdf5"
        self.model_arch=self.baseSaveDir+"model.json"
        self.best_model=self.baseSaveDir+"best_model.hdf5"
        self.best_arch=self.baseSaveDir+"best_model.json"

    def create_model_folder(self):
        if not os.path.isdir(self.baseSaveDir):
            os.makedirs(self.baseSaveDir)

    def build_train_test_data(self,input_array,output_array,test_rate):
        input_shape=input_array.shape
        self.input_dim=input_shape[1]
        output_shape=output_array.shape
        self.output_dim=output_shape.shape[1]

    def build_model(self,input_dim,hidden_dim,output_length,output_dim,depth):
        #model = SimpleSeq2Seq(input_dim=, hidden_dim=10, output_length=8, output_dim=20, depth=(4, 5))
        self.model = SimpleSeq2Seq(input_dim=self.input_dim, hidden_dim=self.hidden_dim, output_length=self.output_length, output_dim=self.output_dim, depth=self.depth)
        self.model.compile(loss='mse', optimizer='rmsprop')
    
    def run_model(self):
        self.model.fit(batch_size=self.batch_size,
            epochs=self.epochs,
            validation_split=self.validation_split)


class std_seq2seq():
    def __init__(self):
        self.input_dim=None
        self.batch_input_shape=
        self.hidden_dim=None
        self.output_length=None
        self.output_dim=None
        self.loss_func_name="mse"
        self.optimizer_name="rmsprop"
        self.gpyopt_bounds=None

def model(self,batch_input_shape,hidden_dim,output_length,output_dim,depth):
    #model = Seq2Seq(batch_input_shape=(16, 7, 5), hidden_dim=10, output_length=8, output_dim=20, depth=4)
    self.model = Seq2Seq(batch_input_shape=batch_input_shape, hidden_dim=hidden_dim, output_length=output_length, output_dim=output_dim, depth=depth)
    self.model.compile(loss='mse', optimizer='rmsprop')


def attention_seq2seq():
    def __init__(self):

    def model(self,input_dim,hidden_dim,output_length,output_dim,depth):
        #model = AttentionSeq2Seq(input_dim=5, input_length=7, hidden_dim=10, output_length=8, output_dim=20, depth=4)
        self.model = AttentionSeq2Seq(input_dim=input_dim,hidden_dim=hidden_dim,output_dim=output_dim, depth=depth)
        self.model.compile(loss='mse', optimizer='rmsprop')

def peek_seq2seq():
    def __init__(self):
        
    def model(self):
        self.model = Seq2Seq(batch_input_shape=(16, 7, 5), hidden_dim=10, output_length=8, output_dim=20, depth=4, peek=True)
        self.model.compile(loss='mse', optimizer='rmsprop')
    def 
def main():
    print("not test...")

if __name__=="__main__":
    main()
