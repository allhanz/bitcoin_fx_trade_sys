from tradingapis.bitflyer_api import pybitflyer
import keysecret as ks
import time
import datetime
import predict
import configIO
import sys
import technical_fx_hilo2
import technical_fx_turtle
import math
import configIO

class AutoTrading:

    switch_in_hour = False # if true, will be waiting for inhour position change
    order_id = ''
    init_trade_amount_buy = 0.1
    init_trade_amount_sell = 0.1
    auto_decide = True

    # for trail order
    max_profit = 0
    loss_cut_line = -100
    acc_factor = -0.02

    # position amount control
    total_margin = 50000
    least_collateral = 15000
    useable_margin = 35000
    level = 3
    max_loss = 0.025

    # panic index
    init_panic_index = 35
    panic = True


    def __init__(self):
        print("Initializing API")
        self.bitflyer_api = pybitflyer.API(api_key=str(ks.bitflyer_api), api_secret=str(ks.bitflyer_secret))


    def decide_trade_amount(self, curp ,losscut):
        safe_trade = 0.1
        if self.auto_decide:
            while curp == 0.0:
                predict.print_and_write('curp == 0 try again')
                curp = self.get_current_price(30)
            max_trade = round(self.useable_margin * self.level / curp, 2)
            safe_trade = round(self.useable_margin * self.max_loss / losscut, 2)
            predict.print_and_write('Amount control, Max trade: %.2f, safe trade: %.2f' % (max_trade, safe_trade))
            if safe_trade > max_trade:
                predict.print_and_write('Use smaller')
                safe_trade = max_trade
            self.init_trade_amount_buy = safe_trade
            self.init_trade_amount_sell = safe_trade


        if self.panic:
            buy_panic_weight = -0.025
            buy_panic_bias = 1.5
            sell_panic_weight = 0.025
            sell_panic_bias = -0.25

            panic_factor_buy = self.init_panic_index * buy_panic_weight + buy_panic_bias
            if panic_factor_buy > 1:
                panic_factor_buy = 1
            elif panic_factor_buy < 0.25:
                panic_factor_buy = 0.25
            panic_factor_sell = self.init_panic_index * sell_panic_weight + sell_panic_bias
            if panic_factor_sell > 1:
                panic_factor_sell = 1
            elif panic_factor_sell < 0.25:
                panic_factor_sell = 0.25

            self.init_trade_amount_buy = round(safe_trade * panic_factor_buy,2)
            if self.init_trade_amount_buy < 0.01:
                self.init_trade_amount_buy = 0.01
            self.init_trade_amount_sell = round(safe_trade * panic_factor_sell,2)
            if self.init_trade_amount_sell < 0.01:
                self.init_trade_amount_sell = 0.01
            predict.print_and_write('Use panic index: %.0f, buy amount %.2f, sell amount %.2f'%(self.init_panic_index, self.init_trade_amount_buy, self.init_trade_amount_sell))


    def trade_market(self, type, amount, wprice = 10000):
        self.maintance_time()

        product = 'FX_BTC_JPY'
        print('trade bitflyer')
        expire_time = 575
        try_t = 0
        while try_t < 20:
            if type == 'BUY' or type == 'buy':
                order = self.bitflyer_api.sendchildorder(product_code=product, child_order_type='MARKET',
                    side='BUY', size= str(amount))
                data2csv.data2csv(
                    [time.strftime('%b:%d:%H:%M'), 'order', 'BUY_MARKET', 'amount', '%f' % float(amount)])
                predict.print_and_write('Buy market ' +str(amount))
            elif type == "SELL" or type == "sell":
                order = self.bitflyer_api.sendchildorder(product_code=product, child_order_type='MARKET',
                                                         side='SELL', size=str(amount))
                data2csv.data2csv(
                    [time.strftime('%b:%d:%H:%M'), 'order', 'SELL_MARKET', 'amount', '%f' % float(amount)])
                predict.print_and_write('Sell market ' +str(amount))
            else:
                print("error!")
            if 'child_order_acceptance_id' in order:
                time.sleep(2)
                execute_price = self.get_execute_order()
                if execute_price != 0:
                    if type == "SELL" or type == "sell":
                        slides = float(wprice) - float(execute_price)
                        predict.print_and_write('SELL : Wish price: %f, deal price: %f, slide : %f'%(wprice, execute_price, slides))
                    elif type == "BUY" or type == "buy":
                        slides = float(execute_price) - float(wprice)
                        predict.print_and_write('BUY : Wish price: %f, deal price: %f, slide : %f'%(wprice, execute_price, slides))
                return order
            else:
                try_t += 1
                print(order)
                print('Failed, try again')
                time.sleep(20)


    # deal with maintance time
    def maintance_time(self):
        while 1:
            cur_oclock = int(time.strftime('%H:')[0:-1])
            cur_min = int(time.strftime('%M:')[0:-1])
            if (cur_oclock == 4 and cur_min >= 0 and cur_min <= 12) or (cur_oclock == 3 and cur_min >= 58):
                predict.print_and_write('Server maintenance')
                time.sleep(60)
                continue
            else:
                return

    def get_execute_order(self):
        try:
            result = self.bitflyer_api.getexecutions(product_code = 'FX_BTC_JPY',count = 1)
            #print(result['price'])
            return(float(result[0]['price']))
        except Exception:
            return (0)

    # judge if the time stamp in this hour
    def bf_timejudge(self, timestring):
        cur_time = time.gmtime()
        #time.sleep(10)
        #cur_time2 = time.gmtime()
        a = time.mktime(timestring)
        b = time.mktime(cur_time)
        tdelta = b - a
        return(tdelta)

    def get_curhour(self):
        cur_hour = datetime.datetime.fromtimestamp(time.time() - time.time() % 3600 +10)
        return(cur_hour.timestamp())

    def judge_order(self, id):
        i = 20
        while i > 0:
            try:
                order = self.get_orderbyid(id)
                if order['parent_order_state'] == 'REJECTED':
                    predict.print_and_write('Order rejected')
                    return True
                else:
                    return False
            except Exception:
                time.sleep(5)
                print(Exception)
                print('Exception Try again')
                i -= 1
        predict.print_and_write('Try many times but no result, return False without confidence')
        return False

    def get_hilo(self):
        i = 0
        while i < 100:
            try:
                hilos = technical_fx_turtle.HILO()
                result = hilos.publish_current_hilo_price()
        # result = prediction.publish_current_limit_price(periods="1H")
                sell = float(result[1])
                buy = float(result[0])
                close = float(result[2])  # the close price of last hour
                high = float(result[3])
                low =float(result[4])
                quits = float(result[5])
                quitl = float(result[6])
                return([sell, buy, close, high, low, quits, quitl])
            except Exception:
                print(Exception)
                predict.print_and_write('Try to get hilo again')
                time.sleep(10)
                i+=1
                continue

    def get_ATR(self):
        i = 0
        while i < 100:
            try:
                atrs = technical_fx_hilo2.HILO()
                result = atrs.getATR()
                # result = prediction.publish_current_limit_price(periods="1H")
                return (result)
            except Exception:
                print(Exception)
                predict.print_and_write('Try to get atr again')
                time.sleep(10)
                i += 1
                continue


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

    def get_checkin_price(self):
        p = self.bitflyer_api.getpositions(product_code='FX_BTC_JPY')
        position0 = 0.0
        checkin_price = 0.0
        #time_diff = 0
        if isinstance(p, list):
            for i in p:
                #predict.print_and_write('check in price: %f' % (i['price']))
                if i['side'] == 'SELL':
                    position0 -= i['size']
                else:
                    position0 += i['size']

            for i in p:
                checkin_price += i['size']/abs(position0) * i['price']
            #predict.print_and_write('Check in price: %f, position: %f' % (checkin_price, position0))

            # for i in p:
            #     opentime = i['open_date']
            #     time_diff = self.bf_timejudge(opentime)
            #     break

        elif isinstance(p, dict) or len(p) == 0:
            predict.print_and_write('Position not exist')
        checkin_price = math.floor(checkin_price)
        return([checkin_price, position0])

    def get_current_price(self, number):
        d = 200
        while d > 0:
            try:
                trade_history = self.bitflyer_api.executions(product_code = 'FX_BTC_JPY', count = number)
                total_size = 0.0
                cur_price = 0.0
                for i in trade_history:
                    total_size += i['size']

                for i in trade_history:
                    cur_price += i['size']/total_size * i['price']

                return(math.floor(cur_price))
            except Exception:
                print('Get price error ,try again')
                time.sleep(10)
                d -= 1
                continue
        print('Try too many times, failed')
        return 0.0

    def detect_and_trade(self, direction, line, amount):
        price = self.get_current_price(30)
        print('Price: %5.0f, Line: %5.0f' % (price, line), end='\r')
        if direction == 'buy':
            if price > line and price != 0 :
                predict.print_and_write(price)
                order = self.trade_market('buy', amount, int(price))
                predict.print_and_write(order)
                return(True)
        elif direction == 'sell':
            if price < line and price != 0 :
                predict.print_and_write(price)
                order = self.trade_market('sell', amount, int(price))
                predict.print_and_write(order)
                return(True)
        return(False)



    def trade_hour_init(self, checkins, cur_price, hilo):
        # if we have a new position in this hour, initial position and return suggested position.

        position_suggest = checkins[1]

        if hilo[2] >= hilo[1] : # if close > hi
            #TODO
            trade_mount = self.init_trade_amount_buy - checkins[1]
            if trade_mount > 0.0:
                amount_str = '%.2f' % (trade_mount)
                self.trade_market('buy', amount_str, int(cur_price))
                predict.print_and_write('Switch to long')
                position_suggest = self.init_trade_amount_buy
                self.loss_cut_line = -100
                self.acc_factor = -0.02
                self.max_profit = 0
            # buy self.init + checkins[1]


        elif hilo[2] <= hilo[0] : # if close < lo
            # TODO
            # sell self.init + checkins[1]
            trade_mount = self.init_trade_amount_sell + checkins[1]
            if trade_mount > 0.0:
                amount_str = '%.2f' % (trade_mount)
                self.trade_market('sell', amount_str,int(cur_price) )
                predict.print_and_write('Switch to short')
                position_suggest = -self.init_trade_amount_sell
                self.loss_cut_line = -100
                self.acc_factor = -0.02
                self.max_profit = 0

        elif cur_price > hilo[0] and cur_price < hilo[1]:
            predict.print_and_write('Switch to middle')
            if checkins[1] < 0.0:
                trade_mount = '%.2f' % (abs(checkins[1]))
                self.trade_market('buy', trade_mount, int(cur_price))
                predict.print_and_write('Buy short back')
            elif checkins[1] > 0.0:
                trade_mount = '%.2f' % (abs(checkins[1]))
                self.trade_market('sell', trade_mount, int(cur_price))
                predict.print_and_write('Sell long back')
            position_suggest = 0
            self.loss_cut_line = -100
            self.acc_factor = -0.02
            self.max_profit = 0

        predict.print_and_write('Suggest position:%.3f'%(float(position_suggest)))
        return(position_suggest)

        # check the position
    def get_stop_acc_line(self, atr, checkins, cur_p):
        position = checkins[1]
        check_p = checkins[0]
        init_loss_cut_factor = 2.2
        trail_max_ratio = 0.24
        trail_ratio_acc = 0.02
        max_line = 0

        profit = 0
        if position > 0.0:
            profit = cur_p - check_p
            if self.loss_cut_line == -100:
                self.loss_cut_line = check_p - init_loss_cut_factor * atr
                predict.print_and_write(
                    'Init loss cut line: %.0f' % (
                        self.loss_cut_line))
        elif position < 0.0:
            profit = check_p - cur_p
            # init the loss cut line
            if self.loss_cut_line == -100:
                self.loss_cut_line = check_p + init_loss_cut_factor * atr
                predict.print_and_write(
                    'Init loss cut line: %.0f' % (
                        self.loss_cut_line))
        predict.print_and_write('Max profit in last hour: %.0f'%profit)

        if profit > self.max_profit:
            self.max_profit = profit
            self.acc_factor += trail_ratio_acc
            if self.acc_factor > trail_max_ratio:
                self.acc_factor = trail_max_ratio
            predict.print_and_write('Max profit updated: %.0f, acc_factor: %.3f'%(self.max_profit, self.acc_factor))

            if position > 0.0:
                max_line = check_p + self.max_profit
            elif position < 0.0:
                max_line = check_p - self.max_profit

            trail_loss_cut = abs(max_line - self.loss_cut_line) * (1 - self.acc_factor)

            if position > 0.0:
                new_loss_cut_line = max_line - trail_loss_cut
                if new_loss_cut_line > self.loss_cut_line:
                    predict.print_and_write(
                        'loss cut line updated: %.0f -> %.0f' % (self.loss_cut_line, new_loss_cut_line))
                    self.loss_cut_line = new_loss_cut_line
            elif position < 0.0:
                new_loss_cut_line = max_line + trail_loss_cut
                if new_loss_cut_line < self.loss_cut_line:
                    predict.print_and_write(
                        'loss cut line updated: %.0f -> %.0f' % (self.loss_cut_line, new_loss_cut_line))
                    self.loss_cut_line = new_loss_cut_line

        else:
            trail_loss_cut = init_loss_cut_factor * atr
            if position > 0.0:
                new_loss_cut_line = check_p - trail_loss_cut
                if new_loss_cut_line > self.loss_cut_line:
                    predict.print_and_write(
                        'Profit is less than 0, loss cut line:2.2 ATR %.0f -> %.0f' % (
                        self.loss_cut_line, new_loss_cut_line))
                    self.loss_cut_line = new_loss_cut_line
            elif position < 0.0:
                new_loss_cut_line = check_p + trail_loss_cut
                if new_loss_cut_line < self.loss_cut_line:
                    predict.print_and_write(
                        'Profit is less than 0, loss cut line:2.2 ATR %.0f -> %.0f' % (
                        self.loss_cut_line, new_loss_cut_line))
                    self.loss_cut_line = new_loss_cut_line

    # detect order in hour
    # record the inital state of position
    # if position changed
    # detect the profit
    # following profit ever 1 min, if profit is starting to reduce , quite (need a trial order)
    def trade_in_hour(self, initposition, starttime, hilo, atr):
        amount_stop = abs(float('%.2f' % (initposition)))
        tdelta = self.bf_timejudge(starttime)
        self.switch_in_hour = False
        enable_other_side = True
        switch2other_side = False
        print_onec = True
        trial_loss_cut = atr
        suggest_position = initposition

        switch_line = self.loss_cut_line
        print('quit_short ', hilo[5], 'quit_long ', hilo[6])
        if initposition > 0.0 and hilo[6] > self.loss_cut_line:
            predict.print_and_write('quit line is higher than stop line, use quit %.0f to quit'%(hilo[6]))
            switch_line = hilo[6]
        elif initposition < 0.0 and hilo[5] < self.loss_cut_line:
            predict.print_and_write('quit line is lower than stop line, use quit %.0f to quit'%(hilo[5]))
            switch_line = hilo[5]


        predict.print_and_write('hi: %.0f, lo: %.0f, close: %.0f, atr: %.0f, quit: %.0f' % (hilo[1], hilo[0], hilo[2], atr, switch_line))


        if initposition > 0.0:
        # if we have a positive position, detect a change to quit and switch
            tdelta = self.bf_timejudge(starttime)
            predict.print_and_write('Detecting a chance to switch short')
            while tdelta < 3600:
                direction = 'sell'
                if not self.switch_in_hour:
                # if not switch , detecting
                    self.switch_in_hour = self.detect_and_trade(direction, switch_line, amount_stop)
                else:
                # if switch
                    if print_onec:
                        predict.print_and_write('Switch in hour')
                        suggest_position = 0
                        self.loss_cut_line = -100
                        self.acc_factor = -0.02
                        self.max_profit = 0
                        checkins = self.judge_position(suggest_position)
                        print_onec = False
                    if (not switch2other_side) and enable_other_side:
                        switch2other_side = self.detect_and_trade(direction, hilo[0], self.init_trade_amount_sell)
                    elif switch2other_side and enable_other_side:
                        suggest_position = -self.init_trade_amount_sell
                        checkins = self.judge_position(suggest_position)
                        predict.print_and_write('switch to other side')
                        self.trial_order(checkins, trial_loss_cut, starttime)
                    # trade another direction:
                time.sleep(0.8)
                tdelta = self.bf_timejudge(starttime)

        elif initposition < 0.0:
            # if we have a positive position, detect a change to quit and switch
            tdelta = self.bf_timejudge(starttime)
            predict.print_and_write('Detecting a chance to switch long')
            while tdelta < 3600:
                direction = 'buy'

                if not self.switch_in_hour:
                    # if not switch , detecting
                    self.switch_in_hour = self.detect_and_trade(direction, switch_line, amount_stop)
                else:
                    # if switch
                    if print_onec:
                        predict.print_and_write('Switch in hour')
                        suggest_position = 0
                        self.loss_cut_line = -100
                        self.acc_factor = -0.02
                        self.max_profit = 0
                        checkins = self.judge_position(suggest_position)
                        print_onec = False
                    if not switch2other_side and enable_other_side:
                        switch2other_side = self.detect_and_trade(direction, hilo[1], self.init_trade_amount_buy)
                    elif switch2other_side and enable_other_side:
                        predict.print_and_write('switch to other side')
                        suggest_position = self.init_trade_amount_buy
                        checkins = self.judge_position(suggest_position)
                        self.trial_order(checkins, trial_loss_cut, starttime)

                    # trade another direction:
                time.sleep(0.8)
                tdelta = self.bf_timejudge(starttime)


        elif initposition == 0.0 and enable_other_side:
            # if we have a positive position, detect a change to quit and switch
            tdelta = self.bf_timejudge(starttime)
            predict.print_and_write('Detecting a chance to get in')
            switch_in_hourbuy = False
            switch_in_hoursell = False
            while tdelta < 3600:
                if not self.switch_in_hour:
                    # if not switch , detecting
                    switch_in_hoursell= self.detect_and_trade('sell', hilo[0], self.init_trade_amount_sell)
                    time.sleep(0.8)
                    switch_in_hourbuy = self.detect_and_trade('buy', hilo[1], self.init_trade_amount_buy)
                    self.switch_in_hour = switch_in_hourbuy or switch_in_hoursell
                elif switch_in_hourbuy:
                    predict.print_and_write('Bulid in hour long')
                    suggest_position = float(self.init_trade_amount_buy)
                    checkins = self.judge_position(suggest_position)
                    print_onec = False
                    self.trial_order(checkins, trial_loss_cut, starttime)
                    switch_in_hourbuy = False
                elif switch_in_hoursell:
                    predict.print_and_write('Bulid in hour short')
                    suggest_position = -float(self.init_trade_amount_sell)
                    checkins = self.judge_position(suggest_position)
                    print_onec = False
                    self.trial_order(checkins, trial_loss_cut, starttime)
                    switch_in_hourbuy = False
                time.sleep(0.8)
                tdelta = self.bf_timejudge(starttime)

    def trial_order(self, checkins, trial_loss_cut, starttime):
        # Trial order keep loss less than trial_loss_cut
        profit = 0
        max_profit = 0
        pre_profit = -trial_loss_cut
        atr = trial_loss_cut
        tdelta = self.bf_timejudge(starttime)
        startt= tdelta
        predict.print_and_write('Use a trial order')
        #predict.print_and_write('Current position: %f, price: %f' % (checkins[1], checkins[0]))
        while tdelta < 3600:
            cur_price = self.get_current_price(50)
            if checkins[1] > 0:
                profit = cur_price - checkins[0]
            elif checkins[1] < 0:
                profit = checkins[0] - cur_price
            if profit > max_profit:
                max_profit = profit
                if max_profit > atr * 0.5 and max_profit < atr:
                    trial_loss_cut = atr * 0.5
                elif max_profit >= atr and max_profit< atr * 2:
                    trial_loss_cut = atr
                elif max_profit >= atr * 2:
                    trial_loss_cut = max_profit /2
                if trial_loss_cut > 15000:
                    trial_loss_cut = 15000


            dt = tdelta- startt

            if profit < pre_profit:
                # quit
                if checkins[1] > 0.0:
                    trade_mount = '%.2f' % abs(checkins[1])
                    order = self.trade_market('sell', trade_mount, int(cur_price))
                    suggest_position = 0.0
                    checks = self.judge_position(suggest_position)
                    predict.print_and_write(order)
                elif checkins[1] < 0.0:
                    trade_mount = '%.2f' % abs(checkins[1])
                    order = self.trade_market('buy', trade_mount, int(cur_price))
                    suggest_position = 0.0
                    checks = self.judge_position(suggest_position)
                    predict.print_and_write(order)

                predict.print_and_write('Quit position ,profit: %.2f, time: %d'%(profit, dt))
                return

            elif profit >= pre_profit and profit > 0:
                temp_pre_profit = profit - trial_loss_cut
                if temp_pre_profit > pre_profit:
                    pre_profit = temp_pre_profit
            print('T: %d, P: %5.0f, MP: %5.0f, L: %5.0f' %(dt, profit, max_profit, pre_profit), end='\r')
            time.sleep(0.8)
            tdelta = self.bf_timejudge(starttime)
        predict.print_and_write('Time is over, quit, final profit: %5.0f'%(profit))


    # judge if it is order succeed
    def judge_position(self, suggest_position):
        t = 0
        while t < 100000:
            checkins = self.get_checkin_price()
            if abs(suggest_position - checkins[1]) < 0.01:
                predict.print_and_write('Suggest is same as real')
                return(checkins)
            t += 1
            predict.print_and_write(
                'Position is unusual, suggest: %.3f, real: %.3f , check again' % (suggest_position, checkins[1]))
            time.sleep(5)  # in 5s , we should obvious the position change.
            if (t % 100) == 0 and t > 99 :
                predict.print_and_write('Recorrect position')
                if suggest_position - checkins[1] > 0:
                    self.trade_market('buy', '%.2f'%(suggest_position - checkins[1]))
                elif suggest_position - checkins[1] < 0:
                    self.trade_market('sell', '%.2f'%(checkins[1] -suggest_position ))
        predict.print_and_write('Something is wrong, trade but not succeed')
        return(checkins)


    def judge_condition(self): # judge position at hour start.
        time.sleep(1)
        starttime = time.gmtime(self.get_curhour())
        checkins = self.get_checkin_price()
        suggest_position = checkins[1]
        predict.print_and_write('##################################################')
        cur_price = self.get_current_price(100)
        predict.print_and_write('Start a new hour: Current price: %f' % (cur_price))
        predict.print_and_write('Check in price: %.0f, position: %.2f' % (checkins[0], checkins[1]))
        hilo = self.get_hilo()
        time.sleep(3)
        atr = round(float(self.get_ATR()),0)
        self.decide_trade_amount(cur_price, atr * 2.2)



        # if keep a position and transfor in this hour. ckeck position again:
        if (checkins[1] != 0.0 and self.switch_in_hour) or checkins[1] == 0.0:
            if checkins[1] == 0.0:
                predict.print_and_write('No position exist, trade none position')
            else:
                predict.print_and_write('Trade with position %f and init position'%checkins[1])
            suggest_position = self.trade_hour_init(checkins, cur_price, hilo)
            #self.order_id = order['parent_order_acceptance_id']

            # we should verify the order is dealing or not here
            checkins = self.judge_position(suggest_position)
            #order = self.update_order(checkins, hilo)
        if checkins[1] != 0.0:
            if checkins[1] > 0.0:
                last_peak = hilo[3]
                self.get_stop_acc_line(atr, checkins, last_peak)
            else:
                last_peak = hilo[4]
                self.get_stop_acc_line(atr, checkins, last_peak)

        self.trade_in_hour(suggest_position, starttime, hilo, atr)
        # elif checkins[1] != 0.0 and not self.switch_in_hour:
        #     predict.print_and_write('Update order')
        #     order = self.update_order(checkins, hilo)
        #     self.order_id = order['parent_order_acceptance_id']

        # perform a stop order and detect


    def get_collateral(self):
        try:
            result = self.bitflyer_api.getcollateral(product_code = 'FX_BTC_JPY')
            self.total_margin = float(result['collateral'])
            self.useable_margin = self.total_margin - self.least_collateral
            print('Useable for trading: %.0f'%self.useable_margin)
            data2csv.data2csv(result)
            predict.print_and_write(result)
        except Exception:
            predict.print_and_write(Exception)

