from tradingapis.bitflyer_api import pybitflyer
import keysecret as ks
import time
import predict
import configIO
import sys
import technical_fx_bidirc

from email.mime.text import MIMEText
from email.utils import formatdate
import smtplib

# stop version

class AutoTrading:
    currency_jpy = 0 # jpy btc
    currency_btc = 0
    holdflag = False
    order_places = {
            'exist': False,
            'type': '',
            'id': '',
            'remain' : 0.0,
            'trade_price' : '',
            'slide': 0.0
        }
    tradeamount = 10000
    position = 0
    wave_times = 0
    everhold = False
    real_position = 0.0


    def __init__(self, holdflag = False, order_places = {'exist': False, 'type': '','id': 0,'remain' : 0.0, 'trade_price' : '', 'slide': 0.0}, tradeamount = 1000, position = 0.0):
        print("Initializing API")
        self.bitflyer_api = pybitflyer.API(api_key=str(ks.bitflyer_api), api_secret=str(ks.bitflyer_secret))
        self.holdflag = holdflag # if hold bitcoin
        self.order_places = order_places # specific an exist order
        self.tradeamount = tradeamount # init trade amount only if order not exist
        self.position = position # remain position (btc)
        self.initeverhold()

    def initeverhold(self):
        if self.holdflag == True:
            self.everhold = True
        else:
            self.everhold = False




    def trade_bitflyer_constoplimit(self, type, buysellprice, insurance_price,  amount, slide = 100):
        while 1:
            cur_oclock = int(time.strftime('%H:')[0:-1])
            cur_min = int(time.strftime('%M:')[0:-1])
            if (cur_oclock == 4 and cur_min >= 0 and cur_min <= 11) or (cur_oclock == 3 and cur_min >= 59):
                predict.print_and_write('Server maintenance')
                time.sleep(60)
                continue
            else:
                break

        product= 'FX_BTC_JPY'
        print('trade bitflyer')
        expire_time = 75
        if type == 'BUY' or type == 'buy':
            # order = self.quoinex_api.create_market_buy(product_id=5, quantity=str(amount), price_range=str(buysellprice))
            parameters =  [{'product_code': product, 'condition_type': 'STOP', 'side': 'BUY', 'size': str(amount),
                            'trigger_price': str(buysellprice)}]
            order = self.bitflyer_api.sendparentorder(order_method='SIMPLE', minute_to_expire=expire_time, parameters=parameters)
        elif type == "SELL" or type == "sell":
            parameters = [{'product_code': product, 'condition_type': 'STOP', 'side': 'SELL', 'size': str(amount),
                           'trigger_price': str(buysellprice)}]
            order = self.bitflyer_api.sendparentorder(order_method='SIMPLE', minute_to_expire=expire_time, parameters=parameters)
        else:
            print("error!")
        return (order)





    def get_orders(self, status = ''):
        #order = self.quoinex_api.get_orders()
        #order = self.quoinex_api.get_orders(status, limit)
        #ACTIVE CANCELED
        product = 'FX_BTC_JPY'
        if status != '':
            order = self.bitflyer_api.getparentorders(product_code=product, parent_order_state=status)
        else:
            order = self.bitflyer_api.getparentorders(product_code=product, count=30)
        return (order)

    def get_orderbyid(self, id):
        product = 'FX_BTC_JPY'
        i = 20
        while i > 0:
            try:
            #order = self.bitflyer_api.getparentorder(product_code=product, parent_order_acceptance_id=id)
                orders = self.get_orders()
                for i in orders:
                    if i['parent_order_acceptance_id'] == id:
                        return (i)
                print('order not find')
                return({})
            except Exception:
                print('Server is fucked off ,try again')
                time.sleep(20)
                i -= 1
                continue
        print('Try too many times, failed')
        return({})

    def handel_partly_deal(self, order):
        # if order is partly dealed, the state should be 'COMPLETED' however executed size is not full size.
        if order['parent_order_state'] == 'COMPLETED' and order['executed_size'] != order['size']:
            if self.order_places['remain'] - order['executed_size'] >= 0.001:
                order['executed_size'] = self.order_places['remain']
        return(order)

    def cancle_order(self, id):
        product = 'FX_BTC_JPY'
        i = 20
        while i>0:
            try:
                statue = self.bitflyer_api.cancelparentorder(product_code=product, parent_order_acceptance_id=id)
                time.sleep(10)
                order = self.get_orderbyid(id)
                if order['parent_order_state'] == 'COMPLETED':
                    predict.print_and_write('Order completed')
                    return (0.0)

                if order['parent_order_state'] == 'CANCELED':
                    predict.print_and_write('Order cancelled')
                    if order['parent_order_type'] == 'OCO':
                        real_executed_size = abs(self.position)
                        if real_executed_size > self.order_places['remain']:
                            predict.print_and_write('maybe double executed')
                            predict.print_and_write('real: %f, executed: %f, pre_remain: %f'%(real_executed_size, order['executed_size'], self.order_places['remain']))
                        remain_amount = float(order['cancel_size']) - self.order_places['remain']
                    else:
                        remain_amount = float(order['cancel_size'])
                    return(remain_amount)
                else:
                    i -= 1
                    print('Try again cancelling')
                    continue
            except Exception:
                order = self.get_orderbyid(id)
                if order['parent_order_state'] == 'COMPLETED':
                    print('Executed before cancelling')
                    return(0.0)
                time.sleep(5)
                print('Exception Try again cancelling')
                i -= 1
        predict.print_and_write('Cancel order failed')
        self.sendamail('Cancel order failed','cancel failed : id %s'%(id))
        return([])



    def onTrick_trade(self, buyprice, sellprice, buyi, selli, slide = 200):

        buyprice = float(buyprice)
        sellprice = float(sellprice)

        if self.order_places['exist']: # There is an order existed in last time
            placed = self.get_orderbyid(self.order_places['id'])
            placed = self.handel_partly_deal(placed)
            if placed['executed_size'] > self.order_places['remain']:
                predict.print_and_write('Maybe double dealed, size %f'%(placed['executed_size'] - self.order_places['remain']))
                return (-1)

            # detecting the order and get the information of this order
            if self.order_places['type'] == 'buy':
                self.position += placed['executed_size']
                #self.tradeamount -= placed['executed_size'] * self.order_places['trade_price']
                self.tradeamount -= placed['executed_size'] * self.order_places['trade_price']
            elif self.order_places['type'] == 'sell':
                self.position -= placed['executed_size']
                #self.tradeamount += placed['executed_size'] * self.order_places['trade_price']
                self.tradeamount += placed['executed_size'] * self.order_places['trade_price']

            predict.print_and_write(
                'buy amount : %.2f sell amount : %.2f' % (self.position, self.tradeamount / buyprice))

            if self.order_places['remain'] - placed['executed_size'] < 0.01  : # if filled
                if self.order_places['type'] == 'buy': # if buy filled sell double
                    predict.print_and_write('Buy order filled')
                    self.holdflag = True
                    self.everhold = True
                    amount = self.position + self.position
                else:
                    predict.print_and_write('Sell order filled')
                    self.holdflag = False
                    amount = self.tradeamount / buyprice

                self.order_places['exist'] = False
                self.order_places['id'] = 0
                self.order_places['remain'] = .0

            else: # not filled or partly filled
                self.order_places['remain'] = self.cancle_order(self.order_places['id'])
                #self.checkposition(placed)
                time.sleep(20)
                pflag = self.checkP()
                if abs(pflag - self.position) > 0.001: # if position is unusuall
                    predict.print_and_write('Position is unsuall')
                    return(-1)
                # if a order is cancelled, but some trading happened between
                # detection and cancelling, the result may cause bug
                # it is necessary to check the cancel result and detection result and fix them
                self.order_places['exist'] = False
                self.order_places['id'] = 0
                predict.print_and_write('remain:%f'%(self.order_places['remain']))

                if self.order_places['remain'] < 0.01: # if filled
                    if self.order_places['type'] == 'buy':
                        predict.print_and_write('Buy order filled')
                        self.holdflag = True
                        self.everhold = True
                        amount = self.position + self.position
                    else:
                        predict.print_and_write('Sell order filled')
                        self.holdflag = False
                        amount = self.tradeamount / buyprice

                else: # not filled
                    if self.order_places['type'] == 'buy': #
                        predict.print_and_write('Buy order not filled buy again')
                        self.holdflag = False
                        amount = self.tradeamount / buyprice # continue buy
                        if amount < 0.01:
                            amount = 0.01
                        #
                    else: # treat as sell succeed
                        predict.print_and_write('Sell order not filled sell again')
                        self.holdflag = True
                        self.everhold = True
                        amount = self.order_places['remain'] # continue sell
                        if amount < 0.01:
                            amount = 0.01

                # maybe bug here cancelled but actually executed

        else:
            if self.holdflag:
                amount = self.tradeamount / sellprice
            else:
                amount = self.tradeamount / buyprice

        if self.holdflag:
            side = 'sell'
        else:
            side = 'buy'

        amount = float(str('%.2f'%amount))
        if amount < 0.01:
            print('less than min amount')
            return(-1) # less than min amount stop trading

        try_times = 20
        while try_times > 0:
            try:
                if side == 'sell':
                    new_order = self.trade_bitflyer_constoplimit(side, sellprice , selli, amount)
                    self.order_places['trade_price'] = sellprice
                    predict.print_and_write('Order placed sell %f @ %f'%(amount, sellprice))
                else:
                    new_order = self.trade_bitflyer_constoplimit(side, buyprice , buyi, amount)
                    self.order_places['trade_price'] = buyprice
                    predict.print_and_write('Order placed buy %f @ %f' % (amount, buyprice))
                self.order_places['exist'] = True
                self.order_places['id'] = new_order['parent_order_acceptance_id']
                self.order_places['remain'] = amount
                self.order_places['type'] = side
                self.order_places['slide'] = slide

                predict.print_and_write('order: id %s, amount: %s, type: %s, price: %s'%(new_order['parent_order_acceptance_id'], str(amount), side, str(self.order_places['trade_price'])) )
                self.wave_times += 1
                return(self.order_places['id'])
            except Exception:
                print('Error! Try again')
                predict.print_and_write(new_order)
                time.sleep(5)
                try_times -= 1
        return(-2) # try too many times stop trading

    # check position of market
    def checkP(self):
        p = self.bitflyer_api.getpositions(product_code = 'FX_BTC_JPY')
        position0 = 0.0
        if isinstance(p, list):
            for i in p:
                predict.print_and_write('check in price: %f'%(i['price']))
                if i['side'] == 'SELL':
                    position0 -= i['size']
                else:
                    position0 += i['size']
            if abs(position0 - self.position) < 0.001:
                predict.print_and_write('Real position is same as program one')
                return(position0)
        if isinstance(p, dict) or len(p) == 0:
            if abs(self.position) < 0.01:
                predict.print_and_write('Position not exist')
                return (position0)
        predict.print_and_write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        str = 'position :%f, program: %f'%(position0,self.position)
        predict.print_and_write(str)
        #self.sendamail('position check failed', str)
        self.real_position = position0
        predict.print_and_write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        return(position0)

    # check position of market and program


    def get_profit(self):
        balances = self.bitflyer_api.getbalance(product_code="FX_BTC_JPY")
        jpy_avai = 0.0
        btc_avai = 0.0
        for balance in balances:
            if balance['currency_code'] == 'JPY':
                jpy_avai = float(balance['available'])
            elif balance['currency_code'] == 'BTC':
                btc_avai = float(balance['available'])
        return ([jpy_avai, btc_avai])

    def get_collateral(self):
        balances = self.bitflyer_api.getcollateral()
        collateral = balances['collateral']
        openpnl = balances['open_position_pnl']
        return([collateral,openpnl])

    def sendamail(self, title ,str):
        address = 'goozzfgle@gmail.com'  # change the reciver e-mail address to yours
        username = 'goozzfgle@gmail.com'
        paswd = 'googlebaidu'

        mail_str = '%s %s' % (str, formatdate(None, True, None))
        sender = SendMail(address, username, paswd)
        msg = MIMEText(mail_str)
        msg['Subject'] = title
        msg['From'] = username
        msg['To'] = address
        msg['Date'] = formatdate()
        sender.send_email(address, msg.as_string())

    def decide_hilo(self, hi, lo, close_previous):
        # return the hilo line
        if close_previous < lo:
            return('hi')
        elif close_previous > hi:
            return('lo')
        else:
            return('pr')


    def isset(self, v):
        try:
            type(eval(v))
        except:
            return 0
        else:
            return 1

    # function for first trade, should decide the line for next hour
    # def trade_first_time(self):
    #     tradeamount0 = 20000
    #     hilos = technical_fx_bidirc.HILO()
    #     result = hilos.publish_current_hilo_price()
    #     sell = float(result[1])
    #     buy = float(result[0])
    #     #close = float(result[2])
    #
    #     buyi = buy + 1000
    #     selli = sell - 1000
    #     oid = self.onTrick_trade(buy, sell, buyi, selli, slide=300)  # trade first time
    #     return(oid)
    #
    #
    # def trade_normal_time(self, hiloline):
    #
    #     buy = hiloline
    #     sell = hiloline
    #     oid = self.onTrick_trade(buy, sell, buyi, selli, slide=300)


