from gmail_sending import *
import pandas as pd
import numpy as np
import os
import sys
from japan_stock_id_divided import *
import time
from datetime import timedelta,datetime
from jsm_stock_lib import *

CHECK_TYPE=["DAILY","WEEKLY","MONTHLY","THREE_MONTHLY","YEARLY"]
YEARLY_UP_THOLD_VALUE=0.5
YEARLY_DOWN_THOLD_VALUE=-0.5

THREE_MONTHLY_UP_THOLD_VALUE=0.4
THREE_MONTHLY_DOWN_THOLD_VALUE=-0.4

MONTHLY_UP_THOLD_VALUE=0.3
MONTHLY_DOWN_THOLD_VALUE=-0.3

WEEKLY_UP_THOLD_VALUE=0.2
WEEKLY_DOWN_THOLD_VALUE=-0.2

DAILY_UP_THOLD_VALUE=0.1
DAILY_DOWN_THOLD_VALUE=-0.1

def get_past_workday(check_time,days_num):
    past_day=check_time - timedelta(days=days_num)
    week_num=past_day.weekday()
    if week_num==5:
        past_day=past_day - timedelta(days=1)
    if week_num==6:
        past_day=past_day - timedelta(days=2)

    return past_day

def stock_info_list(stock_dataframe,label):
    stock_info_list=np.array(stock_dataframe[label])
    return stock_info_list

def remove_error_id(stock_dataframe):
    print(error_stock_id)
    for error_id in error_stock_id:
        stock_dataframe.drop(stock_dataframe["SC"]==error_id)
    print(len(stock_dataframe["SC"]))
    return stock_dataframe

def rate_check(stock_dataframe,check_time,check_type): # now just for dialy rate check
    #up_rate_info={"stock_id":[],"stock_name":[]}
    if check_type=="DAILY":
        subject="weekly rate check"
        UP_THOLD_VALUE=DAILY_UP_THOLD_VALUE
        DOWN_THOLD_VALUE=DAILY_DOWN_THOLD_VALUE

    if check_type=="WEEKLY": # cannot monitorinhg becauseof only monthly stock price download
        subject="weekly rate check"
        UP_THOLD_VALUE=WEEKLY_UP_THOLD_VALUE
        DOWN_THOLD_VALUE=WEEKLY_DOWN_THOLD_VALUE

    if check_type=="MONTHLY":
        subject="monthly rate check"
        UP_THOLD_VALUE=MONTHLY_UP_THOLD_VALUE
        DOWN_THOLD_VALUE=MONTHLY_DOWN_THOLD_VALUE

    if check_type=="THREE_MONTHLY":
        subject="three monthly rate check"
        UP_THOLD_VALUE=THREE_MONTHLY_UP_THOLD_VALUE
        DOWN_THOLD_VALUE=THREE_MONTHLY_DOWN_THOLD_VALUE

    if check_type=="YEARLY":
        subject="yearly rate check"
        UP_THOLD_VALUE=YEARLY_UP_THOLD_VALUE
        DOWN_THOLD_VALUE=YEARLY_DOWN_THOLD_VALUE

    rate_info=pd.DataFrame(columns=["check_time","stock_id","stock_name","rate","open_price","current_price"])
    check_time=[]
    stock_id=[]
    stock_name=[]
    rate=[]
    open_price=[]
    current_price=[]

    stock_id_list=stock_info_list(stock_dataframe,"SC")

    stock_name_list=stock_info_list(stock_dataframe,"名称")

    for stock_id in stock_id_list:
        current_price=get_current_price(stock_id)
        open_price=get_open_price(stock_id)
        rate=(open_price - current_price)/open_price
        print(rate)

        if rate >= UP_THOLD_VALUE or rate < DOWN_THOLD_VALUE:
            index_value=stock_id_list.index(stock_id)
            check_time.append(check_time)
            stock_id.append(stock_id)
            stock_name.append(stock_name_list[index_value])
            rate.append(rate)
            open_price.append(open_price)
            current_price.append(current_price)

            rate_info["check_time"]=check_time
            rate_info["stock_id"]=stock_id
            rate_info["stock_name"]=stock_name
            rate_info["rate"]=rate
            rate_info["open_price"]=open_price
            rate_info["current_price"]=current_price
            print("check_time:",check_time)
            print("stock_id:",stock_id)
            print("rate:",rate)
            print("open_price:",open_price)
            print("current_price(or close price):",current_price)
            contents=str(rate_info)
            send_stock_rate_email(subject,contents)

    return rate_info

def send_stock_rate_email(subject,contents):
    user='hanzhong1987@gmail.com'
    pwd="mikehan6151gmail"
    recipient_list=["hanzhong1987@gmail.com","hanzhong1987@ezweb.ne.jp"]
    subject=subject
    body=contents
    send_email(user, pwd, recipient_list, subject, body)

def get_current_time():
    current_date=time.localtime()
    time_list={"hour":"","min":"","sec":""}
    str_time_hr=time.strftime("%H",current_date)
    str_time_min=time.strftime("%M",current_date)
    str_time_sec=time.strftime("%S",current_date)
    time_list["hour"]=str_time_hr
    time_list["min"]=str_time_min
    time_list["sec"]=str_time_sec
    return time_list

def get_current_weekday():
    d=datetime.today()
    weekday_num=d.weekday()
    return weekday_num
    # 0 means monday
    # ....
    # 5 means saturday
    # 6 means sunday

def daily_monitor(stock_dataframe):
    weekday=get_current_weekday()
    #print(weekday)
    now_date=datetime.now().date()
    #now_date=datetime(2017,1,19)
    #weekday=3 # for test
    if weekday != 6 or weekday !=5:
        current_time=get_current_time()
        hour_num=int(current_time["hour"])
        #hour_num=10 # for test
        print(hour_num)
        hour_num=10 # for test
        if hour_num>=9 and hour_num<=15:
            daily_rate_info=rate_check(stock_dataframe,now_date,"DAILY")
            #weekly_rate_info=rate_check(stock_dataframe,now_date,"WEEKLY")
            #monthly_rate_info=rate_check(stock_dataframe,now_date,"MONTHLY")
            #three_month_rate_info=rate_check(stock_dataframe,now_date,"THREE_MONTHLY")
            #yearly_rate_info=rate_check(stock_dataframe.now_date,"YEARLY")
            print("monitoring.....")

        else:
            print("out of time....")
            
            #time.sleep(10)
            #return 0

    else:
        print("today is sunday or saturday!!")
        return 0

def main_monitor_loop():
    #flag=daily_monitor()
    #if flag==False:
    #    print("keyboard pressed and exit!")
    type1="nikkei225"
    type2="toho1"
    type3="toho2"
    type4="tohomum"
<<<<<<< HEAD
    type=type2
    stock_dataframe=read_stock_id(type)

=======
    stock_dataframe=read_stock_id(type2)
    stock_dataframe_ok=remove_error_id(stock_dataframe)
    list=stock_info_list(stock_dataframe_ok,"SC")
    print(len(list))
    exit()
>>>>>>> cc232fdbd7e5d0bfc13a46d06c7c87eb04e78fcf
    try:
        while True:
            flag=daily_monitor(stock_dataframe_ok)
            if flag==0:
                return

    except KeyboardInterrupt:
        print("exit the daily monitoring.....")
        pass

def main():
    main_monitor_loop()

if __name__=="__main__":
    main()
