import os
import sys
import pandas as pd
import numpy as np
import quandl
from datetime import timedelta, date
import re

# global vars
quandl.ApiConfig.api_version = '2015-04-09'
quandl.ApiConfig.api_key = 'q6sne2ob3eZrg7G4KkBi' # get the api from my account
currency_list_file="currency_list.xlsx"

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

def download_fx_one_day_data(database_name,currency_name,date_str):# date format: ex:2018-xx-xx
    if not check_fx_database(database_name):
        database_name="CLS/HP"
    date_re=re.compile(r"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")
    flag =date_re.match(date_str)
    if flag==None:
        print("data_str format error,please check it again.....")
        return
    fx_data=quandl.get_table(database_name, fx_business_date=date_str, currency=currency_name)
    if not fx_data.empty:
        return fx_data
    else:
        print("fx_data empty,please check it again....")

def download_daterange_his_period_data(database_name,currency_name,start_date,end_date):
    if database_name==None or database_name=="":
        database_name="CLS/HP"

    fx_all_pd=pd.DataFrame()
    date_list=daterange(start_date,end_date)
    daily_fx_pd=pd.DataFrame()
    for single_day in date_list:
        daily_fx_pd=download_fx_one_day_data(database_name,currency_name,single_day)
        fx_all_pd=fx_all_pd.append(daily_fx_pd,ignore_index=True)

    if not fx_all_pd.empty:
        return fx_all_pd
        
def save_pd_data(pd_data,filename):
    if os.path.exists(filename):
        old_pd=pd.read_excel(filename)
        pd_data=pd_data.append(old_pd)

    if not pd_data.empty:
        pd_data.save(filename,encoding="utf-8")

def save_fx_data(fx_pd_data,filename):
    if not fx_pd_data.empty:
        save_pd_data(fx_pd_data,filename)

def main():
    currency_exp=["AUDJPY	AUDNZD	AUDUSD	CADJPY	EURAUD	EURCAD	EURCHF	EURDKK	EURGBP	EURHUF	EURJPY EURNOK	EURSEK	EURUSD	GBPAUD	GBPCAD	GBPCHF	GBPJPY	GBPUSD	NZDUSD	USDCAD	USDCHF	USDDKK	USDHKD	USDHUF	USDILS	USDJPY	USDKRW	USDMXN	USDNOK	USDSEK	USDSGD	USDZAR"]
    start_date = date(2013, 1, 1)
    end_date = date(2015, 6, 2)
    date_list=daterange(start_date, end_date)
    #print("date_list:",date_list)
    fx_data=download_fx_one_day_data("","AUDJPY","2016-07-20")
    print("fx_data:",fx_data)

if __name__=="__main__":
    main()
