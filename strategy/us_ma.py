#us moving average strategy
import sys
sys.path.append('..')
from db.us_db import US_Database
import numpy as np
import pandas as pd
import datetime
from strategy_base import Strategy
import sklearn
from sklearn import linear_model
from util.plot_util import PlotUtil

import matplotlib.pyplot as plt

class MA_strategy(Strategy):
    def __init__(self,tickers):
        self.short_k_day = 5
        self.middle_k_day = 15
        self.long_k_day = 50
        self.target_range = 20 #计算周期
        self.db = db
        self.tickers = tickers
        self.ticker_filter_result = [];

    def filter_ticker(self):
        print('is calculating ...')
        for ticker in self.tickers:
            ticker_data = self.db.get_moving_average_price(ticker,self.target_range,1)
            #in case empty
            if ticker_data.empty == True or ticker_data.shape[0] == 0 :
                continue
            #price between 5 ~ 25
            price = ticker_data['adj_close'][-1]


            if price >= 5 and price <= 25:
                #short < middle < short
                short_k = self.db.get_moving_average_price(ticker,self.target_range,self.short_k_day)['adj_close']
                middle_k = self.db.get_moving_average_price(ticker,self.target_range,self.middle_k_day)['adj_close']
                long_k = self.db.get_moving_average_price(ticker,self.target_range,self.long_k_day)['adj_close']

                short_k_price = short_k[-1]
                middle_k_price = middle_k[-1]
                long_k_price = long_k[-1]
                profit_short_k = self.db.get_profit_by_days(ticker,self.short_k_day)
                volume = ticker_data['volume'][-1]


                #接下来还要从以下几点考虑
                #成交量，20% － 50％，
                #盈利前 10-30％
                if(short_k_price > middle_k_price) and (middle_k_price > long_k_price) and abs(middle_k_price - long_k_price) < 1:

                    #linear regression
                    reg = linear_model.LinearRegression()
                    train_short_x = np.arange(short_k.shape[0]).reshape(short_k.shape[0],1)
                    train_short_y = np.array(short_k)
                    train_middle_x = np.arange(middle_k.shape[0]).reshape(middle_k.shape[0],1)
                    train_middle_y = np.array(middle_k)
                    train_long_x = np.arange(long_k.shape[0]).reshape(long_k.shape[0],1)
                    train_long_y = np.array(long_k)

                    reg.fit(train_short_x,train_short_y)
                    short_k_coef = reg.coef_
                    short_k_intercept = reg.intercept_

                    reg.fit(train_middle_x,train_middle_y)
                    middle_k_coef = reg.coef_
                    middle_k_intercept = reg.intercept_

                    reg.fit(train_long_x,train_long_y)
                    long_k_coef = reg.coef_
                    long_k_intercept = reg.intercept_

                    if short_k_coef > middle_k_coef and middle_k_coef > long_k_coef:
                        print('ticker',ticker,'===')
                        plt = PlotUtil()
                        plt.plot_k(np.array(ticker_data['adj_close']),np.array(short_k),np.array(middle_k),np.array(long_k))

                        self.ticker_filter_result.append({
                            'ticker': ticker,
                            'profit': profit_short_k,
                            'volume': volume
                            })



        #10% - 30% profit
        self.ticker_filter_result = pd.DataFrame(self.ticker_filter_result).sort_values(by=['profit'])
        print (self.ticker_filter_result)

        shape = self.ticker_filter_result.shape[0]
        self.ticker_filter_result = self.ticker_filter_result[int(shape * 0.7): int(shape * 0.9)].sort_values(by=['volume'])
        #20%-50% volume
        shape = self.ticker_filter_result.shape[0]
        self.ticker_filter_result = self.ticker_filter_result[int(shape * 0.5): int(shape * 0.8)]

        print(self.ticker_filter_result)
        return (self.ticker_filter_result)




if __name__ == '__main__':
    db = US_Database()
    plt = PlotUtil()
    symbols = db.get_33_66_volume_by_day_symbol(10)
    ma = MA_strategy(symbols)
    tickers = ma.filter_ticker()


