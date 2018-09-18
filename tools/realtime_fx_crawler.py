import os
import sys
import pandas as pd
import mongodb_api
import redis_datatabase_api
import time
from datetime import datetime
import hashlib

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
#from webdriver_manager import EdgeDriverManager
#from webdriver_manager import IEDriverManager



xe_url="https://www.xe.com"
oanda_live_fx_rates_url="https://www.oanda.com/currency/live-exchange-rates/"

def hash_sha512(str_data):
    hash_object = hashlib.sha512(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig

def hash_sha256(str_data):
    hash_object = hashlib.sha256(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def build_webdriver(browser_type):
    browser_enum=["chrome","firefox","edge","ie"]
    if browser_type==None or browser_type not in browser_enum:
        browser_type="firefox"
    if browser_type=="chrome":
        driver=webdriver.Chrome(ChromeDriverManager().install())
    if browser_type=="firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    """
    if browser_type=="edge":
        driver = webdriver.Edge(EdgeDriverManager().install())
    if browser_type=="ie":
        driver = webdriver.Ie(IEDriverManager().install())
    """
    return driver
    
def get_realtime_fx_price_in_oanda(driver,xpath_dict):
    if xpath_dict==None:
        xpath_dict={}
        xpath_dict["bid"]=['//*[@id="USD_JPY-b-int"]','//*[@id="USD_JPY-b-pip"]','//*[@id="USD_JPY-b-ette"]']
        xpath_dict["ask"]=['//*[@id="USD_JPY-a-int"]','//*[@id="USD_JPY-a-pip"]','//*[@id="USD_JPY-a-ette"]']

    current_datetime=datetime.now().strftime("%Y%m%d %H:%M:%S")
    fx_data={
        "datetime":current_datetime,
        "bid_price":None,
        "ask_price":None,
        "fx_platform":"oanda_fx",
        "fx_symbol":None
    }
    bid_price=''
    ask_price=''
    fx_data["fx_symbol"]=xpath_dict["name"]

    for xpath_item in xpath_dict["bid"]:
        try:
            ele=driver.find_element_by_xpath(xpath_item)
            text_data=ele.text
            if text_data:
                bid_price=bid_price+text_data
                #bid_price.append(text_data)

        except:
            print("element not found, pass....")
            pass
    
    for xpath_item in xpath_dict["ask"]:
        try:
            ele=driver.find_element_by_xpath(xpath_item)
            text_data=ele.text
            if text_data:
                ask_price=ask_price+text_data
                #ask_price.append(text_data)

        except:
            print("element not found, pass....")
            pass
    if len(bid_price)>0 and len(ask_price)>0:
        fx_data["ask_price"]=ask_price
        fx_data["bid_price"]=bid_price
        fx_data["_id"]=hash_sha512(str(fx_data))
        return fx_data
    else:
        print("fx price data download error.....")

    '''    
    usd_jpy_bid_price_1_xpath='//*[@id="USD_JPY-b-int"]'
    usd_jpy_bid_price_2_xpath='//*[@id="USD_JPY-b-pip"]'
    usd_jpy_bid_price_3_xpath='//*[@id="USD_JPY-b-ette"]'

    usd_jpy_ask_price_1_path='//*[@id="USD_JPY-a-int"]'
    usd_jpy_ask_price_1_path='//*[@id="USD_JPY-a-pip"]'
    usd_jpy_ask_price_1_path='//*[@id="USD_JPY-a-ette"]'
    '''


def get_realtime_fx_price_in_ex(driver):
    from_currency_xpath='//*[@id="ratesTable"]/div/section[1]/table/tbody/tr[2]/th/span/span/a'
    from_currency_ele=driver.find_element_by_xpath(from_currency_xpath)
    from_currency=from_currency_ele.text

    #to_usd_xpath='//*[@id="ratesTable"]/div/section[1]/table/tbody/tr[1]/th[2]/div/span/a'
    #to_usd_ele=driver.find_element_by_xpath(to_usd_xpath)

    to_usd_price_xpath='//*[@id="ratesTable"]/div/section[1]/table/tbody/tr[2]/td[1]/a'
    to_usd_price_ele=driver.find_element_by_xpath(to_usd_price_xpath)
    to_usd_price=to_usd_price_ele.text

    to_eur_price_xpath='//*[@id="ratesTable"]/div/section[1]/table/tbody/tr[2]/td[2]/a'
    to_eur_price_ele=driver.find_element_by_xpath(to_eur_price_xpath)
    to_eur_price=to_eur_price_ele.text

def build_fx_mongodb(db_name,collection_name):
    database=mongodb_api.build_one_database(db_name,None,None)
    collection=mongodb_api.build_one_collection(database,collection_name)
    #document=mongodb_api.build_one_document(collection,collection_name)
    return collection

def main():

    usdjpy_xpath_dict={
        "ask":[
            '//*[@id="USD_JPY-a-int"]',
            '//*[@id="USD_JPY-a-pip"]',
            '//*[@id="USD_JPY-a-ette"]'
        ],
        "bid":[
            '//*[@id="USD_JPY-b-int"]', #
            '//*[@id="USD_JPY-b-pip"]',
            '//*[@id="USD_JPY-b-ette"]'

        ],
        "name":"USD/JPY"
    }
    eurjpy_xpath_dict={
        "ask":[
            '//*[@id="EUR_JPY-a-int"]', #
            '//*[@id="EUR_JPY-a-pip"]',
            '//*[@id="EUR_JPY-a-ette"]'
        ],
        "bid":[
            '//*[@id="EUR_JPY-b-int"]',
            '//*[@id="EUR_JPY-b-pip"]',
            '//*[@id="EUR_JPY-b-ette"]'
        ],
        "name":"EUR/JPY"
    }
    gbdjpy_xpath_dict={
       "ask":[
            '//*[@id="GBP_JPY-a-int"]', #
            '//*[@id="GBP_JPY-a-pip"]',
            '//*[@id="GBP_JPY-a-ette"]'
        ],
        "bid":[
            '//*[@id="GBP_JPY-b-int"]',
            '//*[@id="GBP_JPY-b-pip"]',
            '//*[@id="GBP_JPY-b-ette"]'
        ],
        "name":"GBD/JPY"
    }
    audjpy_xpath_dict={
        "ask":[
            '//*[@id="AUD_JPY-a-int"]',
            '//*[@id="AUD_JPY-a-pip"]',
            '//*[@id="AUD_JPY-a-ette"]'
        ],
        "bid":[
            '//*[@id="AUD_JPY-b-int"]',
            '//*[@id="AUD_JPY-b-pip"]',
            '//*[@id="AUD_JPY-b-ette"]'
        ],
        "name":"AUD/JPY"
    }
    fx_xpath_dict_list=[
        usdjpy_xpath_dict,
        eurjpy_xpath_dict,
        gbdjpy_xpath_dict,
        audjpy_xpath_dict
    ]

    fx_collection=build_fx_mongodb("fx_db","price_collection")
    r=redis_datatabase_api.build_realtime_db()
    count=0
    delta_time=10
    driver=build_webdriver("firefox")
    time.sleep(1)
    driver.get(oanda_live_fx_rates_url)
    today_now=int(datetime.now().strftime("%Y%m%d"))

    while(True):
        start_time=time.time()
        today_next=int(datetime.now().strftime("%Y%m%d"))
        print("today_next:",today_next)
        print("today_now:",today_now)

        for xpath_dict in fx_xpath_dict_list:
            redis_index=xpath_dict["name"]+"_"+str(count)
            redis_ptn=xpath_dict["name"]+"_[0-9]*"
            if today_next>today_now:
                today_now=today_next
                redis_datatabase_api.delete_data_by_ptn(r,redis_ptn)
                count=0
            try:
                fx_data=get_realtime_fx_price_in_oanda(driver,xpath_dict)
                print("fx_data:",fx_data)
                flag=redis_datatabase_api.pickle_insert_by_id(r,redis_index,fx_data)
                if not flag:
                    print("redis data insert failed......")
                res=fx_collection.insert_one(fx_data)
                if not res:
                    print("insert data into mongodb error....")
            except:
                driver.close()
                time.sleep(0.5)
                driver=build_webdriver("firefox")
                driver.get(oanda_live_fx_rates_url)
                print("canot get the data, try again.....")
                pass
        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)
            count=count+1

if __name__=="__main__":
    main()
