#!/usr/bin/python3
# coding=utf-8
#from the following website
#https://raw.githubusercontent.com/ZhangZhaofeng/simu_var_hilo/master/technical_fx_var_hilo.py

import talib
import numpy as np
import historical_fx
import os
import pandas as pd
# import plot_chart as plc
import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick_ohlc as plot_candle
import time,math


class HILO:
    def __init__(self):
        print("HILO initialized")
        self.btc_charts = historical_fx.charts()

    def MA(self, ndarray, timeperiod=5):
        #x = np.array([talib.MA(ndarray.T[0], timeperiod)])
        x = np.asarray([talib.MA(ndarray.T[0], timeperiod)])
        # print(x)
        return x.T

    def get_HIGH_MA(self, HIGH, var_day = 23):  # price=1*N (N>61)
        ma_high=self.MA(HIGH,var_day)
        return ma_high

    def get_LOW_MA(self, LOW, var_day = 23):  # price=1*N (N>61)
        ma_low=self.MA(LOW,var_day)
        return ma_low

    def get_long_price(self, HIGH, var_day = 23):
        ma_high=self.get_HIGH_MA(HIGH, var_day)
        return ma_high

    def get_short_price(self, LOW, var_day = 23):
        ma_low = self.get_LOW_MA(LOW, var_day)
        return ma_low

    def calcalate_er(self, open_price, high_price, low_price, close_price ,num=15, periods='1H'):

        abs_all_hilo = np.sum(abs(high_price - low_price))
        abs_act_hilo = abs(max(high_price) -min(low_price))

        er = abs_act_hilo / abs_all_hilo
        time_unit = math.floor((1-er) * 70 + 1)
        return (er,time_unit)

    def publish_current_hilo_price(self, num=100, periods="1H"):
        (time_stamp, open_price, high_price, low_price, close_price) = self.btc_charts.get_price_array_till_finaltime(
            final_unixtime_stamp=time.time(), num=num, periods=periods, converter=True)

        [er, time_unit] = self.calcalate_er()
        low_price_ma = self.get_short_price(low_price, time_unit)
        high_price_ma = self.get_long_price(high_price, time_unit)
        (buyprice, sellprice)=(high_price_ma[-1][0],low_price_ma[-1][0])
        a=(int(buyprice), int(sellprice))
        print(a)
        return (int(buyprice), int(sellprice))

    def trade_short(self, inprice, outprice, cash = 10000):
        # return profit
        return((inprice-outprice)*cash/inprice)

    def trade_long(self, inprice, outprice, cash = 10000):
        # return profit
        return((outprice-inprice)*cash/inprice)

    def simulate(self, num=100, periods="1m" ,end_offset=0):
        mode=0  #0: both long and short;
                #1: only long;
                #2: only short;


        leverage = 1.0
        fee_ratio = 0.000  # trading fee percent
        ################Simulation#######################
        (time_stamp, open_price, high_price, low_price, close_price) = self.btc_charts.get_price_array_till_finaltime(
            final_unixtime_stamp=time.time() - end_offset, num=num, periods=periods, converter=True)


        all = np.c_[time_stamp, open_price, high_price, low_price, close_price]
        long_price = self.get_long_price(high_price)
        short_price = self.get_short_price(low_price)

        for t in range(50, len(all)):
            [er, time_unit] = self.calcalate_er(open_price[t-5:t], high_price[t-5:t], low_price[t-5:t], close_price[t-5:t])
            long_price[t] = self.get_long_price(high_price, time_unit)[t]
            short_price[t] = self.get_short_price(low_price, time_unit)[t]

            print(time_unit)
        print(len(long_price))
        print(len(short_price))


        amount = np.zeros([len(all), 7])
        long = False
        short = False
        cash = 10000.
        trading_cash = 10000.
        prev_cash=cash
        btc = 0.
        value = cash
        long_times = 0
        short_times = 0
        short_start_price= 0.
        long_start_price = 0.
        trade_back=0
        slide = 0
        breakfactor =0
        for t in range(50, len(all)):
            # (gradient_real, grad_w_real)=self.get_current_GMMA_gradient_realtime(ema[t-1], all[t][2], periods)
            #current hour's operation price initialization
            buy_price = long_price[t]
            sell_price = short_price[t]


            if not short and not long:

                if all[t][4] < sell_price*(1-breakfactor):   #low < sell_price
                    #short starts
                    short = True
                    long = False
                    short_start_price = all[t][4] - slide
                    short_times += 1
                    amount[t][5] = 5


                    #Current hour processing

                elif all[t][4] > buy_price: # high > buy_price
                    # long starts
                    long = True
                    short = False
                    long_start_price = all[t][4] + slide
                    long_times += 1
                    amount[t][5] = 8

            elif short and not long:

                line = sell_price+(buy_price-sell_price)/2*(1+breakfactor)
                if all[t][2] > line:
                    short = False
                    long = False
                    cash += self.trade_short(short_start_price, line)
                    short_start_price = 0.
                    trade_back += 1
                    amount[t][5] = 50

                    if all[t][4] > buy_price:  # close > buy
                        long = True
                        short = False
                        long_start_price = all[t][4] + slide
                        amount[t][5] = 58
                        long_times += 1

                    elif all[t][4] < sell_price:
                        short = True
                        long = False
                        short_start_price = all[t][4] - slide
                        amount[t][5] = 55
                        short_times += 1

                    # long starts
                elif all[t][4] > buy_price:
                #     # high > buy
                    short = False
                    long = True
                    long_start_price = all[t][4] + slide
                    cash += self.trade_short(short_start_price, all[t][4])
                    amount[t][5] = 88

            elif not short and long:
                line = sell_price + (buy_price - sell_price) / 2
                if all[t][3] < line:
                    long = False
                    short = False
                    cash += self.trade_long(long_start_price, line)
                    long_start_price = 0.
                    trade_back += 1
                    amount[t][5] = 80

                    if all[t][4] > buy_price:  # close > buy
                        long = True
                        short = False
                        long_start_price = all[t][4] + slide
                        amount[t][5] = 88
                        long_times += 1

                    elif all[t][4] < sell_price:
                        short = True
                        long = False
                        short_start_price = all[t][4] - slide
                        amount[t][5] = 85
                        short_times += 1

                elif all[t][4] < sell_price:
                        #     # high > buy
                    short = True
                    long = False
                    short_start_price = all[t][4] - slide
                    cash += self.trade_long(long_start_price, all[t][4])
                    amount[t][5] = 55


            #result log

            value = cash


            amount[t][0] = buy_price
            amount[t][1] = sell_price
            amount[t][2] = cash
            amount[t][3] = btc
            amount[t][4] = value
            print("value: %s" % value)

        all = np.c_[
            time_stamp, open_price, high_price, low_price, close_price, long_price,short_price, amount]

        data = pd.DataFrame(all,
                            columns={"1", "2", "3", "4", "5", "6", "7", "8", "9", "10","11","12","13", "14"})

        print("============================")
        print(long_times)
        print(short_times)

        cwd = os.getcwd()
        data.to_csv(
            cwd + "_jpy.csv",
            index=True)

        print("trade_back= %s "  %trade_back)

        return value, trade_back



