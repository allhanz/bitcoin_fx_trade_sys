import os
import sys
import codecs
import pandas as pd
import gensim
from pyknp import Jumanpp
import env_settings as env

def create_jumanpp_obj():
    return Jumanpp()

def read_file_str(filename):
    file_str=codecs.open(filename,"r",encoding="utf-8",errors="replace").read()
    if len(file_str)>0:
        file_str=data_clean(file_str)
        return file_str

def nlp_analysis(jumanpp_obj,str_data):
    print("str_data:",str_data)
    res_str=""
    result=jumanpp_obj.analysis(str_data)
    for mrph in result.mrph_list():
        res_str=res_str+" ".join(mrph.midasi)
    if len(res_str)>=0:
        return res_str

def data_clean(str_data):
    if not isinstance(str_data,str):
        return
    target_char_list=["\t","\n"," "]
    for target in target_char_list:
        str_data=str_data.replace(target,"")
    return str_data

def remove_stop_words(str_data): #stopwords have no meaning in sentences
    jp_stopwords=list(set(pd.read_csv(env.japanese_stopword_file,encoding="utf-8").values))
    en_stopwords=list(set(pd.read_csv(env.english_stopword_file,encoding="utf-8").values))
    
    for item in jp_stopwords:
        if item in str_data:
            str_data=str_data.replace(item,"")
    for item in en_stopwords:
        if item in str_data:
            str_data=str_data.replace(item,"")
    if str_data=="":
        print("data is empty after cleaning the stopwords. please take a notice....")

    return str_data

def main():
    #for test
    print("not tested....")
    test_file=env.nlp_test_file
    file_str=read_file_str(test_file)
    nlp_engine=create_jumanpp_obj()
    res=nlp_analysis(nlp_engine,file_str)
    print("res:",res)

if __name__=="__main__":
    main()