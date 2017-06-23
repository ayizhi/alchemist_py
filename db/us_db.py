print ('================== may the force be with you =================')
import quandl
import datetime
import pandas
import json
from pymongo import MongoClient
from db import Database as Database

#us_stock
class US_Database(Database):
    def __init__(self):
        self.client = MongoClient('localhost',27017);
        self.db = self.client.us_ticker_master
        self.quandl_key = 'pDHyXjHidqQvhqGWWkMa'
        quandl.ApiConfig.api_key = self.quandl_key

    #the way of quandl to download data is by date not id
    def download_us_ticker_from_quandl_by_date(self,date):
        print('downloading the ticker data of %s ...' % date )
        data_df = pandas.DataFrame(quandl.get_table('WIKI/PRICES', date = date))
        return data_df

    #save data
    def save_data_into_db(self,data):
        ticker_json = json.loads(data.to_json(orient='records'))
        collection = self.db.daily_price
        collection.insert_many(ticker_json)
        print('save data success!')



date = datetime.date.today() + datetime.timedelta(days = 3 * -1)
data = US_Database().download_us_ticker_from_quandl_by_date(date)
US_Database().save_data_into_db(data)