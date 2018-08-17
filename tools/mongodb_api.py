import os
import sys
import pandas
import pymongo
from pymongo import MongoClient
from pprint import pprint
from bson.objectid import ObjectId

"""
NOTICE:
This tutorial also assumes that a MongoDB instance is running on the default host and port. Assuming you have downloaded and installed MongoDB, you can start it like so:
run command:
$ mongod
"""
def build_db_Client(server_name,port_no):
    if server_name=="" or server_name==None:
            server_name="localhost"
    if port_no==None:
        port_no=27017

    #client = MongoClient()
    client = MongoClient(server_name, port_no)
    if client:
        return client
    else:
        print("build client error....")

def build_one_document(collection_obj,docu_name):
    return collection_obj[docu_name]

def build_many_document(collection_name,docu_name_list):
    docu_obj_list=[]
    for docu_name in docu_name_list:
        docu_obj=collection_name[docu_name]
        if docu_obj:
            docu_obj_list.append(docu_obj)
    if len(docu_name_list)>0:
        return docu_name_list

def build_one_database(db_name,server_name,port_no):
    client=build_db_Client(server_name,port_no)
    db=client[db_name]
    return db

def build_multi_database(db_name_list,server_name,port_no):
    client=build_db_Client(server_name,port_no)
    db_ob_list=[]
    for item in db_name_list:
        db=None
        if isinstance(item,str):
            db=client[item]
            db_ob_list.append(db)
    if len(db_ob_list)>0:
        return db_name_list
    else:
        print("database build failed.....")

def build_one_collection(db_obj,collection_name):
    return db_obj[collection_name]

def search_one_data(db_obj,collection_name,find_json):
    res=db_obj[collection_name].find_one(find_json)
    if res:
        return res
    else:
        print("no results....")

def search_muilt_data(db_obj,collection_name,find_json):
    res=db_obj[collection_name].find(find_json)
    if res:
        return res
    else:
        print("no results....")

def update_one_data():
    print("not finished.....")

def insert_one_data(collection_obj,data):
    result = collection_obj.insert_one(data)
    if result:
        return True
    else:
        return False

def insert_many_data(collection_obj,data_json_list):
    if not check_data_type(data_json_list,"list"):
        return
    result=collection_obj.insert_many(data_json_list)
    if result:
        return True
    else:
        return False

def check_data_type(data,check_type):
    flag=None
    type_enm=[str,dict,int,float]
    if check_type not in type_enm:
        return
    if isinstance(data,check_type):
        flag=True
    else:
        flag=False
    return flag

def count_item(collection_obj,find_json):
    if not check_data_type(find_json,"dict"):
        return

    count=collection_obj.find(find_json).count()
    if count:
        return count
    else:
        print("cannot find data...")

def check_bool(bool_data):
    if isinstance(bool_data,bool):
        return True
    else:
        return False

def delete_one_data(collection_obj,condition_json):
    result=collection_obj.delete_one(condition_json)
    return check_bool(result)

def delete_many_data(collection_obj,condition_json):
    result=collection_obj.delete_many(condition_json)
    return check_bool(result)

def main():
    #write your test code
    db=build_one_database("test_db",None,None)
    collection_obj=build_one_collection(db,"test_collection")
    test_data={
        "test":"test"
    }
    res=insert_one_data(collection_obj,test_data)
    print("res:",res)
    pprint("not finished.....")

if __name__=="__main__":
    main()