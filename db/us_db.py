print ('================== may the force be with you =================')
import quandl
import datetime
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
from db import Database as Database

#us_stock
class US_Database(Database):
    def __init__(self):
        self.client = MongoClient('localhost',27017);
        self.db = self.client.us_ticker_master
        #collection daily_price
        self.daily_price_collection = self.db.daily_price
        #collectiion symbol
        self.symbol_collection = self.db.symbol
        self.quandl_key = 'pDHyXjHidqQvhqGWWkMa'
        quandl.ApiConfig.api_key = self.quandl_key

    #the way of quandl to download data is by date not id
    #because of mongo date bug , we need ture datetime to str
    def download_us_ticker_from_quandl_by_date(self,date):
        dateStr = date.strftime('%Y-%m-%d')
        #if the date has already exist, return
        dateList = list(self.daily_price_collection.find({'date': dateStr}))
        if len(dateList) != 0:
            return
        print('downloading the ticker data of %s ...' % date )
        try:
            data_df = pd.DataFrame(quandl.get_table('WIKI/PRICES', date = dateStr))
        except:
            data_df = pd.DataFrame()
        data_df['date'] = dateStr
        print ('the shape of this data is %s , %s' % (data_df.shape[0],data_df.shape[1]))
        return data_df

    #save data
    def save_data_into_db(self,data):
        ticker_json = json.loads(data.to_json(orient='records'))
        self.daily_price_collection.insert_many(ticker_json)
        print('save data success!')

    #get the lastest date , str to datetime
    def get_the_last_date_from_db(self):
        dateList = list(self.daily_price_collection.find({'ticker': 'A'}).sort('date', pymongo.DESCENDING))
        if len(dateList) == 0:
            return None
        last_date_str = dateList[0]['date']
        return datetime.datetime.strptime(last_date_str,"%Y-%m-%d")



    #get all data until today
    def download_all_data_until_today(self):
        last_date = self.get_the_last_date_from_db()
        end_date = datetime.datetime.today()
        if last_date == None:
            start_date = datetime.datetime(2014,1,1)
        else:
            start_date = last_date
        #get date range list
        date_list = pd.date_range(start=start_date,end=end_date)
        print('downloading data from %s to %s ...' % (start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')))
        for index in range(len(date_list)):
            date = date_list[index]
            ticker_data = self.download_us_ticker_from_quandl_by_date(date)
            if(ticker_data.shape[0] == 0):
                continue
            self.save_data_into_db(ticker_data)





usDb = US_Database()
usDb.download_all_data_until_today()



