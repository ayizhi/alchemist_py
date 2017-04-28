#coding: utf-8
#数据工具库
import sys
sys.path.append('../..')
from db.cn_db import Database
import numpy as np
import time
from progressbar import *

class DbUtil(Database):
	def get_middle_33_average_volume_tickers(self):
		ticker_list = self.get_ticker_ids_from_db()
		volume_list = np.array([])
		list_len = len(ticker_list)

		pbar = ProgressBar(maxval=list_len).start()
		for i in range(list_len):
			pbar.update(i+1)
			time.sleep(0.0001)
			ticker = ticker_list.ix[i]
			ticker_id = ticker['code']
			ticker_name = ticker['name']
			volume = self.get_average_volume_by_id(ticker_id,10)
			print (ticker_id,ticker_name,volume,'===')
			volume_list = np.append(volume_list,volume)
		pbar.finish()

		t33 = int(list_len * 0.3333333)
		t66 = int(list_len * 0.6666666)

		volume_list_middle_33 = np.sort(volume_list)[t33: t66]
		return volume_list_middle_33

	def get_k(ticker_id, nDays=5):
		ticker_list = list(self.get_ticker_data_by_id_from_db(ticker_id))


dbUtil = DbUtil()
dbUtil.get_middle_33_average_volume_tickers()