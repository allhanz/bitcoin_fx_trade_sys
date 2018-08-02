import pandas as pd
import numpy as np
import os
import sys
import time

HEADER_STR=["date","open","high","low","close","volume", "_adj_close"]
ROOT_PATH="/Users/zhonghan/workspace/japan_stock_analysis/python_stock/data/stock_data/"

def get_home_dir():
    home_path=os.getenv("HOME")
    return home_path

def get_current_dir():
    current_path=os.getcwd()
    return current_path

def get_data_dir():
    current_path=get_current_dir()
    whole_data_path=current_path+"/stock_data/whole_data"
    return whole_data_path

def get_one_stock_whole_data(stock_id):
    #remove_same_file()
    data_dir=get_data_dir()
    all=False
    data=read_from_csv(data_dir,stock_id,all)
    print("stock datframe:",data)
    return data

def remove_same_file(): # test NG 
    data_dir=get_data_dir()
    full_path_list=list_up_files(data_dir)
    file_list=[] # file name list not include the path info
    for i in full_path_list:
        filename=os.path.basename(i)
        file_list.append(filename)

    file_info=[[],[]]
    check_list=[[],[]]
    for item in file_list:
        file_info[0].append(int(item[:4])) # stock id
        file_info[1].append(int(item[5:13])) # date info 20171011
    print(file_info)

    for data in file_info[0]:
        index_data=file_info[0].index(data)
        check_list[0]=file_info[0][index_data+1:]
        check_list[1]=file_info[1][index_data+1:]
        print("check_list:",check_list)
        if data in check_list[0]:
            same_index=check_list[0].index(data)
            one_date=int(file_info[1][index_data])
            two_date=int(check_list[1][same_index])
            print("reputicated stock id:",data)
            print("one_date",one_date)
            print("two_date",two_date)
            if one_date >=two_date:
                print("remove the file1:",file_list[same_index])
                os.remove(full_path_list[same_index])
                time.sleep(0.01)
            else:
                print("remove the file2:",file_list[index_data])
                os.remove(full_path_list[index_data])
                time.sleep(0.01)


    print("reputicated file check finished!!")


def read_from_csv(dir_path,stock_id,all): #specif the year
    #datatime format 20161109
    csv_data=[]
    file_name_without_day=[]

    if os.path.exists(dir_path):
        full_file_list=list_up_files(dir_path)
        for item in full_file_list:
            file_name_without_day.append(os.path.basename(item)[:4])

        if all == True:
            for file in full_file_list:
                base_dataframe={}
                base_dataframe["stock_id"]=file_str
                data=pd.read_csv(file,header=None)
                data_with_header=set_data_header(data)
                base_dataframe["stock_info"]=data_with_header
                csv_data.append(base_dataframe)
        else:
            for file_str in file_name_without_day:
                if file_str in stock_id:
                    base_dataframe={}
                    base_dataframe["stock_id"]=file_str
                    index_value=file_name_without_day.index(file_str)
                    data=pd.read_csv(full_file_list[index_value],header=None)
                    data_with_header=set_data_header(data)
                    base_dataframe["stock_info"]=data_with_header
                    csv_data.append(base_dataframe)
                    #csv_data.append(data_with_header)
        print("csv data:",data)
        #whole_data=set_data_header(csv_data)
        return csv_data
    else:
        print("file path does not exist!!")
        exit()


#def pandas_data_process(header,data):

def set_data_header(data):
    if type(data) is pd.core.frame.DataFrame:
        data.columns=HEADER_STR
        return data
    else:
        print("data type from csv file error!!")
        exit()

def list_up_files(file_path):
    file_list=[]
    for root, dirs, files in os.walk(file_path):
        #print(root)
        #print(dirs)
        for file in files:
            if file.endswith(".csv"):
                #print(file)
                full_path=os.path.join(root, file)
                file_list.append(full_path)
    return file_list

def main():
    dir_path=sys.argv[1]
    datetime=sys.argv[2]
    stock_id=sys.argv[3]
    read_from_csv(dir_path,datetime,stock_id)

if __name__=="__main__":
    main()
