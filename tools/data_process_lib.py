# for data processing lib
import os
import sys
import pandas as pd
import numpy as np
import string
import hashlib
import json
from hdfs import InsecureClient

def hash_sha512(str_data):
    hash_object = hashlib.sha512(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig

def hash_sha256(str_data):
    hash_object = hashlib.sha256(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig

def convert_pd_to_jsonList(pd_data):
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_json.html
    if not pd_data.empty:
        json_str=pd_data.to_json(orient='records')
        json_list=json.loads(json_str)
        if len(json_list)>0 and isinstance(json_list[0],dict):
            return json_list
        else:
            print("json data empty....")
    else:
        print("dataframe into json error.....")

def get_digit_str(str_data):
    #keep the "." string data
    digit_str=""
    for i in str_data:
        if i!=".":
            if i.isdigit():
                digit_str=digit_str+i
        else:
            digit_str=digit_str+i
    return digit_str

def parse_int(str_data):
    digit_str=get_digit_str(str_data)
    return int(digit_str.strip(string.ascii_letters))

def main():
    str_data="asdnsc234.5,56/.?"
    #int_data=parse_int(str_data)
    #print(int_data)
    json_list=[
        {
            "name":"xasxascds",
            "age":3
        },
        {
            "name":"hanz",
            "age":10
        },
    ]
    
    pd_data=pd.DataFrame(json_list)
    print("pd_data:\n",pd_data)
    json_data=convert_pd_to_jsonList(pd_data)
    print("json_data:",json_data[0])
    print(type(json_data[0]))

if __name__=="__main__":
    main()

