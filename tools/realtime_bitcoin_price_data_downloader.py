#this tool is used for downloading the bitcoin price data from different trader server
# the website change very frequency

import sys
import os
import numpy as np
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import env_settings as env
import data_process_lib as lib
from urllib2 import request
import re
from lxml import etree

#import error
#from CodernityDB.database import Database 
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
profile = FirefoxProfile()
profile.set_preference('browser.cache.disk.enable', False)
profile.set_preference('browser.cache.memory.enable', False)
profile.set_preference('browser.cache.offline.enable', False)
profile.set_preference('network.cookie.cookieBehavior', 2)

options = Options()
#options.add_argument('--headless')

from pymongo import MongoClient

#db = TinyDB(storage=MemoryStorage)

DATAFRAME_TYPE="pd.core.frame.DataFrame"
CENTER_PLATFORM_ENUM=["Zaif","QUNINex","bitFlyer","BTCBOX","coincheck","bitbank"]
MONGODB_DEAFULT_PORT_NO="27020"

def create_database(database_server_name,port_no,database_name,collection_name):
    if database_name=="":
        database_name="coin_price_database"
    if collection_name=="":
        collection_name="bitcoin_collection"
    if database_server_name=="":
        database_server_name=="localhost"
    if port_no=="":
        port_no=MONGODB_DEAFULT_PORT_NO
    client=MongoClient(database_server_name+":"+port_no)
    #client=MongoClient()
    db=client[database_name]
    co=db[collection_name]
    return co

def insert_multi_data_into_database(json_data_list,collection_name): #mongdb
    if not isinstance(json_data_list,list):
        print("json data format error.....")
        return
    result=collection_name.insert_many(json_data_list)
    if result:
        print("multi data insert successfull.....")
    else:
        print("data insert error......")
    return result

def insert_single_data_into_database(json_data,collection_name): #mongodb
    if not isinstance(json_data_list,dict):
        print("json data format error.....")
        return
    result=collection_name.insert_one(json_data)
    if result:
        print("multi data insert successfull.....")
    else:
        print("data insert error......")
    return result

def insert_data_into_database(k_v_list): # use the tinyDB database to save the bitcoin price
    if not isinstance(k_v_list,list):
        return
    if not os.path.exists("database"):
        os.mkdir("database")
    today=datetime.today()
    db_name="coin_price_data"+str(today.year)+str(today.month)+str(today.day)+".json"
    db = TinyDB('./database/'+db_name,storage=CachingMiddleware(JSONStorage))
    for item in k_v_list:
        if isinstance(item,dict):
            db.insert(item)
            
def save_data_in_file(pd_data,file_name):# save the data in csv file or excel file
    if not isinstance(pd_data,DATAFRAME_TYPE):
        print("save data format error....must be dataframe format")
        exit()

    name,ext=os.path.splitext(file_name)
    if ext==".xls" or ext==".xlsx":
        pd_data.save_excel(file_name)
    elif ext==".csv":
        pd_data.save_csv(file_name)

def time_delay(time_int): 
    if isinstance(time_int,int):
        time.sleep(time_int)

def abstract_data(soup_data): #abstract the data from html data 
    today_date=datetime.today()
    soup = BeautifulSoup(soup_data)
    all_data_ele=soup.findAll('div',{"class":"recent_table_middle"}) # table middle includes the price data
    """
    if len(all_data_ele)==1:
        head_ele=all_data_ele.find('thead')
    elsif:
        head_ele=all_data_ele[0].find('thead')

    th_ele=head_ele.findAll("th")
    # get the columns name
    if th_ele:
        center_name_col=item[0].text # 交易平台
        sell_price_col=item[1].text
        buy_price_col=item[2].text
        thread_col=item[3].text
        trade_col=item[4].text
    tbody_ele=all_data_ele.findAll('tbody')
    if tbody_ele:
        td_ele_list=tbody_ele.findAll("td")
        if td_ele_list:
            for item in td_ele_list:
    """
    company_list=["btc_jpy_zaif","btc_jpy_quoine","btc_jpy_bitflyer","btc_jpy_btcbox","btc_jpy_coincheck","btc_jpy_bitbank"]
    
    #td_class_name_list=["data_tick_company","data_tick_bid","data_tick_ask","data_tick_spread","data_tick_volume"] # tag name:td
    td_class_name_list=["data_tick_company","tbl-price price-up","tbl-price price-down","data_tick_spread","data_tick_volume"] # tag name:td
    
    volume_tag="span"
    price_dict_list=[]
    for class_name in company_list:
        data_ele=soup.find("tr",{"class":class_name})
        if data_ele:
            td_list=data_ele.findAll("td")
            for item_ele in td_list:
                print("item_ele:",item_ele)
                attr_dict=item_ele.attrs
                print("attr_dict:",attr_dict)

                if len(attr_dict)>=1 and "class" in attr_dict.keys():
                    if td_class_name_list[0] in attr_dict["class"]:
                        name=item_ele.text
                    if td_class_name_list[1] in attr_dict["class"]:
                        buy_price=item_ele.text
                    if td_class_name_list[2] in attr_dict["class"]:
                        sell_price=item_ele.text
                    if td_class_name_list[3] in attr_dict["class"]:
                        thread_no=item_ele.text
                else:
                    volume_ele=item_ele.find("span",{"class":"data_tick_volume"})
                    volume_no=volume_ele.text+"BTC"

            price_dict={
                "date":str(today_date),
                "name":"bticoin",
                "buy_price":buy_price,
                "sell_price":sell_price,
                "thread":thread_no,
                "trade_volume":volume_no.replace("¥n",""),
                "trade_platform":name
            }
            #append the dict list
            price_dict_list.append(price_dict)
    #print("data_detials:",price_dict_list)
    return price_dict_list

