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


#检测是不是均值回归形，如果是，则价格高于均值价格会下降，否则，价格会上升
def get_adf(symbols,db,date=datetime.datetime(2017,1,1)):
	adf_list = []
	for index in range(len(symbols)):
		symbol = symbols[index]
		ticker = db.get_ticker_by_id(symbol,date)
		if ticker.empty :
			continue
		ticker_close = ticker.close
		adf = ts.adfuller(ticker_close)
		if(adf[0] < adf[4]['1%'] and adf[0] < adf[4]['5%'] and adf[0] < adf[4]['10%']):
			adf_list.append({
				'ticker': ticker,
				'adf': adf[0]
				})
		if index > 500:
			break

	df = pd.DataFrame(adf_list)
	tickers = df['ticker']
	return tickers

#hurst，等于0.5，随机游走
#>0.5均值回归
#<0.5趋势性
def get_hurst(ticker_id,db,days=100,target_date=datetime.datetime.today()):
	daily_return = db.get_pct_change(ticker_id,days,target_date)
	if daily_return.empty:
		return 0.5
	else:
		daily_return = daily_return['pct'][1:]
	ranges = ['1','2','4','8','16','32']
	lag = pd.Series(index = ranges)
	for i in range(len(ranges)):
		if i == 0:
			lag[i] = len(daily_return)
		else:
			lag[i] = lag[0] // (2 ** i)


	ARS = pd.Series(index = ranges)

	for r in ranges:
		RS = list()
		for i in range(int(r)):
			Range = daily_return[int(i * lag[r]): int((i + 1) * lag[r])]
			mean = np.mean(Range)
			Deviation = Range / mean
			maxi = max(Deviation)
			mini = min(Deviation)
			RS.append(maxi - mini)
			sigma = np.std(Range)

		ARS[r] = np.mean(RS[~np.isnan(RS)])

	lag = np.log10(lag)
	ARS = np.log10(ARS)
	hurst_exponent = np.polyfit(lag,ARS,1)
	hurst = hurst_exponent[0] * 2

	return hurst

if __name__ == '__main__':
	db = US_Database()
	symbols = db.get_symbol_from_db()
	# get_adf(symbols,db,datetime.datetime(2017,5,1))
	hurst_list = []
	for i in range(len(symbols)):
		symbol = symbols[i]
		hurst = get_hurst(symbol,db)
		print(i,hurst)
		hurst_list.append({
			'ticker': symbol,
			'hurst': hurst
			})


	df = pd.DataFrame(hurst_list).dropna()

	sns.distplot(df['hurst'])
	sns.plt.show()

	df2 = df.loc[df['hurst'] < -10]

	for i in df2:
		symbol = df2[i]['ticker']
		data = db.get_pct_change(me)
	print (df2)



