import MockAccount
import params_private as prv
import params_public as pub


class NonLiveBacktesting:
    def __init__(self, coin_data):
        self.coin_data = coin_data
        self.account = MockAccount.MockAccount(pub.set_init_balance)

    def _can_buy(self, coin_price, coin_amount):
        can_buy = False
        total_req = (coin_price * coin_amount) * (1 + pub.fee_rate)

        if self.account.free_balance >= total_req:
            can_buy = True

        return can_buy

    def _can_sell(self, coin_amount):
        can_sell = False
        if (self.account.coin_amount >= coin_amount) & (coin_amount != 0.0):
            can_sell = True

        return can_sell

    @staticmethod
    def _buy_signal(row_df):
        """ basic strategy """
        buy_signal = False
        if row_df['open'] <= row_df['bb_l']:
            buy_signal = True
        return buy_signal

    @staticmethod
    def _sell_signal(row_df):
        """ basic strategy """
        sell_signal = False
        if row_df['open'] >= row_df['bb_l']:
            sell_signal = True
        return sell_signal

    def execute(self):
        coin_price = self.coin_data['open'][0]

        for idx, row in self.coin_data.iterrows():
            coin_price = row['open']
            if self._buy_signal(row):
                buy_full_amount = (self.account.free_balance / row['open']) * (1 - pub.fee_rate)
                if self._can_buy(row['open'], buy_full_amount):
                    self.account.buy_order(row['open'], buy_full_amount)
                    self.display_trading_info('BUY', row['open'], buy_full_amount)
            if self._sell_signal(row):
                if self._can_sell(self.account.coin_amount):
                    self.account.sell_order(row['open'], self.account.coin_amount)
                    self.display_trading_info('SELL', row['open'], self.account.coin_amount)

        print('START BALANCE : ', pub.set_init_balance)
        print('END BALANCE : CASH : {0} \t COIN_AMOUNT : {1} \t COIN_VALUE : {2}'.format(self.account.free_balance, self.account.coin_amount, self.account.coin_amount * coin_price))

    @staticmethod
    def display_trading_info(sell_buy, price, amount):
        print('{0} \t PRICE : {1} \t AMOUNT : {2}'.format(sell_buy, price, amount))
