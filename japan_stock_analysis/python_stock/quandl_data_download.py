import quandl
import os
import urllib
import urllib.request
#from StringIO import StringIO
from bs4 import BeautifulSoup
from io import StringIO
import codecs
#import json
import simplejson as json
import re
from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import datetime,timedelta,date
from forex_python.converter import CurrencyRates

stock_mkt_index_folder="./stock_market_index"

def get_price(stock_id):
    print("not implemented!!")

def get_gold_daily_price():
    downloaded_file="./gold_daily_price/gold_daily_price.html"
    source_url='https://www.quandl.com/api/v3/datasets/WGC/GOLD_DAILY_USD'
    if not os.path.exists('gold_daily_price'):
        os.makedirs('gold_daily_price')
    #urllib.request.urlretrieve(source_url, downloaded_file)
    node_name="code"
    json_file=gen_gold_csv_file(node_name,downloaded_file)

def gen_gold_csv_file(node_name,html_file_path):
    html_data=f=codecs.open(html_file_path, 'r', 'utf-8')
    soup = BeautifulSoup(html_data,'html.parser')
    for tag in soup.find_all(re.compile(node_name)): #get the body contents
        data_str=tag.get_text()
        #print(data_str)
        #print(type(tag.get_text()))
        f=open("./gold_daily_price/data.json","w")
        f.write(data_str)
        f.close()
        with open("./gold_daily_price/data.json") as data_file:
            json_str=json.load(data_file)
            #print(json_str)
            price_data=json_str["dataset"]["data"]
            if type(price_data) is list:
                price_array=np.asarray(price_data)
            price_dataFrame=pd.DataFrame(price_array)
            price_dataFrame.columns=["date","price"]
            price_dataFrame.to_csv("./gold_daily_price/gold_price.csv")

def gold_price(date_start,date_end):
    if os.path.exists("./gold_daily_price/gold_price.csv"):
        data=pd.read_csv("./gold_daily_price/gold_price.csv")
    else:
        print("gold price data error.exit!!")
        exit()
    return data

def get_oil_daily_price():
    url = "https://www.quandl.com/api/v3/datasets/CHRIS/CME_CL1.csv"
    data=pd.read_csv(url, index_col=0, parse_dates=True)
    if not os.path.exists("oil_daily_price"):
        os.mkdir("oil_daily_price")
    data.to_csv("./oil_daily_price/oil_price.csv")
    """
    wticl1 = pd.read_csv(url, index_col=0, parse_dates=True)
    wticl1.sort_index(inplace=True)
    wticl1_last = wticl1['Last']
    wticl1['PctCh'] = wticl1.Last.pct_change()
    fig = plt.figure(figsize=[7,5])
    ax1 = plt.subplot(111)
    line = wticl1_last.tail(68).plot(color='red',linewidth=3)
    ax1.set_ylabel('USD per barrel')
    ax1.set_xlabel('')
    ax1.set_title('WTI Crude Oil Price', fontsize=18)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ax1.tick_params(axis='x', which='major', labelsize=8)
    fig.text(0.15, 0.85,'Last: $' + str(wticl1.Last[-1])\
             + ' (as of: ' \
             + str(wticl1.index[-1].strftime('%Y-%m-%d'))\
             + ')');
    fig.text(0.15, 0.80,'Change: $' + str(wticl1.Change[-1])\
             + '; ' \
             + str((np.round((wticl1.PctCh[-1] * 100), \
             decimals=2))) + '%')
    fig.text(0.1, 0.06, 'Source: ' + url)
    fig.text(0.1, 0.02, 'briandew.wordpress.com')
    plt.savefig('oil.png', dpi=1000)
    """
def oil_price():
    if os.path.exists("./oil_daily_price/oil_price.csv"):
        data=pd.read_csv("./oil_daily_price/oil_price.csv")
    else:
        print("oil price data error.exit!!")
        exit()
    return data

