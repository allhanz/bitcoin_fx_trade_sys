#!/usr/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance
import seaborn as sns
sns.set(style="darkgrid")
from matplotlib.dates import date2num
import time
#seaborn API
#https://seaborn.pydata.org/api.html

def matplot_line(pd_data,col_x,col_y):
    cols=pd_data.columns
    if col_x in clos and col_y in clos:

        plt.plot(col_x, col_y, data=pd_data)
        plt.show()

def matplot_candles(pd_data,col_x,col_y):
    print("not finished...")

def plot_line(pd_data,col_x,col_y):

#    if pd_data.empty:
#        print("pd_data empty......")
#        return 

    cols=pd_data.columns
    #cols=["time","value"]
    if col_x in cols and col_y in cols:
        #for test
        #pd_data= pd.DataFrame(dict(time=np.arange(500),value=np.random.randn(500).cumsum()))
        g = sns.lineplot(x=col_x, y=col_y,data=pd_data)
        #g.fig.autofmt_xdate()
    else:
        print("plot error.....")

def plot_candles(pd_data,col_x,col_y):

    if pd_data.empty:
        print("pd_data empty......")
        return 
    cols=pd_data.columns
    if col_x in cols and col_y in cols:
        #for test
        #pd_data= pd.DataFrame(dict(time=np.arange(500),value=np.random.randn(500).cumsum()))
        g = sns.regplot(x=col_x, y=col_y, kind="line", data=od_data)
        g.fig.autofmt_xdate()

#old version
"""
def plot_candles(time_stamp, price):
    print("plot_candles")

    time_start=time_stamp[0]

    length=len(time_stamp)
    print(length)
    time_end = time_stamp[length-1]

    # print(time_stamp)

    print(str(time_start[0]))
    print(str(time_end[0]))


    idx = pd.date_range(str(time_start[0]), str(time_end[0]), freq='H')
    # print(type(price.T))
    # print(np.shape(price.T))
    print(idx)

    # new_price=np.reshape(price.T, (201,))
    # print(new_price)

    df = pd.Series(price.T[0], index=idx).resample('B').ohlc()
    fig = plt.figure()
    ax = plt.subplot()

    xdate = [x.date() for x in df.index]  # Timestamp -> datetime

    # print(xdate)
    ohlc = np.vstack((date2num(xdate), df.values.T)).T  # datetime -> float
    print(df.values)
    mpf.candlestick_ohlc(ax, ohlc, width=0.1, colorup='g', colordown='r')
    ax.grid()  # グリッド表示
    ax.set_xlim(df.index[0].date(), df.index[-1].date())  # x軸の範囲
    fig.autofmt_xdate()  # x軸のオートフォーマット

    fig.show()
"""

def main():
    #for test
    print("tested,NG....")
    plot_line(None,"time","value")

if __name__=="__main__":
    main()
