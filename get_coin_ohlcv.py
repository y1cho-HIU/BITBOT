from datetime import datetime

import pandas as pd

import authorization


def get_coin_ohlcv(start_time="2023-03-01", end_time="2023-03-31", name="xrp_df"):
    auth = authorization.Auth
    xrp_5m = auth.get_historical_klines(
        symbol="XRPUSDT",
        interval='5m',
        start_str=start_time,
        end_str=end_time
    )
    columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'QAV', 'NOT', 'BASE', 'QUOTE',
               'IGNORE']

    df_xrp_5m = pd.DataFrame(xrp_5m, columns=columns)
    df_xrp_5m['open'].astype(float)
    df_xrp_5m['high'].astype(float)
    df_xrp_5m['low'].astype(float)
    df_xrp_5m['close'].astype(float)
    df_xrp_5m['volume'].astype(float)

    df_xrp_5m.drop(labels=['close_time', 'QAV', 'NOT', 'BASE', 'QUOTE', 'IGNORE'], axis=1, inplace=True)
    df_xrp_5m.to_csv(f'./coin_data/{name}_5m_30d', index=False, index_label='datetime')

# cmd : python get_coin_ohlcv.py
# start_time, end_time, name 설정
get_coin_ohlcv()

