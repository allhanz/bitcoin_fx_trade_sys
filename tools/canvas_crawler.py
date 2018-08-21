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
import base64
from PIL import Image
from io import BytesIO
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

    canvas_png = canvas_base64_png(ele)
    # save to a file
    png_file_name="bt"
    png_writer()

def canvas_base64_png(canvas_obj):
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas_obj)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    return canvas_png

def png_writer(png_file_name,png_data):
    with open(rpng_file_name, 'wb') as f:
        f.write(png_data)

def get_and_save_element_screen_shoot(driver,element_obj,img_file_name):
    location = element_obj.location
    size = element_obj.size
    png = driver.get_screenshot_as_png() # saves screenshot of entire page
    im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(img_file_name) # saves new cropped image
    print("candele png file {} is saved....".format(img_file_name))

def load_url(url):
    driver=webdriver.Firefox(executable_path=env.firefox_webdriver_path)
    driver.get(url)
    driver.maximize_window()
    return driver

def main():
    print("not tested....")
    delta_time=60*5 #5 minutes interval
    url="https://www.tradingview.com/chart/K3RNn4xr/" # please set 5 minutes interval in your own page in tradeview website
    phantomJS_driver=webdriver.PhantomJS(executable_path=env.phantomJS_path)
    driver=load_url(url)
    #driver=phantomJS_driver
    #target_xpath="/html/body/div[1]/div[1]/div/div[1]/div[2]/table/tbody"
    target_xpath="/html/body/div[1]/div[1]/div/div[1]/div/table/tbody"
    
    while(True):
        start_time=time.time()
        driver.refresh()
        now_date=datetime.now()
        time.sleep(5)
        png_file_name=env.bitcoin_candle_pic_root_path+"/fx_bitcoin_price_"+now_date.strftime("%Y-%m-%dT%H:%M:%S")+".png"
        try:
            element_obj=driver.find_element_by_xpath(target_xpath)
            #waiting for loading finihsed
            time.sleep(5)
            get_and_save_element_screen_shoot(driver,element_obj,png_file_name)
        except:
            print("waiting for a minute and try again....")
            driver.close()
            time.sleep(10)
            driver=load_url(url)
            pass
        end_time=time.time()
        spend_time=end_time-start_time  
        if delta_time-spend_time>=0:
            time.sleep(delta_time-spend_time)

if __name__=="__main__":
    main()



