import os
import sys
import talib
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import num2date, date2num
from matplotlib.dates import DateFormatter, WeekdayLocator,DayLocator, MONDAY
import trade_algotithms.technical_analysis
import env_settings as env
from matplotlib.dates import date2num
from plotly.offline import init_notebook_mode, iplot
import plotly
import plotly.figure_factory as FF
import plotly.graph_objs as go
import plotly.plotly as py

def test_code():
    #test ok
    import matplotlib.ticker as ticker
    import numpy as np
    import matplotlib.dates
    import pandas

    dates = [732797.0, 732828.0, 732858.0, 732889.0, 732920.0, 732950.0, 732981.0, 733011.0, 733042.0, 733073.0, 733102.0, 733133.0, 733163.0, 733194.0, 733224.0, 733255.0, 733286.0, 733316.0, 733347.0, 733377.0, 733408.0, 733439.0, 733467.0, 733498.0, 733528.0, 733559.0, 733589.0, 733620.0, 733651.0, 733681.0, 733712.0, 733742.0, 733773.0, 733804.0, 733832.0, 733863.0, 733893.0, 733924.0, 733954.0, 733985.0, 734016.0, 734046.0, 734077.0, 734107.0, 734138.0, 734169.0, 734197.0, 734228.0, 734258.0, 734289.0, 734319.0, 734350.0, 734381.0, 734411.0, 734442.0, 734472.0, 734503.0, 734534.0, 734563.0, 734594.0, 734624.0, 734655.0, 734685.0, 734716.0, 734747.0, 734777.0, 734808.0, 734838.0, 734869.0, 734900.0, 734928.0, 734959.0, 734989.0, 735020.0, 735050.0, 735081.0, 735112.0, 735142.0, 735173.0, 735203.0, 735234.0, 735265.0, 735293.0, 735324.0, 735354.0, 735385.0, 735415.0, 735446.0, 735477.0, 735507.0, 735538.0, 735568.0, 735599.0, 735630.0, 735658.0, 735689.0, 735719.0, 735750.0, 735780.0, 735811.0, 735842.0, 735872.0, 735903.0, 735933.0, 735964.0, 735995.0, 736024.0, 736055.0, 736085.0, 736116.0, 736146.0, 736177.0, 736208.0, 736238.0, 736269.0, 736299.0, 736330.0, 736361.0, 736389.0, 736420.0, 736450.0]
    kurse_o = [60.0, 68.15, 68.08, 65.01, 66.1, 70.59, 75.69, 69.12, 66.25, 53.15, 54.61, 54.12, 50.81, 49.0, 39.09, 36.5, 39.6, 35.75, 27.56, 24.22, 27.3, 21.83, 17.74, 19.0, 27.57, 26.62, 25.78, 32.4, 31.92, 34.5, 32.7, 34.1, 37.24, 33.0, 31.15, 35.08, 38.31, 40.75, 41.46, 41.14, 38.5, 46.32, 48.1, 50.51, 50.9, 54.0, 51.56, 50.31, 52.3, 49.2, 51.9, 51.52, 37.76, 32.2, 35.52, 33.48, 33.92, 42.42, 44.8, 45.76, 42.6, 37.3, 35.4, 40.44, 38.87, 37.82, 36.05, 38.1, 42.03, 42.9, 45.67, 42.55, 41.83, 48.9, 46.5, 52.77, 52.92, 57.64, 60.46, 61.14, 63.21, 62.13, 65.49, 68.97, 67.02, 70.0, 68.58, 61.51, 62.2, 60.39, 62.0, 67.2, 68.26, 80.66, 86.79, 89.7, 87.07, 86.2, 83.5, 81.25, 70.36, 66.14, 78.08, 85.1, 75.26, 64.23, 62.89, 66.9, 61.15, 61.36, 53.93, 61.4, 62.29, 62.85, 65.26, 62.4, 70.18, 70.25, 69.2, 69.55, 68.51]
    kurse_h = [68.49, 69.66, 71.0, 67.2, 71.14, 78.85, 76.64, 71.6, 66.61, 57.81, 56.07, 55.94, 53.2, 49.0, 43.8, 44.44, 43.45, 35.75, 28.3, 26.74, 28.4, 25.98, 23.1, 28.2, 29.03, 28.51, 32.84, 33.99, 34.7, 37.9, 36.37, 37.9, 37.67, 34.95, 35.52, 39.9, 41.92, 44.8, 44.7, 42.75, 47.59, 50.05, 52.63, 55.05, 59.09, 57.22, 52.48, 53.69, 53.03, 51.93, 53.95, 51.81, 37.88, 39.85, 36.95, 35.09, 43.79, 48.9, 48.95, 46.46, 42.8, 37.36, 40.9, 42.44, 40.57, 39.82, 38.23, 42.01, 44.31, 46.06, 47.27, 43.42, 50.37, 49.82, 53.95, 56.1, 59.56, 60.96, 61.36, 63.19, 66.85, 67.81, 69.59, 71.27, 70.0, 70.8, 70.65, 63.62, 65.75, 62.38, 67.8, 70.2, 81.3, 86.51, 96.07, 92.7, 91.0, 87.63, 86.59, 85.12, 76.72, 79.89, 84.73, 85.5, 75.26, 65.86, 68.52, 66.95, 62.1, 61.41, 62.49, 63.8, 64.59, 66.5, 66.36, 71.4, 73.23, 70.94, 73.0, 69.68, 69.29]
    kurse_l = [57.91, 63.53, 63.28, 57.75, 63.55, 70.43, 63.2, 63.88, 46.65, 49.52, 50.51, 48.05, 48.46, 38.65, 35.3, 36.05, 33.7, 17.92, 19.61, 22.15, 20.35, 17.69, 17.2, 18.6, 23.98, 24.03, 23.52, 30.21, 30.1, 32.2, 31.35, 34.0, 32.32, 29.92, 30.74, 34.79, 35.3, 39.47, 39.95, 37.02, 38.3, 43.59, 47.22, 50.09, 50.75, 49.64, 43.56, 48.36, 47.0, 45.7, 49.1, 33.27, 30.92, 30.52, 29.02, 31.1, 33.92, 42.34, 43.11, 39.4, 36.7, 32.86, 34.9, 38.34, 37.36, 35.85, 35.14, 37.74, 41.7, 41.82, 42.1, 38.14, 41.65, 43.16, 45.96, 50.95, 51.89, 56.96, 57.57, 58.05, 60.34, 58.78, 62.65, 63.94, 64.19, 67.46, 61.57, 57.1, 59.34, 55.1, 60.23, 64.13, 65.57, 79.78, 84.65, 84.65, 83.0, 79.03, 77.25, 65.4, 62.06, 62.91, 75.1, 72.48, 62.73, 57.01, 62.36, 58.9, 56.19, 52.0, 50.83, 58.01, 60.14, 62.7, 60.02, 61.61, 68.44, 66.13, 68.91, 64.96, 67.05]
    kurse_c = [68.15, 68.59, 66.89, 65.18, 70.64, 75.95, 69.55, 66.5, 52.19, 55.79, 54.15, 50.15, 48.92, 39.28, 37.33, 39.9, 35.4, 26.81, 24.66, 26.7, 22.0, 18.01, 19.08, 27.14, 25.85, 25.78, 32.47, 31.53, 34.4, 33.08, 33.72, 37.23, 33.42, 30.66, 34.86, 38.82, 41.0, 41.92, 41.38, 38.36, 46.46, 47.43, 49.87, 51.32, 53.42, 51.05, 49.85, 52.19, 49.1, 51.9, 50.66, 37.67, 33.63, 37.0, 33.61, 33.92, 42.24, 45.4, 45.21, 41.76, 37.43, 35.34, 40.71, 39.0, 37.66, 36.02, 37.98, 41.32, 42.88, 45.66, 42.44, 42.02, 49.41, 46.48, 52.22, 51.92, 57.62, 60.44, 61.0, 62.9, 62.13, 67.52, 68.59, 66.73, 69.7, 68.4, 61.88, 62.24, 60.73, 62.03, 67.8, 68.97, 80.48, 86.51, 89.73, 86.33, 85.28, 81.64, 81.39, 71.66, 64.85, 78.97, 84.73, 77.58, 64.16, 63.1, 67.37, 60.69, 61.39, 53.52, 60.82, 62.08, 62.71, 64.91, 62.76, 70.72, 69.35, 68.64, 69.2, 68.4, 69.07]

    quotes = [tuple([dates[i],
                    kurse_o[i],
                    kurse_h[i],
                    kurse_l[i],
                    kurse_c[i]]) for i in range(len(dates))] #_1

    fig, (ax,ax2) = plt.subplots(1,2, sharey=True)

    candlestick_ohlc(ax, quotes, width=0.6)
    candlestick_ohlc(ax2, quotes, width=0.6)

    # ---------------------------------------------------------

    sma = [[kurse_c[i] * 0.8] for i in range(len(dates))]
    data = pandas.DataFrame(sma, index=dates, columns=["sma"]) #_2
    # data = data.astype(float)

    data["sma"].plot(ax=ax)

    # ---------------------------------------------------------

    fig.autofmt_xdate()
    fig.tight_layout()

    ax.set_ylim(0,100)
    ax2.set_ylim(0,100)

    axlim = ax.get_xlim()
    ax.set_xlim(axlim)
    ax2.set_xlim(axlim)

    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax.grid(True)

    ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax2.grid(True)

    plt.savefig('Test.png')

    plt.show()