def save_pd_data_to_csv(pd_data,filename):
    #all_pd=pd.DataFrame()
    today=datetime.today()
    filename_new="bitcoin_price_"+str(today.year)+str(today.month)+str(today.day)+".csv"
    if filename_new!=filename:
        filename=filename_new

    full_path="../historical_data/price_data/"+filename
    if not os.path.exists(os.path.basename(full_path)):
        os.makedirs(os.path.basename(full_path))

    if os.path.exists(full_path):
        old_pd=pd.read_csv(full_path)
        if not old_pd.empty:
            pd_data=pd_data.append(old_pd)
    pd_data.to_csv(full_path,index=False)

def price_downloader(url):
    today=datetime.today()
    filename="bitcoin_price_"+str(today.year)+str(today.month)+str(today.day)+".csv"
    driver = webdriver.Firefox(options=options)
    #driver=webdriver.Firefox()
    time_interval=0.3 # second
    data_list=[]
    x=0
    MAX_COUNT=1000
    driver.get(url)
    all_pd=pd.DataFrame()
    all_list=[]
    #while(x<=MAX_COUNT):
    try:
        while(True):
            try:
                #driver.refresh()
                start_time=time.time()
                page_source=driver.page_source
            except:
                print("{} open error....".format(url))
                exit()
            
            data_dict_list=abstract_data(page_source)
            #insert_data_into_database(data_dict_list)
            #all_pd=all_pd.append(data_dict_list)
            all_list.extend(data_dict_list)
            end_time=time.time()
            delta_time=end_time-start_time
            print("deltatime:",delta_time)
            if len(all_list)>=MAX_COUNT:
                print("length of all_list:",len(all_list))
                save_pd_data_to_csv(pd.DataFrame().append(all_list,ignore_index=True),filename)
                all_list=[]
            if delta_time<time_interval:
               time_delay(time_interval-delta_time)
                #time_delay(1)
            x=x+1
            print("count:",x)
            """
            if len(data_list)==MAX_COUNT:
                insert_data_into_database(data_list)
                data_list=[]
            """
    except KeyboardInterrupt:
        time.sleep(1)
        all_pd=all_pd.append(all_list,ignore_index=True)
        print(len(all_pd))
        if not all_pd.empty:
            print("saveing the data,please wait........")
            save_pd_data_to_csv(all_pd,filename)
            print("data saved........")
    driver.close()
    print("webdriver closed......")

#not finished
def price_downloader_database(url): # save the data into mongo database
    db_co=create_database("","","coin_price_database","bitcoin_collection")
    today=datetime.today()
    filename="bitcoin_price_"+str(today.year)+str(today.month)+str(today.day)+".csv"
    driver = webdriver.Firefox(options=options)
    #driver=webdriver.Firefox()
    time_interval=0.3 # second
    data_list=[]
    x=0
    MAX_COUNT=1000
    driver.get(url)
    all_pd=pd.DataFrame()
    all_list=[]
    #while(x<=MAX_COUNT):
    try:
        while(True):
            try:
                #driver.refresh()
                start_time=time.time()
                page_source=driver.page_source
            except:
                print("{} open error....".format(url))
                exit()
            
            data_dict_list=abstract_data(page_source)
            #insert_data_into_database(data_dict_list)
            #all_pd=all_pd.append(data_dict_list)
            all_list.extend(data_dict_list)
            end_time=time.time()
            delta_time=end_time-start_time
            print("deltatime:",delta_time)
            if len(all_list)>=MAX_COUNT:
                print("length of all_list:",len(all_list))
                result=insert_multi_data_into_database(all_list,db_co)
                #save_pd_data_to_csv(pd.DataFrame().append(all_list,ignore_index=True),filename)
                if result:
                    print("data insert into database succefully......")
                    all_list=[]
            if delta_time<time_interval:
               time_delay(time_interval-delta_time)
                #time_delay(1)
            x=x+1
            print("count:",x)
            """
            if len(data_list)==MAX_COUNT:
                insert_data_into_database(data_list)
                data_list=[]
            """
    except KeyboardInterrupt:
        time.sleep(1)
        all_pd=all_pd.append(all_list,ignore_index=True)
        print(len(all_pd))
        if not all_pd.empty:
            print("saveing the data,please wait........")
            save_pd_data_to_csv(all_pd,filename)
            print("data saved........")
    driver.close()
    print("webdriver closed......")

