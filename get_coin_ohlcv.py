from datetime import datetime

import pandas as pd

import authorization

auth = authorization.Auth
xrp_5m = auth.get_historical_klines(
    symbol="XRPUSDT",
    interval='5m',
    start_str="2023-03-01",
    end_str="2023-03-31"
)
columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'QAV', 'NOT', 'BASE', 'QUOTE', 'IGNORE']

df_xrp_5m = pd.DataFrame(xrp_5m, columns=columns)
df_xrp_5m['open'].astype(float)
df_xrp_5m['high'].astype(float)
df_xrp_5m['low'].astype(float)
df_xrp_5m['close'].astype(float)
df_xrp_5m['volume'].astype(float)

df_xrp_5m.drop(labels=['close_time', 'QAV', 'NOT', 'BASE', 'QUOTE', 'IGNORE'], axis=1, inplace=True)
df_xrp_5m.to_csv("./coin_data/xrp_5m_30d", index=False, index_label='datetime')
