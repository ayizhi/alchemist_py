# -*- coding:utf-8 -*- 
import sys
sys.path.append('..')
from cn_db import Database
from pprint import pprint

if __name__ == '__main__':
	Db = Database()
	tickers = Db.get_ticker_ids_from_db()
	length = len(tickers)

	for i in range(length):
		i = i + 1
		ticker = tickers.ix[i]
		print  (i,length)
		ticker_id = ticker['code']
		ticker_name = ticker['name']
		Db.save_data_into_db_by_id_until_today(ticker_id)


