from datetime import datetime
import pandas as pd

import params_private as prv
import params_public as pub

trading_info_columns = ['time', 'type', 'price', 'amount', 'volume', 'fee']


class MockAccount:
    def __init__(self, init_balance):
        self.free_balance = init_balance
        self.used_balance = 0
        self.coin_amount = 0
        self.__total_balance = self.free_balance + self.used_balance

        self.trading_info = pd.DataFrame(columns=trading_info_columns)

        self.trading_count = 0
        self.win_count = 0
        # (self.win_count / self.trading_count) * 100
        self.winning_rate = 0

        self.buy_price = -1
        self.position = pub.POS_OUT

    def buy_order(self, buy_price, amount):
        # buy_price store
        self.buy_price = buy_price

        trading_fee = buy_price * amount * pub.fee_rate
        self.free_balance -= buy_price * amount + trading_fee
        self.coin_amount += amount

        # append trading_info
        buy_info = [datetime.now(), 'BUY', buy_price, amount, buy_price * amount, trading_fee]
        self.trading_info.append(pd.Series(buy_info, index=self.trading_info.columns), ignore_index=True)

    def sell_order(self, sell_price, amount):
        # winning count
        self.trading_count += 1
        if sell_price > self.buy_price:
            self.win_count += 1

        # buy_price = initializing
        self.buy_price = -1

        trading_fee = sell_price * amount * pub.fee_rate
        self.free_balance += sell_price * amount + trading_fee
        self.coin_amount -= amount

        # append trading_info
        sell_info = [datetime.now(), 'SELL', sell_price, amount, sell_price * amount, trading_fee]
        self.trading_info.append(pd.Series(sell_info, index=self.trading_info.columns), ignore_index=True)

    def pos_in(self, buy_price, pos):
        if pos == 'LONG':
            self.position = pub.POS_LONG
        elif pos == 'SHORT':
            self.position = pub.POS_SHORT
        self.buy_price = buy_price
        print('POS_IN  : {0} \t PRICE : {1}'.format(pos, buy_price))

    def pos_out(self, sell_price):
        # long
        if self.position == pub.POS_LONG:
            if sell_price > self.buy_price:
                self.win_count += 1
        # short
        elif self.position == pub.POS_SHORT:
            if sell_price < self.buy_price:
                self.win_count += 1
        self.trading_count += 1
        self.position = pub.POS_OUT
        print('POS_OUT : \t PRICE : {0}'.format(sell_price))

    def display_historical_trading_info(self):
        print(self.trading_info)

    def display_account_info(self):
        print('#' * 30)
        print('# ACCOUNT INFO #')
        print('CASH :  ', self.free_balance)
        print('COIN :  ', self.coin_amount)
        print('TOTAL : ', self.__total_balance)
        print('#' * 30)

    def display_win_rate(self, weight, period):
        if self.trading_count != 0:
            win_rate = round(self.win_count / self.trading_count * 100, 4)
            print('PERIOD : {0} \t WEIGHT : {1} \t WIN : {2} \t TRADING : {3} \t WIN_RATE : {4}'.format(period, weight, self.win_count, self.trading_count, win_rate))
