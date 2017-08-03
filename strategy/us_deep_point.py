#coding: utf-8
#火炉底架
import sys
sys.path.append('../')
from db.us_db import US_Database
import numpy as np
import pandas as pd
import datetime
from strategy_base import Strategy
import sklearn
from sklearn import linear_model
from util.plot_util import Plot_util
from util.test_util import Test_util
import statsmodels.tsa.stattools as ts
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import seaborn as sns

class Deep_point_strategy(Strategy):
    def __init__(self):
        self.date_range = 15
        self.lr_range = 70
        self.db = US_Database()

    def deal_data(self,symbol):
        #find the biggest drop around 10 days
        start_date = datetime.datetime.today() - datetime.timedelta(self.date_range)
        ticker_data = self.db.get_ticker_by_id_not_consecutive_date(symbol,start_date=start_date).reset_index()
        ticker_data['delta'] = ticker_data['close'] - ticker_data['open']
        ticker_data['delta_pc'] = (ticker_data['close'] - ticker_data['open']) * 100 / ticker_data['open']

        if not ticker_data[ticker_data['delta_pc'] > 6].empty:
            #then we need to confirm the trend of drop
            pre_start_date = datetime.datetime.today()
            pre_target_date = pre_start_date - datetime.timedelta(days=self.lr_range)
            pre_ticker_data = self.db.get_ticker_by_id_not_consecutive_date(symbol,start_date=pre_target_date).reset_index()
            X_train = np.array(pre_ticker_data.index)
            y_train = np.array(pre_ticker_data.close)
            xx = np.linspace(0,pre_ticker_data.index[-1],100)
            
            quadratic_featurizer = PolynomialFeatures(degree=2)
            X_train_quadratic = quadratic_featurizer.fit_transform(X_train.reshape(X_train.shape[0],1))
            regressor_quadratic = LinearRegression()
            regressor_quadratic.fit(X_train_quadratic, y_train)

            xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1))
            yy_quadratic = regressor_quadratic.predict(xx_quadratic)

            # y = ax2 + bx + c
            coef_ = regressor_quadratic.coef_
            a = coef_[-1]
            b = coef_[1]
            # 我们想让导数为零的点在今天附近或者之后,且二次函数a为正
            # 导数为零点
            d_p = (b * -1) / (2 * a)
            d_range = len(X_train)
            if a > 0 and (d_p > d_range - 10 and d_p < d_range + 10):
                print (symbol, d_p, d_range)
                df_predict_quadratic = pd.DataFrame({'x': xx, 'y': yy_quadratic})
                sns.jointplot('x','y',df_predict_quadratic[['x','y']],kind = 'scatter',color='blue')
                sns.plt.show()

                #判断有大跌
                deep_index = ticker_data[ticker_data['delta_pc'] > 4].index[-1]
                if deep_index <= 2:
                    #volume is so few and the change of price after deep is slience
                    print(ticker_data.iloc[deep_index : ])





if __name__ == '__main__':
    db = US_Database()
    symbols = db.get_33_66_volume_by_day_symbol(20)
    dp = Deep_point_strategy()
    #loop
    # symbols.map(lambda x: dp.deal_data(x))
    for index in range(len(symbols)):
        # if index > 100 :
        #     break
        symbol = symbols[index]
        dp.deal_data(symbol)