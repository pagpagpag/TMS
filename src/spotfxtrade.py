'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import datetime
from src.trade import Trade
from src.checking_tools import typecheck, trader_check, currency_pair_check,\
    datetime_check

SPOT_FX_TRADE_VARIABLES_NAMES = ["id", "datetime", "symbol", "currency_pair",
                                 "size", "price", "trader"]

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
    spotfxt = SpotFXTrade.get_spot_fx_trade_example()
    #print(spotfxt.__dict__)
    #print(spotfxt.to_string())
    print(SpotFXTrade.__init__)