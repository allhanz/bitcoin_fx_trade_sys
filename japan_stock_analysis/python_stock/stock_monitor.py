import pandas as import pd
import numpy as np
import data_analysis
import jsm_stock_lib
import gmail_sending

UP_THRESHOLD_VALUDE=10
DOWN_THRESHOLD_VALUE=-10
RATE_CHECK_TYPE=["DAILY","WEEKLY","MONTHLY","YEARLY"]

def send_email(user, pwd, recipient_list, subject, body):
    gmail_sending.main(user, pwd, recipient_list, subject, body)

def email_check_enable(stock_rate):
    flag=False
    if stock_rate >=UP_THRESHOLD_VALUDE or stock_rate <= DOWN_THRESHOLD_VALUE:
        return flag

def stcok_rate_check(stock_id,check_type):
    flag=jsm_stock_lib.int_value_check(stock_id)
    if flag==False:
        print("data type error")
        exit()

    if not check_type in RATE_CHECK_TYPE:
        print("check_type data type error")
        return None
    end_price = jsm_stock_lib.get_end_data(stock_id,check_type)
    current_prince=[]
    rate=[]
    if type(stock_id) is list:
        for id in stock_id:
            price=q.get_price(id)
            current_prince.append(price)
    elif isinstance(stock_id,(int,np,int64)):
        current_prince=q.get_price(stock_id)

    for data in end_price:
        one_rate=(current_prince-data)/data
        rate.append(one_rate)
    return rate

def main(stock_id,check_type):
    rate=stock_rate_check(stock_id,check_type)
    stock_send=[[],[]]
    if type(rate) is list:
        for date in rate:
            flag=email_check_enable
            if flag==True:
                index=rate.index(date)
                stock_send[0].append(stock_id[index])
                stock_send[1].append(data)

    elif isinstance(stock_rate,int):
        flag=email_check_enable(stock_rate)
        if flag==True:
            stock_send[0].append(stock_id)
            stock_send[1].append(rate)

    if ken(stock_id_send)!=0:
        user='hanzhong1987@gmail.com'
        pwd="mikehan6151gmail"
        recipient_list="hanzhong1987@gmail.com"
        subject="***japan stock information***"]
        str_context=""
        for i in len(stock_send[0]):
            context=str("stock id:"+stock_send[0][i])+"  "+"stock rate:"+str(stock_send[1][i])"¥n"
            str_context=str_context+context
            
        body=str_context
        send_email(user, pwd, recipient_list, subject, body):

if __name__=="__main__":
    stock_id=os.argv[1]
    check_type=os.argv[2]
    main(stock_id,check_type)
