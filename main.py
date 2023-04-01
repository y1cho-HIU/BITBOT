import pandas as pd
import NonLiveBacktestingClass as bt


def main(argv):
    btc_df = pd.read_csv('./btc_df.csv')
    backtesting = bt.NonLiveBacktesting(btc_df)
    backtesting.execute()


if __name__ == '__main__':
    import sys
    main(sys.argv)