def fast_price_downloader(url): #not used because of the slow insert into tinydatabase 
    
    driver = webdriver.Firefox(options=options)
    #########without reopen the database
    if not os.path.exists("database"):
            os.mkdir("database")
    today=datetime.today()
    db_name="coin_price_data"+str(today.year)+str(today.month)+str(today.day)+".json"
    #db = TinyDB('./database/'+db_name)
    db = TinyDB('./database/'+db_name,storage=CachingMiddleware(JSONStorage))
    ########################

    time_interval=1 # second
    data_list=[]
    x=0
    MAX_COUNT=10
    driver.get(url)
    #while(x<=MAX_COUNT):
    while(True):
        #print("fast mode.......")
        db_name_next="coin_price_data"+str(today.year)+str(today.month)+str(today.day)+".json"
        if db_name!=db_name_next:
            db = TinyDB('./database/'+db_name,storage=CachingMiddleware(JSONStorage))
            db_name=db_name_next
            print("reopen the database .....")
        try:
            #driver.refresh()
            start_time=time.time()
            page_source=driver.page_source
        except:
            print("{} open error....".format(url))
            exit()
        
        data_dict_list=abstract_data(page_source)
        insert_data_into_database(data_dict_list)
        #print("data_list length:",len(data_list))
        end_time=time.time()
        delta_time=end_time-start_time
        #if delta_time<time_interval:
        #    time_delay(delta_time)
        x=x+1
        print("count:",x)
        """
        if len(data_list)==MAX_COUNT:
            insert_data_into_database(data_list)
            data_list=[]
        """
    #
def get_bitcoin_fx_price(url):
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    bitflyer_name_xpath='//*[@id="pair_tick_rate_label"]/div/div[2]/table/tbody/tr[1]/td[1]'
    bitcoin_fx_sell_price_xpath='//*[@id="pair_tick_rate_label"]/div/div[2]/table/tbody/tr[1]/td[2]'
    bitcoin_fx_buy_price_xpath='//*[@id="pair_tick_rate_label"]/div/div[2]/table/tbody/tr[1]/td[3]'
    thread_number_xpath='//*[@id="pair_tick_rate_label"]/div/div[2]/table/tbody/tr[1]/td[4]'
    trade_volume_24hr_xpath='//*[@id="pair_tick_rate_label"]/div/div[2]/table/tbody/tr[1]/td[5]/span'
    all_price_pd=pd.DataFrame()
    while(True):
        bit_fx_dict={
            "name":None,
            "buy_price":None,
            "sell_price":None,
            "avg_price":None,
            "trade_vol":None,
            "thread_nu":None,
            "time":None
        }
        try:
            name_ele=driver.find_element_by_xpath(bitflyer_name_xpath)
            name=name_ele.text

            sell_price_ele=driver.find_element_by_xpath(bitcoin_fx_sell_price_xpath)
            sell_price=sell_price_ele.text

            buy_price_ele=driver.find_element_by_xpath(bitcoin_fx_buy_price_xpath)
            buy_price=buy_price_ele.text

            thread_number_ele=driver.find_element_by_xpath(thread_number_xpath)
            thr_nu=thread_number_ele.text

            trade_volume_ele=driver.find_element_by_xpath(trade_volume_24hr_xpath)
            trade_vol=trade_volume_ele.text

            time_now=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            bit_fx_dict["name"]=name
            bit_fx_dict["buy_price"]=lib.parse_int(buy_price)
            bit_fx_dict["sell_price"]=lib.parse_int(sell_price)
            bit_fx_dict["trade_vol"]=lib.parse_int(trade_vol)
            bit_fx_dict["thread_nu"]=lib.parse_int(thr_nu)
            bit_fx_dict["time"]=time_now
            bit_fx_dict["avg_price"]=(lib.parse_int(buy_price)+lib.parse_int(sell_price))/2
            one_price_pd=pd.DataFrame(bit_fx_dict)
            print("bit_fx_price:",bit_fx_dict)
            all_price_pd=
        except KeyboardInterrupt:
            time.sleep(1)
            all_pd=all_pd.append(all_list,ignore_index=True)
            print(len(all_pd))
            if not all_pd.empty:
                print("saveing the data,please wait........")
                save_pd_data_to_csv(all_pd,filename)
                print("data saved........")

    driver.close()
    print("webdriver closed......")

#download the html data from website
def get_html_str(url):
    res_obj=request.urlopen(url)
    html_byte=res_obj.read()
    if isinstance(html_byte,bytes):
        return html_byte.decode("utf-8")
    elif isinstance(html_byte,str):
        return html_byte
def bitcoin_realtime_price_data_abstraction(html_str):
    if isinstance(html_str,str):
        soup=BeautifulSoup(html_str)
    else:
        return

def main():
    mode=sys.argv[1]
    url="https://cc.minkabu.jp/pair/BTC_JPY"
    if mode=="fast":
        fast_price_downloader(url)
    elif mode=="normal":
        price_downloader(url)
    elif mode=="database":
        price_downloader_database(url)
    elif mode=="btc_fx":
        get_bitcoin_fx_price(url)


if __name__=="__main__":
    main()

# run command:python realtime_bitcoin_price_data_downloader.py btc_fx