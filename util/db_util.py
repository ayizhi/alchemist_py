#coding: utf-8
import sys
sys.path.append('../..')
from db.cn_db import Database
import numpy as np
import time
from progressbar import *

class DbUtil(Database):
	def get_middle_33_average_volume_tickers(self):
		ticker_list = list(self.get_ticker_ids_from_db())
		volume_list = np.array([])
		list_len = len(ticker_list)
		pbar = ProgressBar(maxval=list_len).start()
		for i in range(len(ticker_list)):
			pbar.update(i+1)
			time.sleep(0.0001)
			
			ticker = ticker_list[i]
			ticker_id = ticker['code']
			ticker_name = ticker['name']
			volume = self.get_average_volume_by_id(ticker_id,10)
			volume_list = np.append(volume_list,volume)
		pbar.finish()

		t33 = int(list_len * 0.3333333)
		t66 = int(list_len * 0.6666666)

		volume_list_middle_33 = np.sort(volume_list)[t33: t66]
		print volume_list_middle_33
		return volume_list_middle_33




dbUtil = DbUtil()

dbUtil.get_middle_33_average_volume_tickers()