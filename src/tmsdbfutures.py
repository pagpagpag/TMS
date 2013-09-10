'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from src.tmsdb import TMSDataBase
from src.futurestrade import FuturesTrade
from sqlalchemy import Column, Integer, String, DateTime, Float

class TMSDataBaseFutures(TMSDataBase):
    
    def _define_trade_class(self):
        self.trade_class = FuturesTrade
        
    def _get_columns_sql(self):
        return (Column('id', Integer, primary_key=True),
                Column('datetime', DateTime),
                Column('symbol', String),
                Column('month', Integer),
                Column('year', Integer),
                Column('num_contracts', Integer),
                Column('price', Float),
                Column('trader', String)
                )

if __name__ == '__main__':
    db = TMSDataBaseFutures()
    print(db.get_all_table_as_trades())