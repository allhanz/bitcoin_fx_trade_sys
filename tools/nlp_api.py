import os
import sys
import codecs
import pandas as pd
import gensim
from pyknp import Jumanpp

def read_file_str(filename):
    file_str=codecs.open(filename,"r",encoding="utf-8",errors="replace").readlines()
    if len(file_str)>0:
        return file_str

def data_clean(data_list):
    jp_stopwords=[]
    en_stopwords=[]

def main():
    #for test
    print("not tested....")

if __name__=="__main__":
    main()