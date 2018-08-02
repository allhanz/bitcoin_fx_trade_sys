from pymongo import MongoClient
from read_csv_to_pandas import *
import json

def open_mongodb():
    database_info=[]
    client = MongoClient('mongodb://localhost:27017/')
    db = client["stock_database"]
    collection = db["japan_stock_collection"]
    database_info.append(client)
    database_info.append(db)
    database_info.append(collection)
    return database_info

def insert_data(data_object):
    db_info=open_mongodb()
    db=db_info[1] ##[1] db name [2] db collection
    data_list=dataFrame_to_dic(data_object)
    for data in data_list:
        posts = db.posts.insert_one(data).insert_id


def dataFrame_to_dic(data):
    dic_list_data=[]
    if type(data) is pd.core.frame.DataFrame:
        for item in data:
            x=json.loads(item.T.to_json())
            dic_list_data.append(x)
    else:
        print("data error!")
        exit()
    return dic_list_data

def find_data(search_dic_list):
    db_info=open_mongodb()
    db=db_info[1]
    search_resul=[]
    if type(search_dic_list) is list:
        for item in search_dic_list:
            data=db.posts.find_one(item)
            search_resul.append(data)
    else:
        print("data error!")
        exit()
    return search_resul

def remove_data(data_attr_list):
    db_info=open_mongodb()
    db=db_info[1]
    if type(data_attr_list) is list:
        for data in data_attr_list:
            db.delete_many(data)

'''
def update_data(data_list):
    db_info=open_mongodb()
    db=db_info[1]
    if type(data_list) is list:
        for data in data_list:
            db
'''
