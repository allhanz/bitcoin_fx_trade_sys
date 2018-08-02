import jsm
from  datetime import datetime
import numpy as np

q = jsm.Quotes()
c = jsm.QuotesCsv()
TIME_TYPE={"DAILY":jsm.DAILY,"WEEKLY":jsm.WEEKLY,"MONTHLY":jsm.MONTHLY}

def jsm_type_check(time_type):
    if TIME_TYPE[time_type]:
        return TIME_TYPE[time_type]
    else:
        return jsm.DAILY

def int_value_check(stock_id):
    #print(type(stock_id))
    if type(stock_id) is list:
        #flag=all(isinstance(id, int) for id in stock_id)
        for data in stock_id:
            flag=isinstance(data,(int,np.int64))
            #print(type(data))
            #print(flag)
            #exit()
            if flag==False:
                index=stock_id.index(data)
                print(str(data))
                print("index value:"+str(index))
        print("0")
    else:
        flag=isinstance(stock_id,(int,np.int64))
        #print("1")
    #print(flag)
    return flag

def get_current_price(stock_id):
    if not int_value_check(stock_id):
        return None

    price = q.get_price(stock_id)
    return price.close

def get_monthly_price(stock_id,date):
    if not int_value_check(stock_id):
        return None

    start_date=date
    print("the start time:"+date)
    price = q.get_historical_prices(stock_id)
    return price

def get_open_price(stock_id):
    if not int_value_check(stock_id):
        return None

    return q.get_price(stock_id).open

def get_close_price(stock_id):
    if not int_value_check(stock_id):
        return None

    return q.get_price(stock_id).close

def get_high_price(stock_id):
    if not int_value_check(stock_id):
        return None

    return q.get_price(stock_id).high

def get_low_price(stock_id):
    if not int_value_check(stock_id):
        return None

    return q.get_price(stock_id).low

def get_daily_volume(stock_id):
    if not int_value_check(stock_id):
        return None

    return q.get_price(stock_id).volume

def get_monthly_volume(stock_id):
    if not int_value_check(stock_id):
        return None

    price = q.get_historical_prices(stock_id)
    sum=0
    for data in price:
        sum= sum+data.volume
    return sum

def get_period_volume(stock_id,start_date,end_date):
    if not int_value_check(stock_id):
        return None

    price = q.get_historical_prices(stock_id,start_date,end_date)
    sum=0
    for data in price:
        sum= sum+data.volume
    return sum

def get_end_price(stock_id,time_type):
    if time_type in TIME_TYPE:
        jsm_type="jsm."+time_type
    else:
        print("time_type data type error")
        exit()
    price=[]
    end_price=[]
    data_type=data_type_check(stock_id)
    if data_type is list:
        if time_type=="DAILY":
            for id in stock_id:
                get_price=q.get_price(id).open
                price.append(get_price)
        else:
            for id in stock_id:
                price=q.get_historical_prices(id,jsm_type)
                price.append(get_price)

    elif isinstance(data_type,(int,np.int64)):
        if time_type=="DAILY":
            price.append(q.get_price(stock_id).open)
        else:
            price.append(q.get_historical_prices(stock_id,jsm_type))

    if type(price) is list:
        end_price = price[len(price)-1]
    elif isinstance(price,(int,np.int64)):
        end_price=price
    return end_price

def get_whole_daily_data(stock_id):
    stock_id=list(stock_id)
    if not int_value_check(stock_id):
        return None

    if type(stock_id) is list:
        for id in stock_id:
            price = q.get_historical_prices(id,jsm.DAILY,all=True)
    else:
        price = q.get_historical_prices(stock_id,jsm.DAILY,all=True)
    return price

def get_whole_monthly_data(stock_id):
    if not int_value_check(stock_id):
        return None

    if type(stock_id) is list:
        for id in stock_id:
            price = q.get_historical_prices(id,jsm.MONTHLY,all=True)
    else:
        price = q.get_historical_prices(stock_id,jsm.MONTHLY,all=True)
    return price

def get_whole_weekly_data(stock_id):
    if not int_value_check(stock_id):
        return None

    if type(stock_id) is list:
        for id in stock_id:
            price = q.get_historical_prices(id,jsm.WEEKLY,all=True)
    else:
        price = q.get_historical_prices(stock_id,jsm.WEEKLY,all=True)

    return price

def get_whole_yearly_data(stock_id):
    if not int_value_check(stock_id):
        return None

    if type(stock_id) is list:
        for id in stock_id:
            price = q.get_historical_prices(id,jsm.YEARLY,all=True)
    else:
        price = q.get_historical_prices(stock_id,jsm.YEARLY,all=True)
    return price

def get_stock_data(stock_id):
    if not int_value_check(stock_id):
        return None

    price = q.get_price(stock_id).date
    return price

def get_current_month_data(stock_id):
    if not int_value_check(stock_id):
        return None
    if type(stock_id) is list:
        for id in stock_id:
            price = q.get_historical_prices(id,jsm.DAILY)
    else:
        price = q.get_historical_prices(stock_id,jsm.DAILY)
    return price

def data_type_check(data):
    return type(data)

# not tested monthly historical price data
def get_period_price(stock_id,start_time,end_time):
    if type(stock_id) is list:
        for id in stock_id:
            price=q.get_period_price(id,start_time,end_time)
    else:
        price=q.get_period_price(stock_id,start_time,end_time)

    return price

def save_whole_data(stock_id_list,file_path_list):
    for id in stock_id_list:
        index_value=stock_id_list.index(id)
        file_path=file_path_list[index_value]
        c.save_historical_prices(file_path,id,jsm.DAILY,all=True)

def main():
    print("not implemented!!")
