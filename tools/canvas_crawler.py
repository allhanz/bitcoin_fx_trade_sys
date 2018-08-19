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
def get_target_canvas_obj(driver,path_str,select_type):
    select_enum=["css","xpath"]
    if select_type not in select_enum:
        return
    if select_type=="css":
        ele=driver.find_element_by_css_selector(path_str)
    elif select_type=="xpath": 
        ele=driver.find_element_by_xpath(path_str)
    

def main():
    target_text=""
    url="https://www.tradingview.com/chart/K3RNn4xr/"
    phantomJS_driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    
    firefox_driver=webdriver.Firefox(executable_path=env.firefox_webdriver_path)
    driver=firefox_driver
    driver.get(url) #phantomjs

    while(True):
        start_time=time.time()
        try:
            
        except:
            print("waiting for a minute and try again....")
            pass
        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)

if __name__=="__main__":
    main()