def sendamail(title ,str):
    address = 'phoenixflame11@rakuten.jp'  # change the reciver e-mail address to yours
    username = 'goozzfgle@gmail.com'
    paswd = 'googlebaidu1'

    mail_str = '%s %s' % (str, formatdate(None, True, None))
    sender = SendMail(address, username, paswd)
    msg = MIMEText(mail_str)
    msg['Subject'] = title
    msg['From'] = username
    msg['To'] = address
    msg['Date'] = formatdate()
    sender.send_email(address, msg.as_string())



if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    autoTrading = AutoTrading()

    if argc >= 2:
        cofile = sys.argv[1]
    else:
        cofile = 'order.ini'
        #tempcf = dict()
        #tempcf['stoploss'] = {'max_profit':autoTrading.max_profit,
        #                   'loss_cut_line':autoTrading.loss_cut_line,
        #                   'acc_factor':autoTrading.acc_factor}

        #cf.save_config_order(tempcf)
    cf = configIO.configIO(config_file=cofile)
    parameters = cf.read_config_order('stoploss')
    autoTrading.max_profit = parameters['max_profit']
    autoTrading.loss_cut_line = parameters['loss_cut_line']
    autoTrading.acc_factor = parameters['acc_factor']
    predict.print_and_write('config read')



    #tdelta = autoTrading.bf_timejudge('2018-05-21T14:35:44.713')
    try_times = 20
    while 1:
        if autoTrading.panic:
            p2 = cf.read_config_order('panic')
            autoTrading.init_panic_index = p2['init_panic_index']
            print('Panic read')

        autoTrading.get_collateral()
        autoTrading.judge_condition()
        tempcf = dict()
        tempcf['stoploss'] = {'max_profit':autoTrading.max_profit,
                           'loss_cut_line':autoTrading.loss_cut_line,
                           'acc_factor':autoTrading.acc_factor}
        predict.print_and_write('config saved')
        cf.save_config_order(tempcf)


    #tdelta = autoTrading.bf_timejudge('2018-05-21T14:35:44.713')
    # while try_times > 0:
    #     try:
    #         while 1:
    #             autoTrading.judge_condition()
    #             autoTrading.get_collateral()
    #     except Exception:
    #         print(Exception)
    #         sendamail('Exception', 'exception happend')
    #         predict.print_and_write('Exception happened, try again')
    #         predict.print_and_write('Last try times: %d'%try_times)
    #         try_times -= 1