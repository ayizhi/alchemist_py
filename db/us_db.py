print ('================== may the force be with you =================')
import sys
sys.path.append('./db/')
import quandl
import datetime
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
from db_base import Database as Database

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
            return pd.DataFrame()
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

    #get symbol id from db
    def get_symbol_from_db(self):
        date = datetime.datetime(2016,6,23).strftime('%Y-%m-%d')
        ticker_data_by_date = pd.DataFrame(list(self.daily_price_collection.find({'date': date})))
        return ticker_data_by_date['ticker']

    #save ticker id into symbol
    def save_ticker_into_symbol(self):
        tickers = pd.DataFrame(self.get_all_symbol_from_db())
        tickers_json = json.loads(tickers.to_json(orient='records'))
        #delete first
        self.symbol_collection.delete_many({})
        self.symbol_collection.insert_many(tickers_json)
        print ('save into db success!')

    #get ticker by id
    def get_ticker_by_id(self,ticker_id,start_date=datetime.datetime(2016,5,1),end_date=datetime.datetime.today()):
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        date_range = {'$gte': start_date,'$lt': end_date}
        ticker_data = self.daily_price_collection.find({'ticker': ticker_id,'date': date_range})
        ticker_data_df = pd.DataFrame(list(ticker_data))

        if ticker_data_df.empty != True:
            ticker_data_df = ticker_data_df[['adj_close','adj_high','adj_low','adj_open','volume']].set_index(ticker_data_df['date'])
            return ticker_data_df
        else:
            return pd.DataFrame()

    #get 33%-66% volume by day range
    def get_33_66_volume_by_day_symbol(self,days,target_date=datetime.datetime.today()):
        end_date = target_date.strftime('%Y-%m-%d')
        start_date = (target_date + datetime.timedelta(days = -1 * days)).strftime('%Y-%m-%d')
        date_range = {'$gte': start_date,'$lt': end_date}
        date_range_df = pd.date_range(start=start_date,end=end_date)
        ticker_data = self.daily_price_collection.find({'date': date_range})
        ticker_data_df = pd.DataFrame(list(ticker_data))
        #set val for content to fill volume
        all_volume_df = pd.DataFrame(columns=['volume'])
        for date in date_range_df:
            date = date.strftime('%Y-%m-%d')
            df_by_date = ticker_data_df[ticker_data_df['date'] == date][['ticker','date','volume']]
            df_by_date = df_by_date.reset_index().fillna(method='ffill')
            df_by_date = df_by_date.set_index(df_by_date['ticker'])
            if df_by_date.shape[0] == 0:
                continue
            all_volume_df['volume'] = df_by_date['volume'] if all_volume_df.empty else all_volume_df['volume'] + df_by_date['volume']
            all_volume_df = all_volume_df.fillna(method='ffill')
        #sort
        all_volume_df = all_volume_df.sort(['volume'])
        #cut
        cut_start = int(all_volume_df.shape[0] * 0.33)
        cut_end = int(all_volume_df.shape[0] * 0.66)
        filter_symbol_list = all_volume_df[cut_start:cut_end].index
        return filter_symbol_list

    #get moving average price
    def get_moving_average_price(self,ticker_id,day_range,k_days,target_date=datetime.datetime.today()):
        end_date = target_date
        start_date = (target_date + datetime.timedelta(days = - 1 * (day_range + k_days)))
        date_range = pd.date_range(start=start_date,end=end_date).strftime('%Y-%m-%d')
        #get ma
        ticker_data = self.get_ticker_by_id(ticker_id,start_date,end_date)
        if ticker_data.shape[0] == 0 :
            return pd.DataFrame()
        ticker_data = ticker_data.reindex(date_range).fillna(method="ffill").fillna(method='bfill')
        ticker_data_ma = pd.DataFrame(columns=['adj_close','volume'])
        ticker_data_ma['adj_close'] = ticker_data['adj_close'].rolling(window=k_days,center=False).mean().dropna()
        ticker_data_ma['volume'] = ticker_data['volume']
        return ticker_data_ma

    #get profit
    def get_profit_by_days(self,ticker_id,days,target_date=datetime.datetime.today()):
        end_date = target_date
        start_date = (target_date + datetime.timedelta(days = - 1 * days))
        date_range = pd.date_range(start=start_date,end=end_date).strftime('%Y-%m-%d')
        #get ma
        ticker_data = self.get_ticker_by_id(ticker_id,start_date,end_date)
        ticker_data = ticker_data.reindex(date_range).fillna(method="ffill").fillna(method='bfill')
        if ticker_data.empty == True:
            return 0
        profit = ticker_data['adj_close'][-1] - ticker_data['adj_close'][0]
        return profit




if __name__ == '__main__':
    db = US_Database()
    # db.download_all_data_until_today()

