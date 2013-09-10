'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import unittest
import datetime
from tmsdbfutures import TMSDataBaseFutures
from tmsdbspotfx import TMSDataBaseSpotFX
from trmdbtools import add_trade
from futurestrade import FuturesTrade
from spotfxtrade import SpotFXTrade

class TMSTests(unittest.TestCase):

    def test_create_db(self):
        #self.assertRaises(TypeError, tmsdatabase.TMSDataBase())
        return None
        
    def create_futures_trade(self):
        dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
        FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        self.assertTrue(True)
        
    def create_futures_trade_too_little_year(self):
        dt = datetime.datetime(20, 9, 9, 9, 0, 0)
        FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        self.assertTrue(True)
    
    def cancel_trade(self):
        pass
    
    def modify_trade(self):
        pass
    
    def request_inexisting_trade(self):
        pass
    
    def amend_trade_with_incorrect_trader(self):
        pass
    
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
        
    def create_futures_trade_example(self):
        FuturesTrade.get_trade_example()
        self.assertTrue(True)
        
    def test_add_futures_trade(self):
        add_trade(FuturesTrade.get_trade_example())
        self.assertTrue(True)
    
    
    #def create_spotfx_trade_example(self):
    #    SpotFXTrade.get_trade_example()
        
    
    #def test_add_spotfx_trade(self):
    #    add_trade(SpotFXTrade.get_trade_example())
    
if __name__ == '__main__':
    unittest.main()