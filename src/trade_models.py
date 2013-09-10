'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import datetime
from abc import abstractmethod, ABCMeta
from checking_tools import typecheck, trader_check, symbol_check, year_check,\
    month_check, datetime_check, currency_pair_check


FUTURES_TRADE_VARIABLES_NAMES = ["id", "datetime", "symbol", "month", 
                                 "year", "num_contracts", "price", "trader"]
SPOT_FX_TRADE_VARIABLES_NAMES = ["id", "datetime", "currency_pair",
                                 "size", "price", "trader"]


class Trade(tuple):
    """ abstract class for trade object"""
    __metaclass__ = ABCMeta
    
    @staticmethod
    @abstractmethod
    def get_variables_names():
        """ define the variables"""
        raise TypeError("Cannot instantiate Trade abstract class")
    
    def __setattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        return NotImplemented

    def __delattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        return NotImplemented
    
    def __str__(self):
        variables_names = self.get_variables_names()
        return ", ".join(name + ": " + str(getattr(self, name)) 
                         for name in variables_names)
        
    def get_variables_dict(self):
        params = self.get_variables_names()
        return {param: getattr(self, param) for param in params}
    
    def get_variables_dict_no_id(self):
        variables_dict = self.get_variables_dict()
        return {var: variables_dict[var] for var in variables_dict
                                    if var != "id"}
        

class FuturesTrade(Trade):
    """
    Futures trades
    defined as (id, datetime, symbol, month, year, num_contracts, price, trader).
    E.g., a sell of -15 Dec 13 bund contracts at 137.52 might be represented as 
    (id00001, 2013-09-09 09:00:00, RX, 12, 2013, -15, 137.52, pierre).
    """
    @typecheck
    def __new__(cls,
                id: int, 
                datetime: datetime,
                symbol: str,
                month: int,
                year: int,
                num_contracts: int,
                price: float,
                trader: str):
        datetime_check(datetime)
        symbol_check(symbol)
        month_check(month)
        year_check(year)
        trader_check(trader)
        return tuple.__new__(cls, 
            (id, datetime, symbol, month, year, num_contracts, price, trader))
    
    @staticmethod
    def get_variables_names():
        """ more robust"""
        return FUTURES_TRADE_VARIABLES_NAMES
    
    @property
    def id(self):
        return self[0]

    @property
    def datetime(self):
        return self[1]
    
    @property
    def symbol(self):
        return self[2]

    @property
    def month(self):
        return self[3]
    
    @property
    def year(self):
        return self[4]

    @property
    def num_contracts(self):
        return self[5]
    
    @property
    def price(self):
        return self[6]

    @property
    def trader(self):
        return self[7]
        
    @staticmethod
    def get_trade_example():
        dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
        return FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        

class SpotFXTrade(Trade):
    """
    Spot FX trades, 
    defined as (id, datetime, currency pair, size, price, trader).
    E.g., a buy of 1 million AUDUSD at 0.9205 would be represented as
    (id00002, 2013-09-09 09:00:00, AUDUSD, 1000000, 0.9205, damien).
    """
    @typecheck
    def __new__(cls,
                id: int,
                datetime: datetime,
                currency_pair: str, 
                size: float,
                price: float,
                trader: str):
        datetime_check(datetime)
        currency_pair_check(currency_pair)
        trader_check(trader)
        return tuple.__new__(cls, (id, datetime, currency_pair, size, price, trader))
    
    @staticmethod
    def get_variables_names():
        """ more robust"""
        return SPOT_FX_TRADE_VARIABLES_NAMES
    
    @property
    def id(self):
        return self[0]

    @property
    def datetime(self):
        return self[1]
    
    @property
    def currency_pair(self):
        return self[2]

    @property
    def size(self):
        return self[3]
    
    @property
    def price(self):
        return self[4]

    @property
    def trader(self):
        return self[5]
    
    @staticmethod    
    def get_trade_example():
        dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
        return SpotFXTrade(-1, dt, "AUDUSD", 1000000.0, 0.9205, "damien")
    
    
if __name__ == '__main__':
    dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
    ft = FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
    print(type, ft)
    print(ft.get_variables_dict())
    
    spotfxt = SpotFXTrade.get_trade_example()
    #print(spotfxt.__dict__)
    #print(spotfxt.to_string())
    print(spotfxt)