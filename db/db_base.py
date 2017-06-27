from abc import ABCMeta, abstractmethod

#base class
class Database(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def save_ticker_names_into_db(self):
        raise NotImplementedError('should implement save_ticker_names_into_db')

    @abstractmethod
    def get_ticker_ids_from_db(self):
        raise NotImplementedError('should implement get_ticker_ids_from_db')

    @abstractmethod
    def get_ticker_data_by_id_from_db(self):
        raise NotImplementedError('should implement get_ticker_data_by_id_from_db')