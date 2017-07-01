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
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor



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

        data_X = [];
        data_Y = [];

        for ticker in symbols:
            start_date = self.target_date - datetime.timedelta(days=(self.feature_date_range + self.more_date))
            ticker_data = self.db.get_ticker_by_id(ticker,start_date,self.target_date)

            if ticker_data.empty :
                continue

            # #addFeatures
            # ticker_data = self.feature_util.CCI(ticker_data,self.more_date)
            # ticker_data = self.feature_util.TL(ticker_data,self.more_date)
            # ticker_data = self.feature_util.EVM(ticker_data,self.more_date)
            # ticker_data = self.feature_util.SMA(ticker_data,self.more_date)
            # ticker_data = self.feature_util.EWMA(ticker_data,self.more_date)
            # ticker_data = self.feature_util.ROC(ticker_data,self.more_date)
            # ticker_data = self.feature_util.BBANDS(ticker_data,self.more_date)
            # ticker_data = ticker_data.dropna()

            date_range = pd.date_range(start=self.target_date - datetime.timedelta(days=(self.feature_date_range)),end=self.target_date)
            ticker_data = ticker_data[date_range[0]: date_range[-1]]

            # #profit
            # profit_list = [];
            # for date in date_range:
            #     profit = self.db.get_profit_by_days(ticker,self.profit_date_range,date + datetime.timedelta(days=self.profit_date_range))
            #     profit_list.append(profit)

            # #formalize
            # ticker_data = (ticker_data - ticker_data.mean())/(ticker_data.max() - ticker_data.min())

            # #get import feature
            # train_x = pd.DataFrame(ticker_data,dtype="|S6")
            # train_y = pd.Series(profit_list,index=date_range,dtype='|S6')
            # important_features = self.feature_util.find_most_important_feature(train_x,train_y,5,5)[0: 5]

            # ticker_data = ticker_data[important_features]

            #append x and y into summary data content
            print(ticker,'=-=============================================')

            data_X.append(np.array(ticker_data['close']))
            data_Y.append(
                self.db.get_profit_by_days(ticker,self.profit_date_range,self.target_date + datetime.timedelta(days=self.profit_date_range))
                )


        data_X = np.array(data_X)
        data_Y = np.array(data_Y)

        return (data_X,data_Y)

    def get_r2(self):
        data_X,data_Y = self.pre_deal_data()

        data_len = len(data_X)
        i = int(data_len * 0.8)

        train_x = data_X[:i]
        train_y = data_Y[:i]

        test_x = data_X[i:]
        test_y = data_Y[i:]

        models = [
        ('LR',LinearRegression()),
        ('RidgeR',Ridge (alpha = 0.005)),
        ('lasso',Lasso(alpha=0.00001)),
        ('LassoLars',LassoLars(alpha=0.00001)),
        ('RandomForestRegression',RandomForestRegressor(1000))]

        print(data_X,data_Y)

        best_r2 = (0,0,None)
        for m in models:
            m[1].fit(train_x,train_y)
            pred_y = m[1].predict(test_x)
            r2 = r2_score(pred_y,test_y)
            if r2 > best_r2[1]:
                best_r2 = (m[0],r2,m[1])

        print ('the best regression is:',best_r2)

        return best_r2[2]


    def forecast(self):
        model = self.get_r2()
        try_date = datetime.datetime(2017,5,1)

        symbols = self.db.get_symbol_from_db()

        df_list = []

        for ticker in symbols:
            start_date = try_date - datetime.timedelta(days=(self.feature_date_range))
            ticker_data = self.db.get_ticker_by_id(ticker,start_date,try_date)

            if ticker_data.empty :
                continue

            close = ticker_data['close']
            print (close,'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            predict = model.predict(close)
            profit = self.db.get_profit_by_days(ticker,self.profit_date_range,try_date + datetime.timedelta(days=self.profit_date_range))

            if predict > 0:
                df_list.append({
                    'predict': predict,
                    'profit': profit
                    })

        df = pd.DataFrame(df_list)
        print(df.shape)


        print(df[df['profit'] > 0].shape)

        print(df)







if __name__ == '__main__':
    unicon = Unicon_strategy()
    unicon.forecast()