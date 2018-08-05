# this tool is used for trading in bitflyer trading server

import pybitflyer
import sys
import os
#sys.path.append(os.path.abspath("./bitflyerAPI"))
#import bitflyer_api as pybitflye
import pandas as pd
from datetime import datetime
import env_settings as env

#api manual
#https://lightning.bitflyer.com/docs?lang=zh-CN#http-api

def get_key_info(key_file):
    if key_file==None or key_file=="":
        key_file=env.bitflyer_api_file
    if not os.path.exists(key_file):
        print("{} file not exist. please check it again....")
    pd_data=pd.read_excel(key_file)
    info_dict={}
    api_key=pd_data["api_key"].values
    api_password=pd_data["api_password"].values
    info_dict["api_key"]=api_key[0]
    info_dict["api_password"]=api_password[0]
    if info_dict:
        #print("info_dict:",info_dict)
        print("get the bitflyer api with no error.....")
        return info_dict
    else:
        print("key info error,please check it.....")

def set_api_info():
    api_info_dict=get_key_info(None)
    if api_info_dict:
        api = pybitflyer.API(api_key=api_info_dict["api_key"], api_secret=api_info_dict["api_password"])
        return api
    else:
        print("api info set error....")

def get_board_info(api,product_code):
    if product_code==None or product_code=="":
        product_code="FX_BTC_JPY"
    board = api.board(product_code=product_code)

    if board:
        return board
    else:
        print("get {} board info error......".format(product_code))

def get_ticker_info(api,product_code):
    if product_code==None or product_code=="":
        product_code="FX_BTC_JPY"

    ticker = api.ticker(product_code=product_code)
    if ticker:
        return ticker
    else:
        print("get {} ticker info error....".format(product_code))

def get_today_time():
    today_date=datetime.now()
    date_str=today_date.strftime("%Y-%m-%d-%H-%m")
    return date_str

def get_balance(api):
    #respose data format
    #[{'currency_code': 'JPY', 'amount': 50000.0, 'available': 50000.0}, {'currency_code': 'BTC', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'BCH', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'ETH', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'ETC', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'LTC', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'MONA', 'amount': 0.0, 'available': 0.0}, {'currency_code': 'LSK', 'amount': 0.0, 'available': 0.0}]

    balance=api.getbalance()
    if balance:
        pd_balance=pd.DataFrame(balance)
        save_pd_data(pd_balance,"../balance_daily/balance_"+get_today_time()+".xlsx")
        return pd_balance
    else:
        print("get balance error...")

def save_pd_data(pd_data,filename):
    if not pd_data.empty:
        pd_data.to_excel(filename,encoding="utf-8")

def check_all_key_value(key_enum,dict_data):
    flag=True
    for key in dict_data.keys():
        if key not in key_enum:
            flag=False
            break
    return flag

def request_child_order(api,order_dict):
    #product_codeは注文するプロダクトを指定します。BTC_JPYやFX_BTC_JPY、またはETH_BTCを選択します。
    #child_order_typeは注文のタイプで、指値注文なら"LIMIT"、成行注文なら"MARKET"を指定します。
    #sideには売り買いを"SELL"か"BUY"で、sizeに取引額を指定します。

    """
    {
    "product_code": "BTC_JPY",
    "child_order_type": "LIMIT",
    "side": "BUY",
    "price": 30000,
    "size": 0.1,
    "minute_to_expire": 10000,
    "time_in_force": "GTC"
    }
    """
    key_enum=["product_code","child_order_type","side","size","minute_to_expire","time_in_force"]
    flag=check_all_key_value(key_enum,order_dict)
    if flag:
        order_res=api.sendchildorder(
            product_code=order_dict["product_code"],
            child_order_type=order_dict["child_order_type"],
            side=order_dict["side"],
            price=order_dict["price"],
            size=order_dict["size"],
            minute_to_expire=10000,
            time_in_force="GTC"
        )

    else:
        print("order param data error, please check it again.....")

def request_parent_order(api,order_dict_list):
    #body parameter

    """
    {
    "order_method": "IFDOCO",
    "minute_to_expire": 10000,
    "time_in_force": "GTC",
    "parameters": [{
        "product_code": "BTC_JPY",
        "condition_type": "LIMIT",
        "side": "BUY",
        "price": 30000,
        "size": 0.1
    },
    {
        "product_code": "BTC_JPY",
        "condition_type": "LIMIT",
        "side": "SELL",
        "price": 32000,
        "size": 0.1
    },
    {
        "product_code": "BTC_JPY",
        "condition_type": "STOP_LIMIT",
        "side": "SELL",
        "price": 28800,
        "trigger_price": 29000,
        "size": 0.1
    }]
    """
    print("not finished.....")

def get_child_order_list(api):
    
    order_list=api.getchildorders()
    if len(order_list)==0:
        print("get child order lisy error or there is no order list.....")
    else:
        return order_list

def get_parent_order_list(api):
    order_list=api.getparentorders()
    if len(order_list)==0:
        print("get parent order list error or there is no parent order list.....")
    else:
        return order_list

def confirm_order_status(order_obj):
    status_flag=True
    status_res=None
    if order_obj==None or order_obj=="" or order_obj==[]:
        status_flag=False
    elif isinstance(order_obj,list):
        print("order respose object list analysis not finished....")
    elif isinstance(order_obj,dict):
        key_list=order_obj.keys()
        if "status" in key_list:
            status_value=order_obj["status"]
            if status_value!=200:
                status_flag=False
                save_not_200_status_data(order_obj,None)

        if "child_order_acceptance_id" in key_list:
            status_res=order_obj
        if "child_order_id" in key_list:
            status_res=order_obj

    if status_flag:
        return order_obj

def save_not_200_status_data(status_data,filename): #save in txt file
    if filename==None or filename=="":
        filename="../order_status_error/error_list.xlsx"

    if not os.path.exists(os.path.basename(filename)):
        os.makedirs(os.path.basename(filename))
    with open(filename, "a+") as myfile:
        myfile.write(status_data)
    myfile.close()
    delete_reduplicated_context(filename)

def delete_reduplicated_context(filename):
    print("not finished....")

def get_coin_outs(api):
    return api.getcoinouts()

def get_chat_msg(api,date_data):
    if date_data==None or date_data=="":
        date_data=datetime.now().date()

    #date format
    """
    [
    {
        "nickname": "User1234567",
        "message": "Hello world!",
        "date": "2016-02-16T10:58:08.833"
    },
    {
        "nickname": "TestUser",
        "message": "TestHello",
        "date": "2016-02-15T10:18:06.67"
    }
    """
    chat_msg=api.getchats(from_date=date_data)
    msg_pd=pd.DataFrame(chat_msg)
    if not msg_pd.empty:
        save_pd_data(msg_pd,"../chat_msg_data/bitflyer/msg_data_"+date_data.strftime("%Y-%m-%d")+".xlsx")
        return msg_pd
    else:
        print("get chat msg data error....")

def get_execution_his(api,product_code):
    execu_list=api.executions(product_code=product_code)
    if execu_list:
        exe_pd=pd.DataFrame(execu_list)
        save_pd_data(exe_pd,"../execution_his_data/execu_his_data_"+get_today_time()+".xlsx")
        return exe_pd
    else:
        print("get executions historical data error.....")

def main():
    api=set_api_info()
    print("api:",api)


if __name__=="__main__":
    main()