if __name__ == '__main__':
    tradeamount0 = 10000
    waiting_time = 10
    detect_fre = 0 # detection frequency
    succeed = 0 # succeed times
    failed = 0 # failed times
    wait = 0 # waiting times
    argvs = sys.argv
    argc = len(argvs)
    cofile = 'orders.ini'
    times = 3


    order_places = {'exist' : False,'type' : '','id' : '','remain' : 0.0, 'trade_price' : 0.0, 'slide': 200.0}
    tradeamount0 = 10000
    position = 0.00
    holdflag = False


    if argc >= 2:
        cofile = sys.argv[1]
        cf = configIO.configIO(config_file=cofile)
        parameters = cf.read_config_order()
        order_places = {'exist': parameters['exist'], 'type': parameters['type'], 'id': parameters['id'],
                        'remain':parameters['remain'], 'trade_price': parameters['trade_price'], 'slide':parameters['slide']}
        tradeamount0 = parameters['tradeamount']
        position = parameters['position']
        holdflag = parameters['holdflag']
    else:
        cf = configIO.configIO(config_file=cofile)


        # if sell order exist tradeamount should be
    autoTrading = AutoTrading(holdflag=holdflag, order_places=order_places, tradeamount=tradeamount0, position=position)
    prediction = predict.Predict()


    hilos = technical_fx_bidirc.HILO()
    collateral = autoTrading.get_collateral()
    predict.print_and_write('Collateral: %f Profit: %f ' % (collateral[0], collateral[1]))
    tradingtimes = 0
    if holdflag == False:
        curthis = 'hi'
    else:
        curthis = 'lo'

    while 1:
        this_maintance_time = 0
        if tradingtimes > 0: # get the buy and sell price of last hour
            sell0 = sell
            buy0 = buy
            order0 = autoTrading.order_places['trade_price']
            position0 = autoTrading.position
            tradeamount0 = autoTrading.tradeamount
            everholdflag = autoTrading.everhold
            holdflag0 = autoTrading.holdflag
        result = hilos.publish_current_hilo_price()

        #result = prediction.publish_current_limit_price(periods="1H")
        selli = float(result[1])
        buyi = float(result[0])
        close = float(result[2])  # the close price of last hour

        # no else just for test do not consider first time
        hiloline = autoTrading.decide_hilo(buyi, selli, close)
        if hiloline == 'hi':
            thisline = buyi
            curthis = 'hi'
        elif hiloline == 'lo':
            thisline = selli
            curthis = 'lo'
        elif hiloline == 'pr':
            if curthis == 'hi':
                thisline = buyi
            else:
                thisline = selli

        sell = float('%.0f' % (thisline+1800))
        buy = float('%.0f' % (thisline-1800))
        predict.print_and_write('sell: %.0f , buy : %.0f , %s' % (selli, buyi, curthis))
        autoTrading.initeverhold()  # initinal the ever hold flag before each iteration
        previousline = hiloline
        buys = buy + 2000
        sells = sell - 2000


        oid = autoTrading.onTrick_trade(buy, sell, buys, sells, slide=300)  # trade first time
        if oid == -1 or oid == -2:
            print('oid : %d'%oid)
            break
        tempcf = dict()
        tempcf['order'] = {'exist': autoTrading.order_places['exist'],
                            'type': autoTrading.order_places['type'],
                            'id': autoTrading.order_places['id'],
                            'remain': autoTrading.order_places['remain'],
                            'trade_price': autoTrading.order_places['trade_price'],
                            'slide': autoTrading.order_places['slide'],
                            'tradeamount': autoTrading.tradeamount,
                            'position': autoTrading.position,
                            'holdflag': autoTrading.holdflag,
                            'timestamp': time.strftime('%b-%d/%H:%M:%S')}
        result = cf.save_config_order(tempcf)
        time.sleep(waiting_time)
        collateral = autoTrading.get_collateral()


        # record following thing of last 2 hour:
        # close price, buy price, sell price, btc remain, jpy remain
        if tradingtimes > 0:
             if holdflag0 :
                 predict.print_and_write('Hold: close: %f, trade: %f, buy: %f sell: %f BTC: %f, JPY %f'%(close, order0, buy0, sell0, position0, tradeamount0))
             elif holdflag0==False :
                 predict.print_and_write('Not hold: close: %f, trade: %f, buy: %f sell: %f BTC: %f, JPY %f' % (close, order0, buy0, sell0, position0, tradeamount0))
             if everholdflag:
                 if close >= sell0 and holdflag0:
                     succeed += 1
                     predict.print_and_write('succeed:%d'%succeed)
                 elif close <= sell0 and holdflag0 == False:
                     succeed += 1
                     predict.print_and_write('succeed:%d' % succeed)
                 else:
                     failed += 1
                     predict.print_and_write('failed:%d' % failed)
             else:
                 wait += 1
                 predict.print_and_write('wait:%d' % wait)

        predict.print_and_write('Collateral: %f Profit: %f '%(collateral[0], collateral[1]))
        #predict.print_and_write('Trading jpy: %s btc: %s' % (str(autoTrading.tradeamount), str(autoTrading.position)))
        #predict.print_and_write('All jpy: %s btc: %s' % (str(float(cur_jpy)+ autoTrading.tradeamount), str(float(cur_btc) + autoTrading.position)))
        predict.print_and_write('==============================================')
        tradingtimes +=1
