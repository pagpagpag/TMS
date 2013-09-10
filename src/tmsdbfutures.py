'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from sqlalchemy import Column, Integer, String, DateTime, Float
from tmsdb import TMSDataBase
from futurestrade import FuturesTrade

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
    #db = TMSDataBase()
    db = TMSDataBaseFutures()
    ft = FuturesTrade.get_trade_example()
    #db.add_trade(ft)
    #db.add_trade(ft)
    #db.add_trade(ft)
    #db.display_table()
    #db.cancel_trade(42)
    #db.display_table()
    #db.clean_table()
    #db.get_all_table_as_trades()
    print(db.select_trade_from_id(1))
    db.amend_trade_with_trade(1, ft)
    #print(db.select_trade_from_id(1))
    #db.display_table()