def sample_code():
    sample_data = [
    [732797.0, 10, 18,  5, 20],
    [732828.0, 12, 21,  7, 22],
    [732858.0, 14, 24, 9 , 24],
    [732889.0, 16, 27, 11, 26],
    [732920.0, 18, 30, 13, 28],
    [732950.0, 20, 33, 15, 30],
    [732981.0, 22, 36, 17, 32],
    [733011.0, 24, 39, 19, 34],
    [733042.0, 26, 41, 21, 38],
    [733073.0, 30, 45, 25, 40],
    [733102.0, 43, 44, 42, 43],
    [733133.0, 46, 47, 45, 46],
    [733163.0, 44, 45, 43, 44],
    [733194.0, 40, 55, 35, 50],
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

    quotes = [tuple([sample_data[i][0],
                 sample_data[i][1],
                 sample_data[i][2],
                 sample_data[i][3],
                 sample_data[i][4]]) for i in range(sample_data.shape[0])] #_1

    fig, (ax,ax2) = plt.subplots(1,2, sharey=True)

    candlestick_ohlc(ax, quotes, width=0.6)
    candlestick_ohlc(ax2, quotes, width=0.6)


    fig.autofmt_xdate()
    fig.tight_layout()

    ax.set_ylim(0,100)
    ax2.set_ylim(0,100)

    axlim = ax.get_xlim()
    ax.set_xlim(axlim)
    ax2.set_xlim(axlim)

    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax.grid(True)

    ax2.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax2.grid(True)

    plt.savefig('Test.png')

    plt.show()

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
'''    
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
'''

class candlesticks_pattern_detect_lib():
    #website:https://github.com/mrjbq7/ta-lib

    '''
    CDL2CROWS            Two Crows
    CDL3BLACKCROWS       Three Black Crows
    CDL3INSIDE           Three Inside Up/Down
    CDL3LINESTRIKE       Three-Line Strike
    CDL3OUTSIDE          Three Outside Up/Down
    CDL3STARSINSOUTH     Three Stars In The South
    CDL3WHITESOLDIERS    Three Advancing White Soldiers
    CDLABANDONEDBABY     Abandoned Baby
    CDLADVANCEBLOCK      Advance Block
    CDLBELTHOLD          Belt-hold
    CDLBREAKAWAY         Breakaway
    CDLCLOSINGMARUBOZU   Closing Marubozu
    CDLCONCEALBABYSWALL  Concealing Baby Swallow
    CDLCOUNTERATTACK     Counterattack
    CDLDARKCLOUDCOVER    Dark Cloud Cover
    CDLDOJI              Doji
    CDLDOJISTAR          Doji Star
    CDLDRAGONFLYDOJI     Dragonfly Doji
    CDLENGULFING         Engulfing Pattern
    CDLEVENINGDOJISTAR   Evening Doji Star
    CDLEVENINGSTAR       Evening Star
    CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines
    CDLGRAVESTONEDOJI    Gravestone Doji
    CDLHAMMER            Hammer
    CDLHANGINGMAN        Hanging Man
    CDLHARAMI            Harami Pattern
    CDLHARAMICROSS       Harami Cross Pattern
    CDLHIGHWAVE          High-Wave Candle
    CDLHIKKAKE           Hikkake Pattern
    CDLHIKKAKEMOD        Modified Hikkake Pattern
    CDLHOMINGPIGEON      Homing Pigeon
    CDLIDENTICAL3CROWS   Identical Three Crows
    CDLINNECK            In-Neck Pattern
    CDLINVERTEDHAMMER    Inverted Hammer
    CDLKICKING           Kicking
    CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu
    CDLLADDERBOTTOM      Ladder Bottom
    CDLLONGLEGGEDDOJI    Long Legged Doji
    CDLLONGLINE          Long Line Candle
    CDLMARUBOZU          Marubozu
    CDLMATCHINGLOW       Matching Low
    CDLMATHOLD           Mat Hold
    CDLMORNINGDOJISTAR   Morning Doji Star
    CDLMORNINGSTAR       Morning Star
    CDLONNECK            On-Neck Pattern
    CDLPIERCING          Piercing Pattern
    CDLRICKSHAWMAN       Rickshaw Man
    CDLRISEFALL3METHODS  Rising/Falling Three Methods
    CDLSEPARATINGLINES   Separating Lines
    CDLSHOOTINGSTAR      Shooting Star
    CDLSHORTLINE         Short Line Candle
    CDLSPINNINGTOP       Spinning Top
    CDLSTALLEDPATTERN    Stalled Pattern
    CDLSTICKSANDWICH     Stick Sandwich
    CDLTAKURI            Takuri (Dragonfly Doji with very long lower shadow)
    CDLTASUKIGAP         Tasuki Gap
    CDLTHRUSTING         Thrusting Pattern
    CDLTRISTAR           Tristar Pattern
    CDLUNIQUE3RIVER      Unique 3 River
    CDLUPSIDEGAP2CROWS   Upside Gap Two Crows
    CDLXSIDEGAP3METHODS  Upside/Downside Gap Three Methods
    '''

    def __init__(self,ohlc_pd=None):
        print("this is the candlestick pattern detection lib....")
        self.open_np=None
        self.high_np=None
        self.low_np=None
        self.close_np=None
        self.detect_res={}
        self.cdl_ptn_index={}
        self.detect_list_enum=[
                "CDL2CROWS",
                "CDL3BLACKCROWS",
                "CDL3INSIDE",
                "CDL3LINESTRIKE",
                "CDL3OUTSIDE",
                "CDL3STARSINSOUTH",
                "CDL3WHITESOLDIERS",
                "CDLABANDONEDBABY",
                "CDLADVANCEBLOCK",
                "CDLBELTHOLD",
                "CDLBREAKAWAY",
                "CDLCLOSINGMARUBOZU",
                "CDLCONCEALBABYSWALL",
                "CDLCOUNTERATTACK",
                "CDLDARKCLOUDCOVER",
                "CDLDOJI",
                "CDLDOJISTAR",
                "CDLDRAGONFLYDOJI",
                "CDLENGULFING",
                "CDLEVENINGDOJISTAR",
                "CDLEVENINGSTAR",
                "CDLGAPSIDESIDEWHITE",
                "CDLGRAVESTONEDOJI",
                "CDLHAMMER",
                "CDLHANGINGMAN",
                "CDLHARAMI",
                "CDLHARAMICROSS",
                "CDLHIGHWAVE",
                "CDLHIKKAKE",
                "CDLHIKKAKEMOD",
                "CDLHOMINGPIGEON",
                "CDLIDENTICAL3CROWS",
                "CDLINNECK",
                "CDLINVERTEDHAMMER",
                "CDLKICKING",
                "CDLKICKINGBYLENGTH",
                "CDLLADDERBOTTOM",
                "CDLLONGLEGGEDDOJI",
                "CDLLONGLINE",
                "CDLMARUBOZU",
                "CDLMATCHINGLOW",
                "CDLMATHOLD",
                "CDLMORNINGDOJISTAR",
                "CDLMORNINGSTAR",
                "CDLONNECK",
                "CDLPIERCING",
                "CDLRICKSHAWMAN",
                "CDLRISEFALL3METHODS",
                "CDLSEPARATINGLINES",
                "CDLSHOOTINGSTAR",
                "CDLSHORTLINE",
                "CDLSPINNINGTOP",
                "CDLSTALLEDPATTERN",
                "CDLSTICKSANDWICH",
                "CDLTAKURI",
                "CDLTASUKIGAP",
                "CDLTHRUSTING",
                "CDLTRISTAR",
                "CDLUNIQUE3RIVER",
                "CDLUPSIDEGAP2CROWS",
                "CDLXSIDEGAP3METHODS"
            ]
        self.mapping_sheet={
                "CDL2CROWS":talib.CDL2CROWS,
                "CDL3BLACKCROWS":talib.CDL3BLACKCROWS,
                "CDL3INSIDE":talib.CDL3INSIDE,
                "CDL3LINESTRIKE":talib.CDL3LINESTRIKE,
                "CDL3OUTSIDE":talib.CDL3OUTSIDE,
                "CDL3STARSINSOUTH":talib.CDL3STARSINSOUTH,
                "CDL3WHITESOLDIERS":talib.CDL3WHITESOLDIERS,
                "CDLABANDONEDBABY":talib.CDLABANDONEDBABY,
                "CDLADVANCEBLOCK":talib.CDLADVANCEBLOCK,
                "CDLBELTHOLD":talib.CDLBELTHOLD,
                "CDLBREAKAWAY":talib.CDLBREAKAWAY,
                "CDLCLOSINGMARUBOZU":talib.CDLCLOSINGMARUBOZU,
                "CDLCONCEALBABYSWALL":talib.CDLCONCEALBABYSWALL,
                "CDLCOUNTERATTACK":talib.CDLCOUNTERATTACK,
                "CDLDARKCLOUDCOVER":talib.CDLDARKCLOUDCOVER,
                "CDLDOJI":talib.CDLDOJI,
                "CDLDOJISTAR":talib.CDLDOJISTAR,
                "CDLDRAGONFLYDOJI":talib.CDLDRAGONFLYDOJI,
                "CDLENGULFING":talib.CDLENGULFING,
                "CDLEVENINGDOJISTAR":talib.CDLEVENINGDOJISTAR,
                "CDLEVENINGSTAR":talib.CDLEVENINGSTAR,
                "CDLGAPSIDESIDEWHITE":talib.CDLGAPSIDESIDEWHITE,
                "CDLGRAVESTONEDOJI":talib.CDLGRAVESTONEDOJI,
                "CDLHAMMER":talib.CDLHAMMER,
                "CDLHANGINGMAN":talib.CDLHANGINGMAN,
                "CDLHARAMI":talib.CDLHARAMI,
                "CDLHARAMICROSS":talib.CDLHARAMICROSS,
                "CDLHIGHWAVE":talib.CDLHIGHWAVE,
                "CDLHIKKAKE":talib.CDLHIKKAKE,
                "CDLHIKKAKEMOD":talib.CDLHIKKAKEMOD,
                "CDLHOMINGPIGEON":talib.CDLHOMINGPIGEON,
                "CDLIDENTICAL3CROWS":talib.CDLIDENTICAL3CROWS,
                "CDLINNECK":talib.CDLINNECK,
                "CDLINVERTEDHAMMER":talib.CDLINVERTEDHAMMER,
                "CDLKICKING":talib.CDLKICKING,
                "CDLKICKINGBYLENGTH":talib.CDLKICKINGBYLENGTH,
                "CDLLADDERBOTTOM":talib.CDLLADDERBOTTOM,
                "CDLLONGLEGGEDDOJI":talib.CDLLONGLEGGEDDOJI,
                "CDLLONGLINE":talib.CDLLONGLINE,
                "CDLMARUBOZU":talib.CDLMARUBOZU,
                "CDLMATCHINGLOW":talib.CDLMATCHINGLOW,
                "CDLMATHOLD":talib.CDLMATHOLD,
                "CDLMORNINGDOJISTAR":talib.CDLMORNINGDOJISTAR,
                "CDLMORNINGSTAR":talib.CDLMORNINGSTAR,
                "CDLONNECK":talib.CDLONNECK,
                "CDLPIERCING":talib.CDLPIERCING,
                "CDLRICKSHAWMAN":talib.CDLRICKSHAWMAN,
                "CDLRISEFALL3METHODS":talib.CDLRISEFALL3METHODS,
                "CDLSEPARATINGLINES":talib.CDLSEPARATINGLINES,
                "CDLSHOOTINGSTAR":talib.CDLSHOOTINGSTAR,
                "CDLSHORTLINE":talib.CDLSHORTLINE,
                "CDLSPINNINGTOP":talib.CDLSPINNINGTOP,
                "CDLSTALLEDPATTERN":talib.CDLSTALLEDPATTERN,
                "CDLSTICKSANDWICH":talib.CDLSTICKSANDWICH,
                "CDLTAKURI":talib.CDLTAKURI,
                "CDLTASUKIGAP":talib.CDLTASUKIGAP,
                "CDLTHRUSTING":talib.CDLTHRUSTING,
                "CDLTRISTAR":talib.CDLTRISTAR,
                "CDLUNIQUE3RIVER":talib.CDLUNIQUE3RIVER,
                "CDLUPSIDEGAP2CROWS":talib.CDLUPSIDEGAP2CROWS,
                "CDLXSIDEGAP3METHODS":talib.CDLXSIDEGAP3METHODS,
        }
        self.function_names = ['CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE', 'CDL3OUTSIDE', 'CDL3STARSINSOUTH', 'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLBELTHOLD', 'CDLBREAKAWAY', 'CDLCLOSINGMARUBOZU', 'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLDOJI', 'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLENGULFING', 'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR', 'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLHARAMICROSS', 'CDLHIGHWAVE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON', 'CDLIDENTICAL3CROWS', 'CDLINNECK', 'CDLINVERTEDHAMMER', 'CDLKICKING', 'CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM', 'CDLLONGLEGGEDDOJI', 'CDLLONGLINE', 'CDLMARUBOZU', 'CDLMATCHINGLOW', 'CDLMATHOLD', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR', 'CDLONNECK', 'CDLPIERCING', 'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES', 'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP', 'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI', 'CDLTASUKIGAP', 'CDLTHRUSTING', 'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS']
        self.ohlc_pd=ohlc_pd
        if isinstance(ohlc_pd,pd.DataFrame):
            if not ohlc_pd.empty:
                self.ohlc_np=self.ohlc_pd_to_array(ohlc_pd)
        else:
            self.ohlc_np=None

    def plot_candlestick(self):
        #has problem
        #init_notebook_mode(connected=True) # Jupyter notebook用設定
        if not self.ohlc_pd.empty:
            fig = FF.create_candlestick(self.ohlc_pd.open,self.ohlc_pd.high,self.ohlc_pd.low,self.ohlc_pd.close, dates=self.ohlc_pd.index)
            plotly.offline.plot(fig, filename='candlestick_analysic.html')
            #mcd_candle = go.Candlestick(x=self.ohlc_pd.index,open=self.ohlc_pd.open,high=self.ohlc_pd.high,low=self.ohlc_pd.low,close=self.ohlc_pd.close)
        #    data = [mcd_candle]
        #    py.iplot(data, filename='Candle Stick')

    
    def get_cdl_location_index(self):
        #get the candlesticks pattern location
        for key in self.detect_res.keys():
            res_list=self.detect_res[key]
            location_index_list=[]
            for i,x in enumerate(res_list):
                if x<0 or x>0:
                    location_index_list.append((i,x))
            if len(location_index_list)>0:
                self.cdl_ptn_index[key]=location_index_list
    
    def ohlc_pd_to_array(self,ohlc_pd):
        cols=ohlc_pd.columns

        if "open" in cols:
            self.open_np=ohlc_pd["open"]
        if "high" in cols:
            self.high_np=ohlc_pd["high"]
        if "low" in cols:
            self.low_np=ohlc_pd["low"]
        if "close" in cols:
            self.close_np=ohlc_pd["close"]
        if len(self.open_np)>0 and len(self.high_np)>0 and len(self.low_np)>0 and len(self.close_np)>0:
            self.ohlc_np=(self.open_np,self.high_np,self.low_np,self.close_np)
            print("ohlc_np:\n",self.ohlc_np)
        else:
            print("data error")

    def pattern_detector(self,detect_func_list,ohlc_pd,detect_type):
        if not isinstance(ohlc_pd,type(None)):
            self.ohlc_pd=ohlc_pd
            self.ohlc_np=self.ohlc_pd_to_array(ohlc_pd)
        if detect_type=="all":
            for item in self.mapping_sheet.keys():
                res=self.mapping_sheet[item](self.open_np,self.high_np,self.low_np,self.close_np)
                self.detect_res[item]=res
        else:
            for item_detect in detect_func_list:
                if item_detect in self.mapping_sheet.keys():
                    res=self.mapping_sheet[item_detect](self.open_np,self.high_np,self.low_np,self.close_np)
                    self.detect_res[item_detect]=res

def main():
    test_file=env.test_file
    pd_data=pd.read_csv(test_file,names=['Symbol', 'Date_Time', 'Bid', 'Ask'],encoding="utf-8",index_col=1, parse_dates=True)
    print("length of the pd_data:",len(pd_data))
    #pd_data.columns=['Symbol', 'Date_Time', 'Bid', 'Ask']
    #test_pd=pd_data.iloc[:10000]
    test_pd=pd_data.copy()
    #print("last data:\n",test_pd.iloc[-1])
    #test_pd["Date_Time"]=pd.to_datetime(test_pd["Date_Time"],format='%Y%m%d %H:%M:%S', errors='coerce')
    #print("test_pd:\n",test_pd)
    time_interval="5T"
    data_ask =  test_pd['Ask'].resample(time_interval).ohlc()
    data_bid =  test_pd['Bid'].resample(time_interval).ohlc()
    #print("data_ask head data:\n",data_ask)
    #print("data_bid head data:\n",data_bid)
    ohlc_pd=pd.concat([data_ask, data_bid], axis=1, keys=['Ask', 'Bid'])
    #print("ohlc_pd head:\n",ohlc_pd.head())
    #cdl_detector=candlesticks_pattern_detect_lib(ohlc_pd=ohlc_pd)
    print("data_bid length:\n",len(data_bid))
    print("bid ohlc data:\n",data_bid)
    cdl_detector=candlesticks_pattern_detect_lib(ohlc_pd=data_bid)
    detect_name=["CDLTRISTAR"]
    cdl_detector.pattern_detector(detect_name,None,None)
    cdl_detector.plot_candlestick()

    print("detect_res:\n",cdl_detector.detect_res.values())
    print("lenght of detect_res:\n",len(cdl_detector.detect_res.values()))
    cdl_detector.get_cdl_location_index()
    print("index info:\n",cdl_detector.cdl_ptn_index)
    #cdl_detector.plot_candlestick()

if __name__=="__main__":
    main()
    #test_code()
    #sample_code()