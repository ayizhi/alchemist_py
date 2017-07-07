#coding: utf-8

import sklearn
import pandas as pd
import numpy as np
import statsmodels
import sys
sys.path.append('../')
from db.us_db import US_Database
import statsmodels.tsa.stattools as ts
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
	db = US_Database()
	symbols = db.get_symbol_from_db()
	adf_list = []
	for index in range(len(symbols)):
		symbol = symbols[index]
		ticker = db.get_ticker_by_id(symbol,datetime.datetime(2017,1,1))
		if ticker.empty :
			continue
		print(index,len(symbols))
		ticker_close = ticker.close
		adf = ts.adfuller(ticker_close)
		if(adf[0] < adf[4]['1%'] and adf[0] < adf[4]['5%'] and adf[0] < adf[4]['10%']):
			adf_list.append({
				'ticker': ticker,
				'adf': adf
				})
		if index > 100:
			break
		
	df = pd.DataFrame(adf_list)
	tickers = df['ticker']

	for ticker in tickers:
		ticker_data = db.get_ticker_by_id(symbol,datetime.datetime(2017,5,1))
		ticker_close = pd.Series(ticker_data['close'],dtype="float64")
		ticker_date = pd.Series(ticker_data.index,name='date')
		print(ticker_date)
		data = pd.DataFrame({'close': ticker_close}).reset_index()
		index = pd.Series(np.arange(0,data.shape[0]),name='x')
		data = data.join(index)

		print(index,'----')
		# data.close = ticker_close
		# data.date = ticker_date
		print(  data)
		# print(ticker_data.index.strftime('%Y-%m-%d'))
		sns.jointplot(x='x',y='close',data = data[['x','close']])
		sns.plt.show()
		break