def get_currency_daily_price(end_date,currency_type):
    if not type(currency_type) is list:
        print("currency_type data error!!exit!!")
        exit()

    USD_csv_file="./currency_daily_data/USD_price.csv"
    EUR_csv_file="./currency_daily_data/EUR_price.csv"
    GBP_csv_file="./currency_daily_data/GBP_price.csv"
    CNY_csv_file="./currency_daily_data/CNY_price.csv"
    AUD_csv_file="./currency_daily_data/AUD_price.csv"

    start_date=datetime(2000,1,1)
    #start_date=datetime(2017,1,1) # for test
    end_date=datetime.today()
    date_range=daterange(start_date,end_date)
    #print(date_range)
    c=CurrencyRates()
    #currency_data=pd.DataFrame()
    print(currency_type)
    #if type(currency_type) is list:
        #currency_data.columns=currency_type
    for data_type in currency_type:
        array_data={"date":[],"rate":[]}
        if data_type =="USD":
            csv_file=USD_csv_file
        elif data_type == "EUR":
            csv_file=EUR_csv_file
        elif data_type== "GBP":
            csv_file=GBP_csv_file
        elif data_type== "CNY":
            csv_file=CNY_csv_file
        elif data_type=="AUD":
            csv_file=AUD_csv_file
        else:
            print("currency_type not specified!!please check again!!")
            exit()


        for date in date_range:
            #print(date)
            data=c.get_rate(currency_type,"JPY",date)
            #print(data)
            #if not currency_type in currency_data.columns.values():
            #currency_data.columns.append(currency_type)
            array_data["date"].append(date)
            array_data["rate"].append(data)
        #print(array_data.values())
        #currency_data=pd.DataFrame(list(array_data.items()),columns=["date","rate"])
        currency_data=pd.DataFrame({"date":array_data["date"],"rate":array_data["rate"]})
        print(currency_data)
        gen_currency_csv_file(currency_data,csv_file)

    print(currency_data)

def daterange(start_date,end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def gen_currency_csv_file(data,file_path): # the currency daily rate from other currency into JYP
    root_path="./currency_daily_data"
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    data.to_csv(file_path)

def currency_price(currency_type):
    print("not implemented!!")

def get_NASDAQ_daily_index(): #ok
    folder="nasdaq_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="ansdaq_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("NASDAQOMX/COMP", authtoken="q6sne2ob3eZrg7G4KkBi")
    index_data.to_csv(file_path)

def get_DJIA_daily_index():
    folder="nasdaq_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="ansdaq_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("NASDAQOMX/COMP", authtoken="q6sne2ob3eZrg7G4KkBi")
    index_data.to_csv(file_path)

def get_SP500_daily_index(): #ok
    folder="sp500_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="sp500_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("YAHOO/INDEX_GSPC", authtoken="q6sne2ob3eZrg7G4KkBi", start_date="1970-01-01")
    index_data.to_csv(file_path)

def get_DAX_daily_index(): #ok
    folder="dax_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="dax_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("YAHOO/INDEX_GDAXI", authtoken="q6sne2ob3eZrg7G4KkBi")
    index_data.to_csv(file_path)

def get_ASX_daily_index():
    folder="asx_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="ansdaq_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("NASDAQOMX/COMP", authtoken="q6sne2ob3eZrg7G4KkBi")
    index_data.to_csv(file_path)

def get_FTSE100_daily_index():# UK
    folder="nasdaq_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="ansdaq_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("NASDAQOMX/COMP", authtoken="q6sne2ob3eZrg7G4KkBi")
    index_data.to_csv(file_path)

def get_NIKKEI_daily_index(): #ok
    folder="nikkei_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="nikkei_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("NIKKEI/INDEX", authtoken="q6sne2ob3eZrg7G4KkBi", start_date="1970-01-01")
    index_data.to_csv(file_path)

def get_hangSeng_index(): # hong kong index #ok
    foler="hangSeng_index"
    folder_path=stock_market_index+"/"+folder
    csv_file="hangSeng_index.csv"
    file_path=folder_path+"/"+csv_file
    if os.path.exists(folder_path):
        os.mkdir(folder_path)

    index_data=quandl.get("YAHOO/INDEX_HSI", authtoken="q6sne2ob3eZrg7G4KkBi", start_date="1970-01-01")
    index_data.to_csv(file_path)


def get_main_stock_market_index():
    get_NASDAQ_daily_index()
    get_DJIA_daily_index()
    get_SP500_daily_index()
    get_DAX_daily_index()
    get_ASX_daily_index()
    get_FTSE100_daily_index()
    get_NIKKEI_daily_index()
    get_hangSeng_index()

def download_finance_data():
    quandl.ApiConfig.api_key = 'q6sne2ob3eZrg7G4KkBi'
    CURRENCY_TYPE=["USD","EUR","CNY","AUD","GBP"] # AUD
    #get_gold_daily_price() # save the gold daily price data into csv file
    #get_oil_daily_price() # save the oil daily price data into csv file
    end_date=datetime.today().date()
#   end_date=datetime.today()
    get_currency_daily_price(end_date,["USD"])
    get_currency_daily_price(end_date,["EUR"])
    get_currency_daily_price(end_date,["AUD"])
    get_currency_daily_price(end_date,["GBP"])

    get_oil_daily_price()
    get_gold_daily_price()

    get_main_stock_market_index()

def main():
    download_finance_data()

def test():
    print("not implemented!!")


if __name__ == "__main__":
    main()
