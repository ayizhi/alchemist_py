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
from util.plot_util import Plot_util
from sklearn.linear_model import Lasso,LinearRegression,Ridge,LassoLars
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation
import sklearn.preprocessing as preprocessing



class Unicon_strategy(Strategy):
    def __init__(self):
        self.target_date = datetime.datetime(2016,3,1)
        self.forecast_date = datetime.datetime(2017,5,1)
        self.feature_date_range = 100
        self.profit_date_range = 3
        self.db = US_Database()
        self.feature_util = Feature_util()

    def pre_deal_data(self):
        symbols = self.db.get_symbol_from_db()

        data_X = [];
        data_Y = [];

        for ticker in symbols:
            print(ticker,'==============================================')

            start_date = self.target_date - datetime.timedelta(days=(self.feature_date_range))
            end_date = self.target_date
            ticker_data = self.db.get_ticker_by_id(ticker,start_date,end_date)

            if ticker_data.empty :
                continue

            profit = self.db.get_profit_by_days(ticker,self.profit_date_range,self.target_date + datetime.timedelta(days=self.profit_date_range))
            data_X.append(np.array(ticker_data['close']))
            data_Y.append(profit)


        data_X = np.array(data_X)
        data_Y = np.array(data_Y)

        return (data_X,data_Y)

    def get_r2(self,X,y):
        #normalize
        X = self.feature_util.normalize(X)
        y = self.feature_util.normalize(y)

        print (X,y)


        train_x,test_x = cross_validation.train_test_split(X,test_size=0.3,random_state=0)
        train_y,test_y = cross_validation.train_test_split(y,test_size=0.3,random_state=0)

        print(train_x.shape,train_y.shape,test_x.shape,test_y.shape)

        models = [
        ('LR',LinearRegression()),
        ('RidgeR',Ridge (alpha = 0.005)),
        ('lasso',Lasso(alpha=0.00001)),
        ('LassoLars',LassoLars(alpha=0.00001)),
        ('RandomForestRegression',RandomForestRegressor(2000))]

        best_r2 = (0,0,None)
        for m in models:
            m[1].fit(train_x,train_y)
            pred_y = m[1].predict(test_x)
            r2 = r2_score(pred_y,test_y)
            if r2 > best_r2[1]:
                best_r2 = (m[0],r2,m[1])

        print ('the best regression is:',best_r2)

        return best_r2[2]


    def forecast(self,model):
        if model == None:
            print('model is None')

        self.forecast_date = datetime.datetime(2017,5,1)
        symbols = self.db.get_symbol_from_db()

        #build a empty list to be a content
        close_list = []
        profit_list = []

        for ticker in symbols:
            start_date = self.forecast_date - datetime.timedelta(days=(self.feature_date_range))
            ticker_data = self.db.get_ticker_by_id(ticker,start_date,self.forecast_date)

            if ticker_data.empty :
                continue

            close = ticker_data['close']
            close_list.append(close)

            profit = self.db.get_profit_by_days(ticker,self.profit_date_range,self.forecast_date + datetime.timedelta(days=self.profit_date_range))
            profit_list.append(profit)

        close_np = np.array(close_list)
        profit_np = np.array(profit_list)

        #normalize
        close_np = self.feature_util.normalize(close_np)
        profit_np = self.feature_util.normalize(profit_np)

        predict_np = model.predict(np.array(close_list))


        print('r2 is: ', r2_score(predict_np,profit_np))

        df = pd.DataFrame({'predict': predict_np, 'profit': profit_np})

        df.loc[df.predict > 0,'predict'] = 1
        df.loc[df.predict < 0,'predict'] = -1

        df.loc[df.profit > 0,'profit'] = 1
        df.loc[df.profit < 0,'profit'] = -1

        print('r2 -1/1 is: ', r2_score(df['predict'],df['profit']))

        return df









if __name__ == '__main__':

    unicon = Unicon_strategy()
    plt = Plot_util()
    #get X,y
    X,y = unicon.pre_deal_data()

    #get the best model
    lm = unicon.get_r2(X,y)

    #get curve
    plt.plot_learning_curve(lm,'learnCurve',X,y)

    #get score
    df = unicon.forecast(lm)
    print(df)
    print('==============')
    print('==============')
    print('==============')
    print(df.loc[(df.predict > 0 and df.profit > 0)])