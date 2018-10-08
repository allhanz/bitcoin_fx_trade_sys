#########  seq2seq_attention_model.py  #####################
#website:https://qiita.com/HotAllure/items/50cf80cb1caf9c4d11fa
import os
import sys
import pandas as pd
import numpy as np

from keras import backend as K
#use tensorflow as backend
from keras.models import Sequential, Model
from keras.activations import softmax
from keras.layers.core import Dense, Activation, RepeatVector, Permute
from keras.layers import Input, Embedding, Multiply, Concatenate, Lambda
from keras.layers.recurrent import GRU,LSTM
from keras.layers import CuDNNGRU
from keras.layers.wrappers import TimeDistributed
from keras.utils.vis_utils import plot_model
#must install pydot and Graphviz
#pip install pydot 
#pip install graphvize
#apt-get install graphviz
#or yum install graphviz (website:https://nnfailagutan.wordpress.com/2012/01/28/how-to-install-graphviz-in-centos-5/)

class seq2seq_attention_model:
    #encoder
    #convert word_index into embedded vector
    def __init__(self,
                input_length=10,
                embedding_dim=100,
                num_vocab=10000,
                num_units=512,
                output_length=8):
        self.input_length=input_length
        self.num_vocab=num_vocab
        self.embedding_dim=embedding_dim
        self.num_units=num_units
        self.output_length=output_length

        self.x_train=None
        self.y_train=None
        self.x_test=None
        self.y_test=None
        self.model=self.build_model()
        print("model init process finished....")

    def load_data(self):
        pass

    def create_dataset(self):

        pass

    def model_train(self):

        pass

    def predict_val(sel):
        pass

    def plot_data(self):
        pass

    def build_model(self):
        #paper download url:https://arxiv.org/abs/1508.04025
        #fig1
        enc_in = Input(shape=(self.input_length,), dtype='int32', name='enc_input')
        enc_embedding = Embedding(input_dim=self.num_vocab,
                                    output_dim=self.embedding_dim,
                                    input_length =self.input_length,
                                    trainable = True,
                                    name='enc_embedding')
        enc_embedded  =  enc_embedding(enc_in)
        encoded, state = GRU(units=self.num_units,
                            return_sequences=True,
                            return_state=True,
                            name='enc_GRU')(enc_embedded)
        #\fig1

        ################################
        ###### decoder model ############
        ##################################

        #fig2
        dec_in = Input(shape=(self.output_length,), dtype='int32', name='dec_input')
        dec_embedding = Embedding(input_dim=self.num_vocab,
                                    output_dim=self.embedding_dim,
                                    input_length =self.output_length,
                                    trainable = True,
                                    name='dec_embedding')
        #share weights with encoder embedding layer
        dec_embedding.embeddings = enc_embedding.embeddings
        dec_embedded = dec_embedding(dec_in)
        decoded = GRU(units=self.num_units,return_sequences=True,name='dec_GRU')(dec_embedded, initial_state=state)
        #Luong's global attention
        repeat_dec = TimeDistributed(RepeatVector(self.input_length),name='repeat_dec')
        rep_decoded = repeat_dec(decoded)
        #/fig2

        #fig3
        annotation_layer = TimeDistributed(Dense(units=self.num_units),name='annotation_layer')
        annotation = annotation_layer(encoded)
        repeat_enc = TimeDistributed(RepeatVector(self.output_length),name='repeat_enc')
        rep_annotation = repeat_enc(annotation)
        rep_annotation = Permute((2,1,3),input_shape=(self.input_length,self.output_length, self.num_units),name='permute_rep_annotation')(rep_annotation)

        #fig4
        attention_mul = Multiply(name='attention_mul')
        elem_score  = attention_mul([rep_decoded, rep_annotation])
        score = Lambda(lambda x: K.sum(x, axis=3, keepdims = True), name='score')(elem_score)
        attention_weight = Lambda(lambda x: softmax(x, axis=2),name='attention_weight')(score)
        context_mul = Multiply(name='context_mul')
        #\fig4

        #fig5
        rep_encoded = repeat_enc(encoded)
        rep_encoded = Permute((2,1,3),input_shape=(self.input_length,self.output_length,self.num_units),name='permute_rep_encoded')(rep_encoded)
        elem_context = context_mul([rep_encoded, attention_weight])
        context = Lambda(lambda x: K.sum(x, axis=2), name='context')(elem_context)
        concat = Concatenate(axis=-1)
        dec_and_att = Lambda(lambda x: K.concatenate([x[0],x[1]], axis=-1), name='dec_att_concat')([decoded, context])
        #\fig5

        #full_connection and output
        #fig6
        fc1 = TimeDistributed(Dense(units=self.num_units*2), name='fc1')(dec_and_att)
        fc1_activated = Activation('tanh')(fc1)
        fc2 = TimeDistributed(Dense(units=self.num_vocab), name='fc2')(fc1_activated)
        preds = Activation('softmax', name='softmax')(fc2)
        #\fig6

        model = Model([enc_in, dec_in], preds)
        model.summary()
        plot_model(model, to_file='seq2seq_attention_model_plot.png', show_shapes=True, show_layer_names=True)
        return model



def main():
    model_ins=seq2seq_attention_model()

if __name__=="__main__":
    main()
