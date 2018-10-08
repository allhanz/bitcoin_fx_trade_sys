####### pyfolio_test.py ##########
import os
import sys
from pandas_datareader import data as web
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pyfolio as pf
from datetime import datetime

#must install gtk lib in advanced

def get_data_from_remoteDB(symbol_name,remotedb_name,start_date,end_date):
        pd_data=pd.DataFrame()
        if remotedb_name!=None:
                try:
                        pd_data=web.DataReader(symbol_name,remotedb_name,start=start_date,end=end_date)
                except:
                        pd_data=web.get_data_yahoo(symbol_name,start=start_date,end=end_date)
        else:
                pd_data=web.get_data_yahoo(symbol_name,start=start_date,end=end_date)
        if not pd_data.empty:
                return pd_data
        else:
                print("get data error....")

def get_rets_data(symbol_name,remotedb_name,start_date,end_date):
        close_tag_enum=["closed","Closed","close","Close","Adj Close","adj close","Adj close","adj Close"]

        ohlc_pd=get_data_from_remoteDB(symbol_name,remotedb_name,start_date,end_date)
        for item in close_tag_enum:
                if item in ohlc_pd.columns:
                        close_tag=item
                        break

        if not ohlc_pd.empty:
                ohlc_pd["date"]=pd.to_datetime(ohlc_pd.index)
                ohlc_pd.set_index('date', drop=False, inplace=True)
                rets = ohlc_pd[[close_tag]].pct_change().dropna()
                rets.index = rets.index.tz_localize("UTC")
                rets.columns = [symbol_name]
        return rets[symbol_name]
        
def get_bayesian_tear_sheet(rets,live_start_index):
        #rets must be a series data type
        out_of_sample=rets.index[live_start_index]
        pf.create_bayesian_tear_sheet(rets,live_start_date=out_of_sample)
        #problem:cannot output the result figure

def main():
        start_date=datetime(2018,1,1)
        end_date=datetime(2018,9,20)
        symbol_name="FB"
        remotedb_name="iex"
        rets=get_rets_data(symbol_name,remotedb_name,start_date,end_date)
        get_bayesian_tear_sheet(rets,-40)

if __name__=="__main__":
        main()
