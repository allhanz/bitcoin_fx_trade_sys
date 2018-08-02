# coding:utf-8
import pandas as pd
import numpy as np
import os
import sys
#reload(sys)
#sub_name={"tokyo1":"東証一部","tokyo2":"東証二部","tokyomaza":"東証マザ"}
#sys.setdefaultencoding('utf8')
x=sys.getdefaultencoding()
print(x)
#error_stock_id=[1333,1384,1414,1417,1419,1420,1430,1435,1514,1605,1606,1662,1663,1712,1719,1720,1721,1722,1726,1766,1773] # error stock id
error_stock_id=[6767,8301,8728]
"""
def stock_id_divide(sub_name):
    csv_file="./japan-all-stock-ID-oriData.csv"
    stock_id_folder="japan_stock_id"
    market_str="市場"
    stock_id_str="SC"
    stock_name_str="名称"
    if not os.path.exists(stock_id_folder):
        os.mkdir(stock_id_folder)
    stock_dataframe=pd.DataFrame()
    stock_dataframe.columns=["SC","名称"]
    stock_dataframe["SC"]=[]
    stock_dataframe[stock_name_str]=[]

    if os.path.exists(csv_file):
        data=pd.read_csv(csv_file)
        header=data.columns.values
    if stock_id_str,stock_id_str,stock_name_str in header:
        for data in data[stock_id_str]:
            index_no=data[stock_id_str].indexof(data)
            if sub_name==data[market_str]:
                stock_dataframe[]
"""
STOCK_TYPE={"NIKKEI225":"nikkei225","TOHO1":"toho1","TOHO2":"toho2","TOHOMUM":"tohomum"}
nikkei225_csv_file="./stock_id/japan/nikkei225-stock-prices.csv"
toho1_csv_file="./stock_id/japan/tosho-1st-stock-prices.csv"
toho2_csv_file="./stock_id/japan/tosho-2nd-stock-prices.csv"
toho_mother_csv_file="./stock_id/japan/tosho-mothers-stock-prices.csv"

def read_stock_info_dataframe(stock_type):
    stock_dataframe=pd.DataFrame()

    if not os.path.exists(nikkei225_csv_file):
        print("nikkei225_csv_file not exist!")
        exit()
    if not os.path.exists(toho1_csv_file):
        print("toho1_csv_file not exist!")
        exit()

    if not os.path.exists(toho2_csv_file):
        print("toho2_csv_file not exist!")
        exit()

    if not os.path.exists(toho_mother_csv_file):
        print("toho_mother_csv_file not exit!")

    if type(stock_type) is list:
        for item in stock_type:
            if item == STOCK_TYPE["NIKKEI225"]:
                csv_file=nikkei225_csv_file
            if item == STOCK_TYPE["TOHO1"]:
                csv_file=toho1_csv_file
            if item == STOCK_TYPE["TOHO2"]:
                csv_file=toho2_csv_file
            if item == STOCK_TYPE["TOHOMUM"]:
                csv_file = toho_mother_csv_file
            if os.path.exists(csv_file):
                csv_data=pd.read_csv(csv_file,encoding="utf-16")
    elif type(stock_type) is str:
        if stock_type in STOCK_TYPE.values():
            if stock_type == STOCK_TYPE["NIKKEI225"]:
                csv_file=nikkei225_csv_file
            if stock_type == STOCK_TYPE["TOHO1"]:
                csv_file=toho1_csv_file
            if stock_type == STOCK_TYPE["TOHO2"]:
                csv_file=toho2_csv_file
            if stock_type == STOCK_TYPE["TOHOMUM"]:
                csv_file = toho_mother_csv_file
            if os.path.exists(csv_file):
                csv_data=pd.read_csv(csv_file,encoding="utf-16",sep='\t')
            #print(csv_data["SC"])
            #print(csv_data["名称"])
            stock_dataframe=csv_data["SC"]

            #stock_dataframe[stock_type].append(csv_data["SC"])
    else:
        print("stock type error!exit!!")
        exit()
    #return stock_dataframe
    return csv_data
def get_stock_id_array(info_dataframe):
    id_info=info_dataframe["SC"]
    id_array=np.asarray(id_info)
    id_processed=remove_error_stock_id(id_array)
    return id_processed

def remove_error_stock_id(stock_id_list):
    stock_id_list=list(stock_id_list)
    for error_id in error_stock_id:
        if error_id in stock_id_list:
            stock_id_list.remove(error_id)
    return stock_id_list

def main():
    type1="nikkei225"
    type2="toho1"
    type3="toho2"
    type4="tohomum"
    stock_type=[]
    stock_type.append(type1)
    stock_type.append(type2)
    stock_type.append(type3)
    stock_type.append(type4)
    #stock_dataframe=read_stock_id(stock_type)
    stock_dataframe=read_stock_id(type1)
    print(len(stock_dataframe["SC"])) # nkkei 225
    stock_dataframe=read_stock_id(type2)
    print(len(stock_dataframe["SC"])) # toho 1
    stock_dataframe=read_stock_id(type3)
    print(len(stock_dataframe["SC"])) # toho 2
    stock_dataframe=read_stock_id(type4)
    print(len(stock_dataframe["SC"])) # toho mothers

"""
    stock_id_divide(sub_name["tokyo1"])
    stock_id_divide(sub_name["tokyo2"])
    stock_id_divide(sub_name["tokyomaza"])
"""
if __name__=="__main__":
    main()
