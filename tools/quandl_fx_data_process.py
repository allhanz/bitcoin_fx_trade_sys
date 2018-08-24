import os
import sys
import pandas as pd
import numpy as np
import quandl
from datetime import timedelta, date
import re
import env_settings as env

# global vars
def set_quandl_api(api_dict):
    quandl.ApiConfig.api_key = api_dict["api_key"]
    quandl.ApiConfig.api_version=api_dict["date"]
    return quandl

def get_quandl_api_key():
    api_dict={
        "date":None,
        "api_key":None
    }
    acc_file=env.quandl_api_file
    pd_data=pd.read_excel(acc_file)
    version_date=pd.to_datetime(pd_data["date"].values[0])
    api_dict["date"]=version_date.strftime("%Y-%m-%d")
    api_dict["api_key"]=str(pd_data["api_key"].values[0])
    #print("api_dict:",api_dict)
    return api_dict

def check_currency_name(currency_name):
    currency_list=get_currency_enum_list()
    if currency_name in currency_list:
        return True
    else:
        return False

def get_currency_enum_list():
    curr_pd=pd.read_excel(currency_list_file)
    cols=curr_pd.columns
    currency_list=curr_pd[cols[1]].values
    if currency_list:
        return currency_list

def check_date_str_format(date_str):
    date_re=re.compile(r"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
    flag =date_re.match(date_str)
    if flag:
        return True
    else:
        return False

def daterange(start_date, end_date):
    date_list=[]
    daterange=pd.date_range(start_date,end_date)
    for single_date in daterange:
        date_list.append(single_date.strftime("%Y-%m-%d"))
    if len(date_list)>0:
        return date_list

def check_fx_database(database_name):
    fx_database_enum=["CLS/HP","CLS/IDHP"]
    #CLS/HP database start time:2015-09-01
    #database details url:https://www.quandl.com/databases/CLSRP/documentation/coverage-and-data-organization
    if database_name in fx_database_enum:
        return True
    else:
        return False

def download_fx_one_day_data(quandl_api,database_name,currency_name,date_str):# date format: ex:2018-xx-xx
    if not check_fx_database(database_name):
        database_name="CLS/IDH"
    date_re=re.compile(r"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
    flag =date_re.match(date_str)
    if flag==None:
        print("data_str format error,please check it again.....")
        return
    print("database_name:{},date_str:{},currency_name:{}".format(database_name,date_str,currency_name))
    #date_str="2018-01-02"
    fx_data=quandl_api.get_table(database_name,fx_business_date=date_str, currency=currency_name)
    #for test
    #fx_data=quandl.get_table('CLS/IDH', fx_business_date='2018-01-02', currency='AUDJPY')
    if not fx_data.empty:
        return fx_data
    else:
        print("fx_data empty,please check it again....")

def download_daterange_his_period_data(quandl_api,database_name,currency_name,start_date,end_date):
    if database_name==None or database_name=="":
        database_name="CLS/IDH"

    fx_all_pd=pd.DataFrame()
    date_list=daterange(start_date,end_date)
    daily_fx_pd=pd.DataFrame()
    for single_day in date_list:
        daily_fx_pd=download_fx_one_day_data(quandl_api,database_name,currency_name,single_day)
        fx_all_pd=fx_all_pd.append(daily_fx_pd,ignore_index=True)
        print("fx_all_pd:",fx_all_pd)
        filename=currency_name+"_"+single_day+".xlsx"
        fullpath=env.fx_data_root_path+"/"+filename
        save_fx_data(fx_all_pd,fullpath)

    if not fx_all_pd.empty:
        return fx_all_pd
        
def save_pd_data(pd_data,filename):
    if os.path.exists(filename):
        old_pd=pd.read_excel(filename)
        pd_data=pd_data.append(old_pd)

    if not pd_data.empty:
        pd_data.to_excel(filename,encoding="utf-8")

def save_fx_data(fx_pd_data,filename):
    if not fx_pd_data.empty:
        save_pd_data(fx_pd_data,filename)

def main():
    #fx data download test
    currency_enum=["AUDJPY	AUDNZD	AUDUSD	CADJPY	EURAUD	EURCAD	EURCHF	EURDKK	EURGBP	EURHUF	EURJPY EURNOK	EURSEK	EURUSD	GBPAUD	GBPCAD	GBPCHF	GBPJPY	GBPUSD	NZDUSD	USDCAD	USDCHF	USDDKK	USDHKD	USDHUF	USDILS	USDJPY	USDKRW	USDMXN	USDNOK	USDSEK	USDSGD	USDZAR"]
    currency_name="AUDJPY"
    start_date = date(2018, 1, 1)
    end_date = date(2018, 1, 3)
    date_list=daterange(start_date, end_date)
    print("date_list:",date_list)
    api_dict=get_quandl_api_key()
    #print("api_dict:",api_dict)
    quandl_api=set_quandl_api(api_dict)
    # for test
    fx_data=download_fx_one_day_data(quandl_api,"",currency_name,"2018-01-02")
    #print("fx_data:",fx_data)
    pd_data=download_daterange_his_period_data(quandl_api,"",currency_name,start_date,end_date)
    print("pd_data:",pd_data)

if __name__=="__main__":
    main()
