import os
import sys
sys.path.append("../../../tools/")
import env_settings as env
import mongodb_api
import pandas as pd
import data_process_lib
import file_util
from pprint import pprint

def get_fx_csv_file(path_name):
    file_list=file_util.get_specified_ext_file(path_name,".csv")
    if len(file_list)>0:
        return file_list
    else:
        print("no file list,please check it again....")

def read_fx_data(file_name):
    print("file_name:",file_name)
    pd_data=pd.read_csv(file_name,encoding="utf-8",header=None)
    cols=["currency_name","time","price_low","price_high"]
    pd_data.columns=cols
    print("pd_data sample 30:\n",pd_data.iloc[:30])
    return pd_data

def build_fx_database():
    db=mongodb_api.build_one_database("fx_database",None,None)
    fx_collection=mongodb_api.build_one_collection(db,"fx_price_collection")
    return fx_collection

def save_to_database(collection_obj,json_list):
    if not isinstance(json_list,list):
        print("list data type error. please check it again....")
        return

    #insert_data_list=[]
    print("data saving into database. please wait for a monment....")
    for item in json_list:
        if "_id" not in item.keys():
            item["_id"]=data_process_lib.hash_sha512(str(item))
            #insert_data_list.append(item)
            try:
                collection_obj.insert_one(item)
            except:
                """
                print("data saving into database error occured. update data instead of insert data.......")
                print("_id:",item["_id"])
                collection_obj.update_one(
                    {"_id":item["_id"]},
                    {"$set":item},
                    upsert=False
                    )
                """
                #print("find the duplicated id, pass.....")
                pass


def main():
    #get the kill problem, but nit solved....

    fx_data_path=env.fx_data_root_path
    print("path:",fx_data_path)
    csv_file_list=get_fx_csv_file(fx_data_path)
    
    fx_collection=build_fx_database()
    print("csv_file_list:",csv_file_list)
    for file_i in csv_file_list:
        pd_data=read_fx_data(file_i)
        json_list=data_process_lib.convert_pd_to_jsonList(pd_data)
        #print("json_list:",json_list[0:1])
        #save_to_database(fx_collection,json_list[0:1])
        save_to_database(fx_collection,json_list)
        #delete the data to save the space
        del pd_data,json_list
        #exit()
    

if __name__=="__main__":
    main()