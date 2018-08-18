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

phantomJS_path="/usr/local/bin/phantomjs" # please set the path
driver=webdriver.PhantomJS(executable_path=phantomJS_path)
wait=WebDriverWait(driver,3)
data_format={
    "name":None,
    "buy_price":None,
    "sell_price":None,
    "time":None,
    "spread_no":None,
    "trade_vol":None
}

#def get_realtime_price(url):
def get_realtime_price(driver):
    start_time=time.time()
    """
    if url==None or url=="":
        url="https://cc.minkabu.jp/pair/BTC_JPY"
    driver.get(url)
    """

    bitflyer_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(1)"
    bitflyer_ele=driver.find_element_by_css_selector(bitflyer_css_sel)
    name=bitflyer_ele.text
    
    sell_price_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(2)"
    sell_price_ele=driver.find_element_by_css_selector(sell_price_css_sel)
    sell_price=sell_price_ele.text
    
    buy_price_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(3)"
    buy_price_ele=driver.find_element_by_css_selector(buy_price_css_sel)
    buy_price=buy_price_ele.text

    spread_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(4)"
    spread_ele=driver.find_element_by_css_selector(spread_css_sel)
    spread_no=spread_ele.text

    trade_vol_css_sel=".fx_btc_jpy_bitFlyer > td:nth-child(5)"
    trade_vol_ele=driver.find_element_by_css_selector(trade_vol_css_sel)
    trade_vol=trade_vol_ele.text

    #data_format value
    data_format["name"]=name
    data_format["buy_price"]=buy_price
    data_format["sell_price"]=sell_price
    data_format["time"]=datetime.now().strftime("%Y%m%dT%H%M%S")
    data_format["spread_no"]=spread_no
    data_format["trade_vol"]=trade_vol

    return data_format

def build_bitcoin_database(db_name,collection_name):
    database=mongodb_api.build_one_database(db_name,None,None)
    collection=mongodb_api.build_one_collection(database,collection_name)
    #document=mongodb_api.build_one_document(collection,collection_name)

    return collection

def main():
    url="https://cc.minkabu.jp/pair/BTC_JPY"
    driver.get(url)
    delta_time=1 #unit second
    collection=build_bitcoin_database("bitcoin_db","price_collection")

    while(True):
        start_time=time.time()
        data=get_realtime_price(driver)
        print("data:",data)
        end_time=time.time()
        spend_time=end_time-start_time
        res=collection.insert_one(data)
        if not res:
            print("insert data error....")
            
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)

if __name__=="__main__":
    main()
