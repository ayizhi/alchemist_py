#coding: utf-8
#数据工具库
import sys
sys.path.append('../..')
from db.cn_db import Database
import numpy as np
import time
from progressbar import *
import pandas as pd
import numpy as np

class DbUtil(Database):
	def get_middle_33_average_volume_tickers(self):
		ticker_list = self.get_ticker_ids_from_db()
		volume_list = np.array([])
		list_len = len(ticker_list)

		print('is calculating average volume...')

		pbar = ProgressBar(maxval=list_len).start()
		for i in range(list_len):
			pbar.update(i+1)
			time.sleep(0.0001)
			ticker = ticker_list.ix[i]
			ticker_id = ticker['code']
			ticker_name = ticker['name']
			volume = self.get_average_volume_by_id(ticker_id,10)
			if volume:
				volume = int(volume)
				volume_list = np.append(volume_list,volume)
		pbar.finish()

		t33 = int(list_len * 0.3333333)
		t66 = int(list_len * 0.6666666)

		volume_list_middle_33 = np.sort(volume_list)[t33: t66]

		volume_range = (volume_list_middle_33[0],volume_list_middle_33[-1])

		return volume_range

	def get_simple_moving_average(self,ticker_id, nDays=5):
		ticker_list = self.get_ticker_data_by_id_from_db(ticker_id)
		date = np.array(ticker_list['date'])
		sma = pd.Series(ticker_list['close']).rolling(window=nDays,center=False).mean()
		sma.index = date
		return sma

