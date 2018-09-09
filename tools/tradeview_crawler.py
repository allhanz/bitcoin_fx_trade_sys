import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from pyquery import PyQuery as pq
import re
import time
from datetime import datetime
from pprint import pprint
import mongodb_api
import concurrent.futures
import pymongo
import random
import hashlib
import env_settings as env

#OverflowError: MongoDB can only handle up to 8-byte ints
"""
Size of long long types is 8 bytes
Signed long long min: -9223372036854775808 max: 9223372036854775807
Unsigned long long min: 0 max: 18446744073709551615
"""
MAX_RANGE=10**10

data_format={
    "_id":None,
    "name":None,
    "buy_price":None,
    "sell_price":None,
    "mean_price":None,
    "date":None,
    "time":None,
    "trade_vol":None,
    "coin_name":None
}
def hash_sha512(str_data):
    hash_object = hashlib.sha512(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig
    
def hash_sha256(str_data):
    hash_object = hashlib.sha256(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig

#def get_realtime_price(url):
def get_realtime_price(driver):
    start_time=time.time()
    """
    if url==None or url=="":
        url="https://cc.minkabu.jp/pair/BTC_JPY"
    driver.get(url)
    """
    """
    name_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(1)"
    name_ele=driver.find_element_by_css_selector(name_css_sel)
    name=name_ele.text
    """
    name="FXBTCJPY"

    sell_price_css_sel=".tv-trading-toolbar__bs-button--sell > div:nth-child(2)"
    sell_price_ele=driver.find_element_by_css_selector(sell_price_css_sel)
    sell_price=sell_price_ele.text
    
    #time.sleep(0.2)

    buy_price_css_sel=".tv-trading-toolbar__bs-button--buy > div:nth-child(2)"
    buy_price_ele=driver.find_element_by_css_selector(buy_price_css_sel)
    buy_price=buy_price_ele.text

    #time.sleep(0.2)

    mean_price_css_sel=".dl-header-price"
    mean_price_ele=driver.find_element_by_css_selector(mean_price_css_sel)
    mean_price=mean_price_ele.text

    #time.sleep(0.2)

    #data_format value
    now_time=datetime.now()
    data_format["coin_name"]=name
    data_format["buy_price"]=buy_price
    data_format["sell_price"]=sell_price
    data_format["mean_price"]=mean_price
    data_format["time"]=now_time.strftime("%H%M%S")
    data_format["date"]=now_time.strftime("%Y%m%d")
    data_format["_id"]=hash_sha512(str(data_format))
    data_format["name"]="tradeview"
    return data_format

def build_bitcoin_database(db_name,collection_name):
    database=mongodb_api.build_one_database(db_name,None,None)
    collection=mongodb_api.build_one_collection(database,collection_name)
    #document=mongodb_api.build_one_document(collection,collection_name)
    return collection

def check_data_downloaed():
    collection=build_bitcoin_database("bitcoin_db","price_collection")
    inserted_data=collection.find()
    for data in inserted_data:
        pprint(data)
    print("inserted_data:\n",inserted_data)
    return inserted_data

def driver_build(url):
    driver=webdriver.Firefox(executable_path=env.firefox_webdriver_path)
    driver.get(url)
    return driver

def main():
    target_text=""
    url="https://www.tradingview.com/chart/K3RNn4xr/"
    phantomJS_driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    
    driver=driver_build(url)
    
    collection=build_bitcoin_database("bitcoin_db","price_collection")
    #collection.create_index([("index", pymongo.DESCENDING)])
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    wait=WebDriverWait(driver,3)

    delta_time=3 #unit second

    while(True):
        start_time=time.time()
        try:
            data=get_realtime_price(driver)
            print("data:",data)
                #exit()
            res=collection.insert_one(data)
                #res=executor.submit(collection.insert_one,data)
            if not res:
                #if not res.result:
                print("insert data error....")
        except:
            print("waiting for a minute and try again....")
            driver.close()
            driver=driver_build(url)
        #    pass
        
        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)

if __name__=="__main__":
    main()
