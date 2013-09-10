'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from sqlalchemy import Column, Integer, String, DateTime, Float
from trade_models import FuturesTrade, SpotFXTrade
from db_management import TMSDataBase

class TMSDataBaseFutures(TMSDataBase):
    """ sql db info for futures"""
    def _define_trade_class(self):
        self.trade_class = FuturesTrade
        
    def _get_columns_sql(self):
        """ from FUTURES_TRADE_VARIABLES_NAMES"""
        return (Column('id', Integer, primary_key=True),
                Column('datetime', DateTime),
                Column('symbol', String),
                Column('month', Integer),
                Column('year', Integer),
                Column('num_contracts', Integer),
                Column('price', Float),
                Column('trader', String)
                )

    
class TMSDataBaseSpotFX(TMSDataBase):
    """ sql db info for spot fx"""
    def _define_trade_class(self):
        self.trade_class = SpotFXTrade
    
    def _get_columns_sql(self):
        """ from SPOTFX_TRADE_VARIABLES_NAMES"""
        return (Column('id', Integer, primary_key=True),
                Column('datetime', DateTime),
                Column('currency_pair', String),
                Column('size', Float),
                Column('price', Float),
                Column('trader', String)
                )
        
if __name__ == '__main__':
    ft = FuturesTrade.get_trade_example()
    print(ft.__str__())
    db = TMSDataBaseSpotFX()
    print(db.get_all_table_as_trades())