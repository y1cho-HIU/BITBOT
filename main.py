import pandas as pd
import NonLiveAdvanced as nlbt


def main(argv):
    xrp_df =pd.read_csv('./coin_data/xrp_5m_30d')
    backtesting = nlbt.NonLiveBacktesting(xrp_df)
    backtesting.execute(0.0005, 7)


if __name__ == '__main__':
    import sys
    main(sys.argv)
