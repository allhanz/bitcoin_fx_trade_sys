import os
import sys
sys.path.append(os.path.abspath("../"))
import pandas as pd
import random
from datetime import datetime


class account_info:
    def __init__(self):
        self.name="test_user"
        self.status="init"
        self.init_blac=300000
        self.balance=300000 #jpy
        self.all_rate=0 #profit rate
        self.threthhold_val=0.5
        self.trade_count=0
        self.trade_his_info=[]
        self.tarde_unit=0.1 # 0.1 bitcoin
        self.coin_no=0
        self.current_price=None
        self.trade_factor=10 # depend on the model
        self.trade_item={
            "buy_or_sell":None,
            "time":None,
            "price":None,
            "price_vol":None,
            "trade_unit":None
        }
        self.trade_model=None

    def check_account_balance(self,trade_unit,buy_unit_price):
        all_price=trade_unit*buy_unit_price
        nokori=self.balance-all_price
        if nokori>=0:
            return True
        else:
            return False

    def buy(self,trade_unit):
        if self.trade_noise_sim():
            price_vol=trade_unit*self.current_price
            if self.check_account_balance(trade_unit,self.current_price):
                self.balance=self.balance-price_vol
                self.coin_no=self.coin_no-trade_unit
                self.all_rate=(self.coin_no*self.current_price-self.init_blac)/self.init_blac
                trade_item=self.trade_item
                trade_item["buy_or_sell"]="buy"
                trade_item["time"]=datetime.now().strftime("%Y%m%dT%H%M%S")
                trade_item["price"]=self.current_price
                trade_item["price_vol"]=price_vol
                trade_item["trade_unit"]=trade_unit
                self.trade_his_info.append(trade_item)
                self.trade_count=self.trade_count+1
            
        else:
            print("cannot trading......")
    
    def sell(self,trade_unit):
        if self.trade_noise_sim():

            #previous_blance=self.balance
            price_vol=trade_unit*self.current_price
            self.balance=self.balance+price_vol
            self.coin_no=self.coin_no+trade_unit
            self.all_rate=(self.coin_no*self.current_price-self.init_blac)/self.init_blac
            trade_item=self.trade_item
            trade_item["buy_or_sell"]="sell"
            trade_item["time"]=datetime.now().strftime("%Y%m%dT%H%M%S")
            trade_item["price"]=self.current_price
            trade_item["price_vol"]=price_vol
            trade_item["trade_unit"]=trade_unit
            self.trade_his_info.append(trade_item)
            
            self.trade_count=self.trade_count+1
        else:
            print("cannot trading......")

    def trade_principle(self,signal_rate):
        #signal_rate :-1.00~1.00
        trade_unit=self.trade_factor*signal_rate
        if trade_unit>2:
            self.buy(trade_unit)
        elif trade_unit<-2:
            self.sell(-trade_unit)
        else:
            print("hold........")

    def trade_noise_sim(self):
        random_val=random.uniform(-1,1)
        if random_val>0:
            return True
        else:
            return False



def main():
    pass

if __name__=="__main__":
    main()