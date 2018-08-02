import pandas as pd
import read_csv_to_pandas

def caculate_rate(open_price,current_prince):
    rate=(current_price - open_price)/open_price *100
    return rate

def historical_rate(start_date,end_date,stock_object):
    rate_arrat=[]

    rate= caculate_rate(open_price,current_prince)

def daily_rate(open_price, current_prince):
    rate=caculate_rate(open_price, current_prince)
    return rate

def monthly_rate(open_price,current_prince):
    rate=caculate_rate(open_price,current_prince)
    return rate

def yearly_rate(open_price,current_prince):
    rate = caculate_rate(open_price,current_prince)
    return rate

def month_daily_rate(start_date,end_date,stock_object):
    print("not implemented!!")

def year_daily_rate(start):
    print("not implemented!!")
    
