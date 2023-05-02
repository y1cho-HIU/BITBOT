import ccxt

import MockAccount
import params_private as prv
import params_public as pub
import keyboard
import pandas as pd

live_coin_columns = ['datetime', 'open', 'close', 'volume']


class LiveBacktesting:

    def __init__(self):
        self.coin_data = pd.DataFrame(columns=live_coin_columns)
        self.account = MockAccount.MockAccount(pub.set_init_balance)
        self.hist_list = []

    def get_hist_data(self):
        binance = ccxt.binance()
        xrp_ohlcv = binance.fetch_ohlcv(symbol="XRP/USDT", timeframe='5m', limit=prv.sma_period)
        df = pd.DataFrame(xrp_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        df.set_index('datetime', inplace=True)
        for i in xrp_ohlcv:
            self.hist_list.append(i[4])

    @staticmethod
    def calc_rrr(env, sma, rate):
        return round(((rate+1) * env - sma) / rate, 4)

    def execute(self, env_weight=prv.env_weight, sma_period=prv.sma_period):
        live_data = ccxt.binance()
        self.get_hist_data()
        env_weight = env_weight
        sma_period = sma_period
        while True:
            key = keyboard.is_pressed()
            if key == 'q':
                # message
                print('TRADING PAUSED')
                break
            curr_info = live_data.fetch_ticker(pub.ticker)
            live_list = [curr_info['datetime'], curr_info['open'], curr_info['close'], curr_info['volume']]
            self.coin_data.append(pd.Series(live_list, index=live_coin_columns), ignore_index=True)

            now_sma = round(sum(self.hist_list)/len(self.hist_list), 4)
            env_up = round(now_sma * (1 + env_weight), 4)
            env_down = round(now_sma * (1 - env_weight), 4)
            rrr_up = self.calc_rrr(env=env_up, sma=now_sma, rate=prv.rrr_rate)
            rrr_down = self.calc.rrr(env=env_up, sma=now_sma, rate=prv.rrr_rate)

            """
            if coin_data isn't enough -> processing or do nothing
            """


lb = LiveBacktesting()
lb.get_hist_data()
