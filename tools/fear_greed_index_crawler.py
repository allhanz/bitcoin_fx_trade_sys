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
from PIL import Image
from io import BytesIO
import env_settings as env
import redis_datatabase_api
import webdriver_manager


data_format={
    "_id":None,
    "name":"bitcoin_fear_index",
    "index_val":None,
    "date":None,
    "time":None
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

def build_bitcoin_database(db_name,collection_name):
    database=mongodb_api.build_one_database(db_name,None,None)
    collection=mongodb_api.build_one_collection(database,collection_name)
    #document=mongodb_api.build_one_document(collection,collection_name)
    return collection

def get_fear_index_val(driver):
    fear_index_xpath="/html/body/main/section[2]/div/div[1]/div[2]/div[1]/div[1]/div"
    fear_index_ele=driver.find_element_by_xpath(fear_index_xpath)
    fear_val=int(fear_index_ele.text)
    print("fear_val:",fear_val)
    
    #data_format value
    now_time=datetime.now()
    data_format["index_val"]=fear_val
    data_format["time"]=now_time.strftime("%H%M%S")
    data_format["date"]=now_time.strftime("%Y%m%d")
    data_format["_id"]=hash_sha512(str(data_format))

    return data_format

def driver_rebuild(url):
    driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    driver.get(url)
    return driver

def main():
    url="https://alternative.me/crypto/fear-and-greed-index/"
    driver=webdriver.Firefox(executable_path=env.firefox_webdriver_path)
    #driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    collection=build_bitcoin_database("bitcoin_db","fear_index_collection")
    driver.get(url)
    delta_time=60*60 #unit second

    while(True):
        start_time=time.time()
        try:
            driver.refresh()
            time.sleep(20)
            data=get_fear_index_val(driver)
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
            driver=driver_rebuild(url)
            pass

        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)

    

if __name__=="__main__":
    main()
