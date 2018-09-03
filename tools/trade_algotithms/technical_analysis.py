import os
import sys
sys.path.append(os.path.abspath("../"))
import pandas as pd
import numpy as np
import bokeh_plot_api
import talib

#talib api website
#https://github.com/elsen-trading/talib

def period_candle_process(pd_data,time_period,time_col_name):
    #pd_data includes time date information
    #time_period
    if time_col_name=="" or time_col_name==None:
        time_col_name=="time"
    if time_period:
        pass

def candle_rate(np_array):
    #np_array data includes high low open_price close_price
    pass


def moving_average(pd_data,period_time):
    if not isinstance(pd_data,pd.DataFrame):
        print("pd_data is pandas dataframe data type...")
        return 
    average_=pd_data.rolling(window=period_time,min_periods=period_time)
    if average_:
        return average_
    else:
        print("data  error....")

# 単純移動平均(SMA: Simple Moving Average)
def check_np_array(np_array):
    if isinstance(np_array,np):
        return True
    else:
        return False

def sma(np_array):
    if check_np_array(np_array):
        return talib.SMA(np_array)

# 加重移動平均(WMA: Weighted Moving Average)
def wma(np_array):
    if check_np_array(np_array):
        return talib.WMA(np_array)

# 指数移動平均(EMA: Exponential Moving Average)
def ema(np_array):
    if check_np_array(np_array): 
        return talib.EMA(np_array)

# ２重指数移動平均(DEMA: Double Exponential Moving Average)
def dema(np_array):
    if check_np_array(np_array):
        return talib.DEMA(np_array)

# ３重指数移動平均(TEMA: Triple Exponential Moving Average)
def t3ema(np_array):
    if check_np_array(np_array):
        return talib.T3(np_array)

# 三角移動平均(TMA: Triangular Moving Average)
def triangularMA(np_array):
    if check_np_array(np_array):
        return talib.TRIMA(np_array)

# Kaufmanの適応型移動平均(KAMA: Kaufman Adaptive Moving Average)
def kaufmanMA(np_array):
    if check_np_array(np_array):
        return talib.KAMA(np_array)

# MESAの適応型移動平均(MAMA: MESA Adaptive Moving Average)
def mama(np_array):
    cols = ['MAMA', 'FAMA']
    if check_np_array(np_array):
        return talib.MAMA(np_array)

# トレンドライン(Hilbert Transform - Instantaneous Trendline)
def hiTrans(np_array):
    if check_np_array(np_array):
        return talib.HT_TRENDLINE(np_array)

# ボリンジャー・バンド(Bollinger Bands)
def bbands(np_array):
    cols = ['BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband']
    if check_np_array(np_array):
        return talib.BBANDS(np_array)


# MidPoint over period
def midPoint(np_array):
    if check_np_array(np_array):
        return talib.MIDPOINT(np_array)

# 変化率(ROC: Rate of change Percentage)
def roc(np_array): #key function
    if check_np_array(np_array):
        return talib.ROCP(np_array)

# モメンタム(Momentum)
def momentum(np_array):
    if check_np_array(np_array):
        return talib.MOM(np_array)

# RSI: Relative Strength Index
def rsi(np_array):
    if check_np_array(np_array):
        return talib.RSI(np_array)

# MACD: Moving Average Convergence/Divergence
def macd(np_array):
    cols = ['MACD', 'MACD_signal', 'MACD_hist']
    if check_np_array(np_array):
        return talib.MACD(np_array):

# APO: Absolute Price Oscillator
def apo(np_array):
    if check_np_array(np_array):
        return talib.APO(np_array)

# PPO: Percentage Price Oscillator
def ppo(np_array):
    if check_np_array(np_array):
        return talib.PPO(np_array)

# CMO: Chande Momentum Oscillator
def cmo(np_array):
    if check_np_array(np_array):
        return output, talib.CMO(np_array)

# ヒルベルト変換 - Dominant Cycle Period
def dcPeriod(np_array):
    if check_np_array(np_array):
        return talib.HT_DCPERIOD(np_array)

# ヒルベルト変換 - Dominant Cycle Phase
def dcPhase(np_array):
    if check_np_array(np_array):
        return talib.HT_DCPHASE(np_array)

# ヒルベルト変換 - Phasor Components
def phasor(np_array):
    cols = ['HT_PHASOR_inphase', 'HT_PHASOR_quadrature']
    if check_np_array(np_array):
        return talib.HT_PHASOR(np_array):

# ヒルベルト変換 - SineWave
def sineWave(np_array):
    cols = ['HT_SINE_sine', 'HT_SINE_leadsine']    
    if check_np_array(np_array):
        return talib.HT_SINE(np_array)

# ヒルベルト変換 - Trend vs Cycle Mode
def trendCycleMode(np_array):
    if check_np_array(np_array):
        alib.HT_TRENDMODE(np_array)

# 60日単純移動平均
def sma_60(np_array):
    if check_np_array(np_array):
        return talib.SMA(np_array, timeperiod=60)

# 15日ボリンジャー・バンド
def bbands_15(np_array):
    cols = ['BBANDS15_upperband', 'BBANDS15_middleband', 'BBANDS15_lowerband
    if check_np_array(np_array):
        talib.BBANDS(np_array, timeperiod=15, nbdevup=2, nbdevdn=2, matype=0):
']

# 21日RSI
def rsi_21(np_array):
    if check_np_array(np_array):
        return talib.RSI(np_array, timeperiod=21)

def main():
    pass

if __name__=="__name__":
    main()


