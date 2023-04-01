import pandas as pd
from datetime import datetime
import params

buy_price = 100
amount = 10
trading_fee = 0.5
trading_info_test = pd.DataFrame(columns=params.trading_info_columns)
buy_info = pd.DataFrame([datetime.now(), 1, buy_price, amount, buy_price * amount, trading_fee], columns=params.trading_info_columns)
trading_info_test = pd.concat([buy_info, trading_info_test], axis=1)

print(trading_info_test)