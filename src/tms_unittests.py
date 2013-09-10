'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import unittest
import datetime
from trade_models import FuturesTrade, SpotFXTrade
from db_models import TMSDataBaseFutures
from db_tools import add_futures_trade
from src.db_models import TMSDataBaseSpotFX

class TMSTests(unittest.TestCase):

    def test_create_db_futures(self):
        TMSDataBaseFutures()
    
    def test_create_db_spotfx(self):
        TMSDataBaseSpotFX()
     
    def create_futures_trade(self):
        dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
        FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        #self.assertTrue(True)
        
    def create_futures_trade_too_little_year(self):
        dt = datetime.datetime(20, 9, 9, 9, 0, 0)
        FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        #self.assertTrue(True)
    
    def cancel_trade(self):
        error_found = True
        db = TMSDataBaseFutures()
        db.clean_table()
        error_found = error_found or (db.select_trade_from_id(1) is not None)
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        error_found = error_found or (db.select_trade_from_id(1) is None)
        db.cancel_trade(1)
        error_found = error_found or (db.select_trade_from_id(1) is not None)
        self.assertFalse(error_found)
    
    """
    def modify_trade(self):
        pass
    
    def request_inexisting_trade(self):
        pass
    
    def amend_trade_with_incorrect_trader(self):
        pass
    """
    def amend_trade_with_incorrect_num_contracts(self):
        db = TMSDataBaseFutures()
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        db.amend_trade_with_field(1, "num_contracts", "pi")
        #self.assertRaises()
    
    def amend_trade_with_incorrect_maturity(self):
        db = TMSDataBaseFutures()
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        db.amend_trade_with_field(1, "num_contracts", "pi")
        #self.assertRaises()
    
    def amend_trade_with_incorrect_type(self):
        db = TMSDataBaseFutures()
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        spotfxt = SpotFXTrade.get_trade_example()
        db.amend_trade_with_trade(1, spotfxt)
        #self.assertRaises()
        
    def amend_trade_with_fields(self):
        db = TMSDataBaseFutures()
        db.clean_table(True)
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        amend_dict = {"price": "", "num_contracts": 654321}
        db.amend_trade_with_fields(1, amend_dict)
        amended_trade_from_db = db.select_trade_from_id(1)
        self.assertTrue(amended_trade_from_db.price == 1234.56 and 
                        amended_trade_from_db.num_contracts == 654321)
        
    def create_futures_trade_example(self):
        FuturesTrade.get_trade_example()
        self.assertTrue(True)
        
    def test_add_futures_trade(self):
        add_futures_trade(FuturesTrade.get_trade_example())
        self.assertTrue(True)
    
    
    #def create_spotfx_trade_example(self):
    #    SpotFXTrade.get_trade_example()
        
    
    #def test_add_spotfx_trade(self):
    #    add_trade(SpotFXTrade.get_trade_example())
    
if __name__ == '__main__':
    unittest.main()