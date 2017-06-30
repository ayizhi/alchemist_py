#看前十天的数据对后3天的盈利有什么影响
import sklearn
import pandas as pd
import numpy as np
from strategy_base import Strategy
import datetime
import sys
sys.path.append('../')
from db.us_db import US_Database
from util.feature_util import Feature_util

class Unicon_strategy(Strategy):
    def __init__(self):
        self.target_date = datetime.datetime(2017,3,1)
        self.feature_date_range = 10
        self.profit_date_range = 3
        self.more_date = 5 #移动平均需要多出来的数据
        self.db = US_Database()
        self.feature_util = Feature_util()

    def pre_deal_data(self):
        symbols = self.db.get_symbol_from_db()
        for ticker in symbols:
            start_date = self.target_date - datetime.timedelta(days=(self.feature_date_range + self.more_date))
            ticker_data = self.db.get_ticker_by_id(ticker,start_date,self.target_date)

            #addFeatures
            ticker_data = self.feature_util.CCI(ticker_data,self.more_date)
            ticker_data = self.feature_util.TL(ticker_data,self.more_date)
            ticker_data = self.feature_util.EVM(ticker_data,self.more_date)
            ticker_data = self.feature_util.SMA(ticker_data,self.more_date)
            ticker_data = self.feature_util.EWMA(ticker_data,self.more_date)
            ticker_data = self.feature_util.ROC(ticker_data,self.more_date)
            ticker_data = self.feature_util.BBANDS(ticker_data,self.more_date)



            print(ticker_data)

            break



if __name__ == '__main__':
    unicon = Unicon_strategy()
    unicon.pre_deal_data()