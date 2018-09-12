import os
import sys
import talib
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
from trade_algotithms.technical_analysis import *

def sample_code():
    sample_data = [
    ['1/22/14', 10, 18,  5, 20],
    ['1/23/14', 12, 21,  7, 22],
    ['1/24/14', 14, 24, 9 , 24],
    ['1/25/14', 16, 27, 11, 26],
    ['1/26/14', 18, 30, 13, 28],
    ['1/27/14', 20, 33, 15, 30],
    ['1/28/14', 22, 36, 17, 32],
    ['1/29/14', 24, 39, 19, 34],
    ['1/30/14', 26, 41, 21, 38],
    ['1/31/14', 30, 45, 25, 40],
    ['2/01/14', 43, 44, 42, 43],
    ['2/02/14', 46, 47, 45, 46],
    ['2/03/14', 44, 45, 43, 44],
    ['2/04/14', 40, 55, 35, 50],
    ]

    # convert data to columns
    sample_data = np.column_stack(sample_data)

    # extract the columns we need, making sure to make them 64-bit floats
    open = sample_data[1].astype(float)
    high = sample_data[2].astype(float)
    low = sample_data[3].astype(float)
    close = sample_data[4].astype(float)

    res=talib.CDLTRISTAR(open, high, low, close)
    print("shape of sample data:",sample_data.shape)
    print("length of res:",len(res))
    print("res:",res)

def convert_to_candlestick_data(data_file,pd_data,time_period,timestamp_ptn,target_cols,sort_type,sort_col_name):
    
    #sort_type:datetime or timestamp

    if not time_period:
        time_period="5Min"

    if os.path.exists(data_file):
        buffer_pd=pd.read_csv(data_file,encoding="utf-8",parse_dates=True)
    elif not pd_data.empty:
        buffer_pd=pd_data.copy()
    if sort_type=="datetime":
        buffer_pd=sort_value_by_datetime(buffer_pd,sort_col_name,timestamp_ptn)
    elif sort_type=="timestamp":
        buffer_pd=sort_value_by_time(buffer_pd,sort_col_name,)
    else:
        print("the data not sorted....")

    ohlc_data=[]
    for item in target_cols:
        item_data=buffer_pd[item].resample(time_period).ohlc()
        print("head data:",item_data.head())
        ohlc_data.append(item_data)
    ohlc_pd=pd.concat([ohlc_data],axis=1,keys=target_cols)
    
    return ohlc_pd

def sort_value_by_datetime(pd_data,date_col_name,date_ptn):
    
    if not pd_data.empty:
        buffer_pd=pd_data.copy()
        buffer_pd[date_col_name]=pd.to_datetime(buffer_pd[date_col_name],format=date_ptn)
        buffer_pd.sort(date_col_name,inplace=True)
        return buffer_pd
    else:
        print("data error")

def sort_value_by_time(pd_data,time_col_name):
    if not pd_data.empty:
        sorted_pd=pd_data.sort_values(by=[time_col_name])
        return sorted_pd
    else:
        print("data error...")

def caculate_increse_rate(pd_data,col_name):
    if not pd_data.empty:
        pct_pd=pd_data.pct_change()
        return pct_pd
    
def matplot_candlesticks(ohlc_pd):
    if ohlc_pd.empty:
        return
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    #ax.xaxis.set_minor_formatter(dayFormatter)

    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick_ohlc(ax, ohlc_pd, width=0.6)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

def candlesticks_pattern_detector(ohlc_pd,detect_type_list):
    
    pass

def main():
    sample_code()

if __name__=="__main__":
    main()
