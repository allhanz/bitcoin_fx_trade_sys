import os
import sys
import pandas as pd
import alpha_vantage
import requests
import pprint
import matplotlib.pyplot as plt
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import talib
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import candlesticks_pattern_recognition
import requests
import json
import mongodb_api
import redis_datatabase_api
import hashlib
import time
# need premium api_key

API_URL = "https://www.alphavantage.co/query"

api_key="X5Z4X60MA7GE04YY"

def hash_sha512(str_data):
    hash_object = hashlib.sha512(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig

def hash_sha256(str_data):
    hash_object = hashlib.sha256(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def sample_test():
    #test ok
    
    symbols = ['QCOM',"INTC","PDD"]

    for symbol in symbols:
            data = { "function": "TIME_SERIES_INTRADAY", 
            "symbol": symbol,
            "interval" : "60min",       
            "datatype": "json", 
            "apikey": api_key } 
            response = requests.get(API_URL, data) 
            data = response.json()
            print(symbol)
            a = (data['Time Series (60min)'])
            keys = (a.keys())
            for key in keys:
                    print(a[key]['2. high'] + " " + a[key]['5. volume'])

def stock_common_api(function_name,symbol_name,interval_time,data_type):
    stock_func_list=["TIME_SERIES_INTRADAY","TIME_SERIES_DAILY","TIME_SERIES_DAILY_ADJUSTED","TIME_SERIES_WEEKLY","TIME_SERIES_WEEKLY_ADJUSTED"]
    if function_name not in stock_func_list:
        return 
    print("print(symbol):",symbol_name)
    api_info = { "function": function_name, 
            "symbol": symbol_name,
            "interval" : interval_time,       
            "datatype": data_type, 
            "apikey": api_key }
    response = requests.get(API_URL, api_info) 
    data = response.json()
    return data

def get_realtime_fx_data(from_currency_name,to_currency_name):
    api_info={
        "function":"CURRENCY_EXCHANGE_RATE",
        "from_currency":from_currency_name,
        "to_currency":to_currency_name,
        "apikey":api_key
    }
    
    response = requests.get(API_URL, api_info) 
    res_json = response.json()
    print("res_json:\n",res_json)
    if "Realtime Currency Exchange Rate" in res_json.keys():
        data=res_json["Realtime Currency Exchange Rate"]
        price=data["5. Exchange Rate"]
        date_time=data["6. Last Refreshed"]
        time_zone_name=data["7. Time Zone"]
        cleaned_data={
            "data_platform":"alpha_vantage",
            "symbol":from_currency_name+"/"+to_currency_name,
            "date_time":date_time,
            "time_zone":time_zone_name,
            "price":price
        }
        cleaned_data["_id"]=hash_sha512(str(cleaned_data))
        return cleaned_data

    else:
        print("get data error....")

    '''
    #response data sample
    {
    "Realtime Currency Exchange Rate": {
        "1. From_Currency Code": "USD",
        "2. From_Currency Name": "United States Dollar",
        "3. To_Currency Code": "JPY",
        "4. To_Currency Name": "Japanese Yen",
        "5. Exchange Rate": "112.04900000",
        "6. Last Refreshed": "2018-09-16 07:46:38",
        "7. Time Zone": "UTC"
        }
    }
    '''


def fx_common_api(function_name,from_symbol_name,to_symbol_name,interval_time,datatype_name,size_type):
    fx_function_list=["CURRENCY_EXCHANGE_RATE","FX_INTRADAY","FX_DAILY","FX_WEEKLY","FX_MONTHLY"]
    if function_name not in fx_function_list:
        return 
    api_info={
        "function":function_name,
        "from_symbol":from_symbol_name,
        "to_symbol":to_symbol_name,
        "interval":interval_time,
        "outputsize":size_type,
        "datatype":datatype_name,
        "apikey":api_key
    }
    response = requests.get(API_URL, api_info) 
    res_json = response.json()
    index_name="Time Series FX ("+ interval_time+")"
    data_list=[]
    data_dict={
        "date_time":None,
        "open":None,
        "high":None,
        "low":None,
        "close":None
    }
    if index_name in res_json.keys():
        data=res_json[index_name]
        for item in data.keys():
            data_dict["date_time"]=item
            data_dict["open"]=data[item]["1. open"]
            data_dict["high"]=data[item]["2. high"]
            data_dict["low"]=data[item]["3. low"]
            data_dict["close"]=data[item]["4. close"]
            data_list.append(data_dict)
    if len(data_list)>0:
        return data_list
    else:
        print("response data error....")
    '''
    #response data sample
    {
    "Meta Data": {
        "1. Information": "FX Intraday (5min) Time Series",
        "2. From Symbol": "EUR",
        "3. To Symbol": "USD",
        "4. Last Refreshed": "2018-09-14 21:00:00",
        "5. Interval": "5min",
        "6. Output Size": "Full size",
        "7. Time Zone": "UTC"
    },
    "Time Series FX (5min)": {
        "2018-09-14 21:00:00": {
            "1. open": "1.1622",
            "2. high": "1.1625",
            "3. low": "1.1622",
            "4. close": "1.1625"
        },
        "2018-09-14 20:55:00": {
            "1. open": "1.1621",
            "2. high": "1.1623",
            "3. low": "1.1619",
            "4. close": "1.1623"
        },
        "2018-09-14 20:50:00": {
            "1. open": "1.1623",
            "2. high": "1.1623",
            "3. low": "1.1619",
            "4. close": "1.1622"
        },
        "2018-09-14 20:45:00": {
            "1. open": "1.1624",
            "2. high": "1.1625",
            "3. low": "1.1621",
            "4. close": "1.1623"
        },
        "2018-09-14 20:40:00": {
            "1. open": "1.1623",
            "2. high": "1.1625",
            "3. low": "1.1622",
            "4. close": "1.1623"
        },
    }
    '''

def build_fx_mongodb(db_name,collection_name):
    database=mongodb_api.build_one_database(db_name,None,None)
    collection=mongodb_api.build_one_collection(database,collection_name)
    #document=mongodb_api.build_one_document(collection,collection_name)
    return collection

ts = TimeSeries(key=api_key,retries=5,output_format='pandas',indexing_type='integer')

def main():
    fx_symbols=[("USD","JPY"),("CNY","JPY")]
    fx_collection=build_fx_mongodb("fx_db","price_collection")
    r=redis_datatabase_api.build_realtime_db()
    count=0
    delta_time=60
    while(True):
        start_time=time.time()
        for item in fx_symbols:
            from_symbol_name,to_symbol_name=item
            redis_index=from_symbol_name+"_to_"+to_symbol_name+"_"+str(count)
            try:
                data=get_realtime_fx_data(from_symbol_name,to_symbol_name)
            except:
                print("get realtime fx data failed.try again....")
                data=get_realtime_fx_data(from_symbol_name,to_symbol_name)
            time.sleep(20)
            print("data:",data)
            mongodb_flag=fx_collection.insert_one(data)
            if not mongodb_flag:
                print("mongodb insert data failed.....")

            redis_flag=redis_datatabase_api.pickle_insert_by_id(r,redis_index,data)
            if not redis_flag:
                print("redis data insert failed....")
        end_time=time.time()
        spend_time=end_time-start_time
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)
            count=count+1
    #get_stock_test()

if __name__=="__main__":
    main()
    #sample_test()