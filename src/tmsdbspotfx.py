'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from src.tmsdb import TMSDataBase
from src.spotfxtrade import SpotFXTrade
from sqlalchemy import Column, Integer, String, DateTime, Float

class TMSDataBaseSpotFX(TMSDataBase):
    
    def _define_trade_class(self):
        self.trade_class = SpotFXTrade
    
    def _get_columns_sql(self):
        return (Column('id', Integer, primary_key=True),
                Column('datetime', DateTime),
                Column('currency_pair', String),
                Column('size', Float),
                Column('price', Float),
                Column('trader', String)
                )
        
if __name__ == '__main__':
    db = TMSDataBaseSpotFX()
    print(db.get_all_table_as_trades())