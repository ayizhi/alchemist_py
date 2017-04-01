#coding: utf-8
import sys
sys.path.append('..')
from db.cn_db import Database

class DbUtil(Database):
	def get_middle_33_average_volume_tickers(self):
		ticker_list = list(self.get_ticker_ids_from_db())
		volume_list = []
		for i in range(len(ticker_list)):
			print i , len(ticker_list),'======'
			ticker = ticker_list[i]
			ticker_id = ticker['code']
			ticker_name = ticker['name']
			volume = self.get_average_volume_by_id(ticker_id,10)
			volume_list.append(volume)
		volume_list = volume_list.sort()
		print volume_list




dbUtil = DbUtil()

dbUtil.get_middle_33_average_volume_tickers()