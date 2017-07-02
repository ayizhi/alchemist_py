#coding: utf-8
#数据工具库
import sys
sys.path.append('../..')
import numpy as np
import time
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier


class Feature_util(object):
		#CCI
	def CCI(self,data,ndays):
		TP = (data['high'] + data['low'] + data['close'])/3
		CCI = pd.Series((TP - pd.rolling_mean(TP, ndays)) / (0.015 * pd.rolling_std(TP, ndays)),name='CCI')
		data = data.join(CCI)
		return data

	#timeLag
	def TL(self,data,ndays):
		index = data.index
		pH = data['high'].resample(str(ndays) + 'D').max().reindex(index).fillna(method='bfill')
		pL = data['low'].resample(str(ndays) + 'D').max().reindex(index).fillna(method='bfill')
		pO = data['open'] - data['open'].shift(1)
		timeLag = pO/(pH - pL)
		timeLag.name = 'TL'
		data = data.join(timeLag)
		return data


	#Ease of Movement
	def EVM(self,data,ndays):
		dm = ((data['high'] + data['low'])/2) - ((data['high'].shift(1) + data['low'].shift(1))/2)
		br = (data['volume']/100000000)/((data['high'] - data['low']))
		EVM = dm/br
		EVM_MA = pd.Series(pd.rolling_mean(EVM,ndays),name='EVM')
		data = data.join(EVM_MA)
		return data

	# Simple Moving Average
	def SMA(self,data, ndays):
		SMA = pd.Series(pd.rolling_mean(data['close'], ndays), name = 'SMA')
		data = data.join(SMA)
		return data

	# Exponentially-weighted Moving Average
	def EWMA(self,data, ndays):
		EMA = pd.Series(pd.ewma(data['close'], span = ndays, min_periods = ndays - 1),
		name = 'EWMA_' + str(ndays))
		data = data.join(EMA)
		return data


	# Rate of Change (ROC)
	def ROC(self,data,n):
		N = data['close'].diff(n)
		D = data['close'].shift(n)
		ROC = pd.Series(N/D,name='Rate of Change')
		data = data.join(ROC)
		return data

	# Force Index
	def ForceIndex(self,data, ndays):
		FI = pd.Series(data['close'].diff(ndays) * data['volume'], name = 'ForceIndex')
		data = data.join(FI)
		return data

	# Compute the Bollinger Bands
	def BBANDS(self,data, ndays):
		MA = pd.Series(pd.rolling_mean(data['close'], ndays))
		SD = pd.Series(pd.rolling_std(data['close'], ndays))
		b1 = MA + (2 * SD)
		B1 = pd.Series(b1, name = 'Upper BollingerBand')
		b2 = MA - (2 * SD)
		B2 = pd.Series(b2, name = 'Lower BollingerBand')
		data = data.join([B1,B2])
		return data

	#find most important 10 feature
	def find_most_important_feature(self,data_x,data_y,feature_num,n_estimators,random_state=0):
		#build a forest and compute the feature importance
		forest = ExtraTreesClassifier(n_estimators=n_estimators,random_state=random_state)
		forest.fit(data_x, data_y)
		importances = forest.feature_importances_
		std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
		indices = np.argsort(importances)[::-1]

		#Print the feature ranking
		print("Feature ranking:")

		x_columns = data_x.columns
		features = []
		for f in range(data_x.shape[1]):
			features.append(x_columns[int(indices[f])])
			print (f,indices[f],x_columns[int(indices[f])],'===========', importances[indices[f]])
		return features






