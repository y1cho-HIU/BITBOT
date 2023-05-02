import MockAccount
import params_private as prv
import params_public as pub
import execute_function as ef


class NonLiveBacktesting:
    def __init__(self, coin_data):
        self.coin_data = coin_data
        self.account = MockAccount.MockAccount(pub.set_init_balance)

    def execute(self, env_weight, sma_period):
        sma_period = sma_period
        env_weight = env_weight
        past_coin_list = []
        next_position = pub.POS_OUT
        next_trading = False

        for idx, row in self.coin_data.iterrows():
            if next_trading:
                """ trading at open time """
                if next_position == pub.POS_OUT:
                    self.account.pos_out(row['open'])
                elif next_position == pub.POS_LONG:
                    self.account.pos_in(row['open'], 'LONG')
                elif next_position == pub.POS_SHORT:
                    self.account.pos_in(row['open'], 'SHORT')

            """ calc. SMA_{period} """
            if len(past_coin_list) < sma_period:
                past_coin_list.append(row['close'])
            elif len(past_coin_list) == sma_period:
                del past_coin_list[0]
                past_coin_list.append(row['close'])

            next_position, next_trading = ef.strategy(row['close'], past_coin_list, self.account.position, env_weight)

        self.account.display_win_rate(weight=env_weight, period=sma_period)
