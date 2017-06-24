print ('================== may the force be with you =================')
import quandl
import datetime
import pandas
import json
import pymongo
from pymongo import MongoClient
from db import Database as Database

#us_stock
class US_Database(Database):
    def __init__(self):
        self.client = MongoClient('localhost',27017);
        self.db = self.client.us_ticker_master
        self.daily_price_collection = self.db.daily_price
        self.symbol_collection = self.db.symbol
        self.quandl_key = 'pDHyXjHidqQvhqGWWkMa'
        quandl.ApiConfig.api_key = self.quandl_key

    #the way of quandl to download data is by date not id
    def download_us_ticker_from_quandl_by_date(self,date):
        dateStr = date.strftime('%Y-%m-%d')
        #if the date has already exist, return
        dateList = list(self.daily_price_collection.find({'date': dateStr}))
        if len(dateList) != 0:
            return
        print('downloading the ticker data of %s ...' % date )
        data_df = pandas.DataFrame(quandl.get_table('WIKI/PRICES', date = dateStr))
        data_df['date'] = dateStr
        return data_df

    #save data
    def save_data_into_db(self,data):
        ticker_json = json.loads(data.to_json(orient='records'))
        self.daily_price_collection.insert_many(ticker_json)
        print('save data success!')

    #get the lastest date
    def get_the_last_date_from_db(self):
        dateList = list(self.daily_price_collection.find({'ticker': 'A'}).sort('date', pymongo.DESCENDING))
        last_date_str = dateList[0]['date']
        return datetime.datetime.strptime(last_date,"%Y-%m-%d")


    #get all data until today
    # def download_all_data_until_today(self):
        #



usDb = US_Database()
usDb.get_the_last_date_from_db()



