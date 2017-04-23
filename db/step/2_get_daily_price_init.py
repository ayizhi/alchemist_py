#coding: utf-8
import sys
sys.path.append('..')
from cn_db import Database
from pprint import pprint

if __name__ == '__main__':
	Db = Database()
	tickers = Db.get_ticker_ids_from_db()
	total = tickers.count()
	i = 0
	for ticker in tickers:
		i = i + 1
		print (i,total)

		ticker_id = ticker['code']
		ticker_name = ticker['name']
		Db.save_data_into_db_by_id(ticker_id)

		print (ticker_id,ticker_name)

