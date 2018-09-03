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
import shutil

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
    "date":None,
    "time":None,
    "spread_no":None,
    "trade_vol":None
}


def get_screen_shot_and_save(img_ele,driver):
    location = img_ele.location
    size = img_ele.size
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png')

def hash_sha512(str_data):
    hash_object = hashlib.sha512(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    print("hex_dig:",hex_dig)
    return hex_dig

def hash_sha256(str_data):
    hash_object = hashlib.sha256(str_data.encode("utf-8"))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def driver_rebuild(url):
    driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    driver.get(url)
    return driver

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
    now_time=datetime.now()
    data_format["name"]=name
    data_format["buy_price"]=buy_price
    data_format["sell_price"]=sell_price
    data_format["time"]=now_time.strftime("%H%M%S")
    data_format["date"]=now_time.strftime("%Y%m%d")
    data_format["spread_no"]=spread_no
    data_format["trade_vol"]=trade_vol
    #data_format["_id"]=random.randint(0,MAX_RANGE)
    data_format["_id"]=hash_sha512(str(data_format))

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

def check_same_val(data_list,thredhold_val,check_key):
    sam_flag=False
    sam_count=0
    if not data_list:
        return sam_flag

    if check_key not in data_list[0].keys():
        print("please check the key name {} again in data...".format(check_key))
        return
    else:
        check_val=data_list[0][check_key]
    for item in data_list[1:]:
        if check_val==item[check_key]:
            sam_count=sam_count+1
        
    if sam_count>=thredhold_val:
        sam_flag=True
    return sam_flag

def main():
    url="https://cc.minkabu.jp/pair/BTC_JPY"
    driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    wait=WebDriverWait(driver,3)
    #firefox_driver=webdriver.Firefox(executable_path=env.firefox_webdriver_path)
    driver.get(url) #phantomjs
    delta_time=1 #unit second
    collection=build_bitcoin_database("bitcoin_db","price_collection")
    collection.create_index([("index", pymongo.DESCENDING)])
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    check_data_list=[]
    check_len=20
    thredhold_val=10
    r=redis_datatabase_api.build_realtime_db()
    redis_id_prefix="bitflyer_bitcoin_price_"
    scan_ptn="bitflyer_bitcoin_price_[0-9]*"
    today_now=int(datetime.now().strftime("%Y%m%d"))
    #for redis database insert test -> OK
    #redis_datatabase_api.fx_insert_multi_kv(r,redis_id_prefix,scan_ptn,{"a":3})
    #flag=redis_datatabase_api.pickle_insert(r,redis_id_prefix,scan_ptn,{"a":2})
    index=0
    redis_datatabase_api.delete_data_by_ptn(r,scan_ptn)
    #for test
    """
    new_redis_file=env.redis_daily_data_path+"/dump_"+str(today_now)+".rdb"
    old_redis_file=env.redis_daily_data_path+"/dump.rdb"
    redis_datatabase_api.mv_redis_db_file(r,env.redis_daily_data_path)
    os.rename(old_redis_file,new_redis_file)
    exit()
    """
    while(True):
        start_time=time.time()
        today_next=int(datetime.now().strftime("%Y%m%d"))
        if today_next>today_now:
            new_redis_file=env.redis_daily_data_path+"/dump_"+str(today_now)+".rdb"
            old_redis_file=env.redis_daily_data_path+"/dump.rdb"
            redis_datatabase_api.mv_redis_db_file(r,env.redis_daily_data_path)
            os.rename(old_redis_file,new_redis_file)
            today_now=today_next
            redis_datatabase_api.delete_data_by_ptn(r,scan_ptn)
        if len(check_data_list)==check_len:
            check_data_list=[]

        try:
            
            data=get_realtime_price(driver)
            print("data:",data)
            redis_id=redis_id_prefix+str(index)
            flag=redis_datatabase_api.pickle_insert_by_id(r,redis_id,data)
            if not flag:
                print("redis data insert failed......")
            check_data_list.append(data)
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
        """
        sam_flag=check_same_val(check_data_list,thredhold_val,"buy_price")
        if sam_flag:
            print("the page of url in browser not updated. reopen it....")
            driver.close()
            driver=driver_rebuild(url)
            #break
        """
        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)
            index=index+1

if __name__=="__main__":
    main()
