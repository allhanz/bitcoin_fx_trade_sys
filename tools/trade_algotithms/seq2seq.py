import sys
import os
import keras
import seq2seq
from seq2seq.models import AttentionSeq2Seq
from seq2seq.models import Seq2Seq
from seq2seq.models import SimpleSeq2Seq
sys.path.append(os.path.abspath("../"))
import env_settings as env
import redis_datatabase_api

# website
#https://github.com/farizrahman4u/seq2seq.git

def simple_model(input_dim,hidden_dim,output_length,output_dim,depth):
    #model = SimpleSeq2Seq(input_dim=, hidden_dim=10, output_length=8, output_dim=20, depth=(4, 5))
    model = SimpleSeq2Seq(input_dim=input_dim, hidden_dim=hidden_dim, output_length=output_length, output_dim=output_dim, depth=depth)
    model.compile(loss='mse', optimizer='rmsprop')
    return model

def std_model(batch_input_shape,hidden_dim,output_length,output_dim,depth):
    #model = Seq2Seq(batch_input_shape=(16, 7, 5), hidden_dim=10, output_length=8, output_dim=20, depth=4)
    model = Seq2Seq(batch_input_shape=batch_input_shape, hidden_dim=hidden_dim, output_length=output_length, output_dim=output_dim, depth=depth)
    model.compile(loss='mse', optimizer='rmsprop')
    return model

def attentin_model(input_dim,hidden_dim,output_length,output_dim,depth):
    #model = AttentionSeq2Seq(input_dim=5, input_length=7, hidden_dim=10, output_length=8, output_dim=20, depth=4)
    model = AttentionSeq2Seq(input_dim=5, input_length=7, hidden_dim=10, output_length=8, output_dim=20, depth=4)
    model.compile(loss='mse', optimizer='rmsprop')
    return model
    
def main():
    print("not test...")

if __name__=="__main__":
    main()
