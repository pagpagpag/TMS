'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import datetime
from src.trade import Trade
from src.checking_tools import typecheck, trader_check, symbol_check, year_check,\
    month_check, datetime_check

FUTURES_TRADE_VARIABLES_NAMES = ["id", "datetime", "symbol", "month", 
                                 "year", "num_contracts", "price", "trader"]

class FuturesTrade(Trade, tuple):
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
        return tuple.__new__(cls, (id, datetime, symbol, month, year, num_contracts, price, trader))
    
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
    
if __name__ == '__main__':
    dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
    ft = FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
    print(type, ft)
    print(ft.get_variables_dict())