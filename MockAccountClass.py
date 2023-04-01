from datetime import datetime
import pandas as pd

import params

trading_info_columns = ['time', 'type', 'price', 'amount', 'volume', 'fee']


class MockAccount:
    def __init__(self, init_balance):
        self.free_balance = init_balance
        self.used_balance = 0
        self.coin_amount = 0
        self.__total_balance = self.free_balance + self.used_balance

        self.trading_info = pd.DataFrame(columns=trading_info_columns)

    def buy_order(self, buy_price, amount):
        trading_fee = buy_price * amount * params.fee_rate
        self.free_balance -= buy_price * amount + trading_fee
        self.coin_amount += amount
        buy_info = [datetime.now(), 'BUY', buy_price, amount, buy_price * amount, trading_fee]
        self.trading_info.append(pd.Series(buy_info, index=self.trading_info.columns), ignore_index=True)

    def sell_order(self, sell_price, amount):
        trading_fee = sell_price * amount * params.fee_rate
        self.free_balance += sell_price * amount + trading_fee
        self.coin_amount -= amount
        sell_info = [datetime.now(), 'SELL', sell_price, amount, sell_price * amount, trading_fee]

    def display_trading_info(self):
        print(self.trading_info)

    def display_account_info(self):
        print('#' * 30)
        print('# ACCOUNT INFO #')
        print('CASH :  ', self.free_balance)
        print('COIN :  ', self.coin_amount)
        print('TOTAL : ', self.__total_balance)
        print('#' * 30)