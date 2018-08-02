import subprocess
from jsm_stock_lib import *
import pandas as pd
from datetime import datetime
import jsm
import os
import time
import calendar
from japan_stock_id_divided import *
import numpy as np
import multiprocessing

q = jsm.Quotes()
c = jsm.QuotesCsv()
FILE_TYPE=".csv"
now=datetime.now()
ROOT_PATH="./stock_data/"
MONTHLY_DIR_PATH="./stock_data/monthly_data/"
date_str=now.strftime("%Y%m%d")

def get_stock_price(stock_id_list):
    price_list=[]
    for id in stock_id_list:
        price_list.append(q.get_price(id))
    print(price_list)
    return price_list

def check_reputecated_file(stock_id_list):
    day_time=datetime.today().date()
    time_str=day_time.strftime("%Y%m%d")
    id_and_file_list=[[],[]]
    whole_data_folder_path="./stock_data/whole_data"
    if not os.path.exists(whole_data_folder_path):
        os.mkdir(whole_data_folder_path)

    file_list=os.listdir(whole_data_folder_path)
    print(file_list)
    id_list=[]
    for item in file_list:
        id=item[:4]
        id_list.append(int(id))

    for data in stock_id_list:
        if data in id_list:
            print("reputicated id:",data)
            stock_id_list.remove(data)
    print("exist id list:",id_list)
    
    for id in stock_id_list:
        csv_file_name=str(id)+"-"+time_str+".csv"
        file_path=whole_data_folder_path+"/"+csv_file_name
        id_and_file_list[0].append(id)
        id_and_file_list[1].append(file_path)

    #print("check_reputecated_file id:",stock_id_list)
    return id_and_file_list

def whole_stock_data_parallel_processing(stock_type):
    type1="nikkei225"
    type2="toho1"
    type3="toho2"
    type4="tohomum"
    # example
    stock_dataframe=read_stock_info_dataframe(stock_type)
    stock_id=get_stock_id_array(stock_dataframe)
    id_len=len(stock_id) # nkkei 225
    print("stock_id length:",id_len)
    num=id_len//10
    jobs=[]
    print("stock length:",num)
    for i in range(0,num):
        start_index=i*10
        end_index=(i+1)*10-1
        print("start_index:",start_index)
        print("end_index:",end_index)
        print("new thread added!!")
        id_argv=stock_id[start_index:end_index]
        id_checked_info=check_reputecated_file(id_argv)

        job=multiprocessing.Process(target=save_whole_data,args=(id_checked_info[0],id_checked_info[1], ))
        jobs.append(job)
        job.start()

    [job.join() for job in jobs] # run the parallel processing

def main():
    stock_type="toho1"
    whole_stock_data_parallel_processing(stock_type)

if __name__=="__main__":
    main()
