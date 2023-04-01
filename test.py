import unittest
import pandas as pd
import params
from datetime import datetime


class MockAccountTest(unittest.TestCase):
    def Test_DataFrame_input(self):
        buy_price = 100
        amount = 10
        trading_fee = 0.5
        trading_info_test = pd.DataFrame(columns=params.trading_info_columns)
        buy_info = [datetime.datetime.now(), 1, buy_price, amount, buy_price * amount, trading_fee]
        trading_info_test.append([buy_info])

        print(trading_info_test)
        for idx, row in trading_info_test.iterrows():
            self.assertEqual(row[idx], 'NaN')