if __name__ == '__main__':
    # directly

    btc_charts = historical_fx.charts()

    (time_stamp, open_price, high_price, low_price, close_price) = btc_charts.get_price_array_till_finaltime()

    # print(close_price)

    # gmma = GMMA()
    # # simulate the past 24 hours
    # gmma.simulate(num=24 * 7 * 1 + 61, periods="1H", end_offset=3600 * 24 * 7 * 0)

    hilo = HILO()

    #er = hilo.calcalate_er()
    # simulate the past 24 hours
    # hilo.simulate(num=24 * 7 * 1 + 20, periods="1H", end_offset=3600 * 24 * 7 * 0)


    # sum = 0.
    # counter_sum= 0
    # length = 3
    # for i in range(length):
    #     value,counter = gmma.simulate(num=24 * 30 * 1 + 61, periods="1H", end_offset=3600 * 24 * 30 * (i+3))
    #     sum = sum + value
    #     counter_sum = counter_sum+counter
    # # gmma.simulate(num=60*24*50+61, periods="1m", end_offset=0)
    # # a=gmma.publish_current_limit_price(periods="1H")
    #
    # print(sum / length)
    # print(counter_sum / length)

    sum = 0.
    counter_sum= 0
    length = 1
    for i in range(0,length):
        #value,counter = hilo.simulate(num=24 * 7 * 4 + 50, periods="1H", end_offset=3600 * 24 * 7 * (i+0))
        value, counter = hilo.simulate(num=24 * 7 * 12 + 50, periods="1H", end_offset=0)
        sum = sum + value
        counter_sum = counter_sum+counter
    # hilo.simulate(num=60*24*50+61, periods="1m", end_offset=0)
    # a=hilo.publish_current_limit_price(periods="1H")

    print('mouth ave: %f'%( sum / length))
    print(counter_sum / length)

    #hilo.publish_current_hilo_price()
