import pandas as pd
import numpy as np

def calculate_profit(data, risk_reward_ratio, envelope_period, std_multiplier):
    # 인벨로프 밴드 계산
    data['sma'] = data['close'].rolling(window=envelope_period).mean()
    data['std'] = data['close'].rolling(window=envelope_period).std()
    data['upper'] = data['sma'] + (data['std'] * std_multiplier)
    data['lower'] = data['sma'] - (data['std'] * std_multiplier)

    data['cross_upper'] = (data['high'] > data['upper']).astype(int)
    data['cross_lower'] = (data['low'] < data['lower']).astype(int)

    position = 0  # 0: no position, 1: long, -1: short
    entry_price = 0
    exit_price = 0
    profit = 0
    total_trades = 0
    winning_trades = 0
    trading_fee = 0.07  # Trading fee per trade

    for i in range(len(data)):
        if position == 0:
            if data['cross_upper'].iloc[i] == 1:  # Enter short position
                position = -1
                entry_price = data['close'].iloc[i]
                exit_price = entry_price + (entry_price - data['sma'].iloc[i]) * risk_reward_ratio
                total_trades += 1
            elif data['cross_lower'].iloc[i] == 1:  # Enter long position
                position = 1
                entry_price = data['close'].iloc[i]
                exit_price = entry_price - (data['sma'].iloc[i] - entry_price) * risk_reward_ratio
                total_trades += 1
        elif position == -1:  # In a short position
            if data['low'].iloc[i] <= exit_price:  # Stop loss
                profit += ((entry_price - exit_price) / entry_price * 100) - trading_fee
                position = 0
                winning_trades += 1
            elif data['high'].iloc[i] >= data['sma'].iloc[i]:  # Take profit
                profit += ((entry_price - data['close'].iloc[i]) / entry_price * 100) - trading_fee
                position = 0
        elif position == 1:  # In a long position
            if data['high'].iloc[i] >= exit_price:  # Stop loss
                profit -= ((exit_price - entry_price) / entry_price * 100) + trading_fee
                position = 0
            elif data['low'].iloc[i] <= data['sma'].iloc[i]:  # Take profit
                profit -= ((entry_price - data['close'].iloc[i]) / entry_price * 100) + trading_fee
                position = 0
                winning_trades += 1

    if total_trades > 0:
        win_rate = (winning_trades / total_trades) * 100
    else:
        win_rate = 0

    return profit, total_trades, win_rate

data = pd.read_csv('./xrp_df_5m_1y')
risk_reward_ratio = 2
envelope_period = 2
std_multiplier = 0.02

profit, total_trades, win_rate = calculate_profit(data, risk_reward_ratio, envelope_period, std_multiplier)
print(f'Profit: {profit}%')
print(f'Total trades: {total_trades}')
print(f'Win rate: {win_rate}%')
