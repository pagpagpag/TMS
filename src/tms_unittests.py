#!/usr/bin/env python3

'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1
'''
import unittest
import datetime
from trade_models import FuturesTrade, SpotFXTrade
from db_management import TMSDataBase, DB_CONFIG_DEFAULT
from db_helper import get_db
from checking_tools import IntegrityError


DB_CONFIG_TESTS = {"test_mode": True,
                   "force_clean": True,
                   "verbose": False}


class TMSTests(unittest.TestCase):
    """ we use classes variables to run all the tests with different parameters
        because unittest doesn't take argument
        we want to iterate over all possible trade classes
        so create a new class for each trade class
        base is FuturesTrade, see TMSTestsSpotFX for SpotFXTrade
    """
    trade_class = FuturesTrade
    
    def setUp(self):
        """ request and clean the table before each test"""
        config = DB_CONFIG_TESTS
        self.db = get_db(self.trade_class, config)
        self.db.clean_table()
        
    def tearDown(self):
        """ clean the table after each test"""
        self.db.clean_table()
        
    def test_create_futures_trade_example(self):
        trade_example = self.trade_class.get_trade_example()
        self.assertTrue(isinstance(trade_example, self.trade_class))
        
    def test_create_db(self):
        self.assertTrue(isinstance(get_db(self.trade_class, DB_CONFIG_DEFAULT), TMSDataBase))
 
    def test_create_futures_trade(self):
        if self.trade_class == FuturesTrade:
            dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
            ft = FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
            self.assertTrue(isinstance(ft, self.trade_class))
        
    def test_create_futures_trade_too_little_year(self):
        if self.trade_class == FuturesTrade:
            with self.assertRaises(ValueError):
                dt = datetime.datetime(20, 9, 9, 9, 0, 0)
                FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
    
    def test_request_existing_trade(self):
        trade = self.trade_class.get_trade_example()
        self.db.add_trade(trade)
        self.assertTrue(self.db.select_trade_from_id(1) is not None)
        
    def test_immutability_field_trade(self):
        # we assume a trade always has a price
        with self.assertRaises(IntegrityError): 
            trade = self.trade_class.get_trade_example()
            setattr(trade, "price", 12.4543)
        with self.assertRaises(IntegrityError):
            trade = self.trade_class.get_trade_example()
            trade.__setattr__("price", 12.4543)
        
    def test_integrity_database(self):
        with self.assertRaises(IntegrityError):
            trade = self.trade_class.get_trade_example()
            self.db.add_trade(trade)
            trade_sql = self.db.select_trade_from_id(1)
            setattr(trade_sql, "price", 12.4543)
        
    def test_request_inexisting_trade(self):
        self.assertTrue(self.db.select_trade_from_id(1) is None)
    
    def test_cancel_trade(self):
        error_found = False
        error_found = error_found or (self.db.select_trade_from_id(1) is not None)
        trade = self.trade_class.get_trade_example()
        self.db.add_trade(trade)
        error_found = error_found or (self.db.select_trade_from_id(1) is None)
        self.db.cancel_trade(1)
        error_found = error_found or (self.db.select_trade_from_id(1) is not None)
        self.assertFalse(error_found)
        
    def test_cancel_inexisting_trade(self):
        with self.assertRaises(ValueError):
            self.db.cancel_trade(1)
    
    def test_amend_trade_with_unknown_field(self):
        with self.assertRaises(TypeError):
            trade = self.trade_class.get_trade_example()
            self.db.add_trade(trade)
            self.db.amend_trade_with_field(1, "UNKNOWN", "BLABLA")
        
    def test_amend_trade_with_incorrect_trader(self):
        with self.assertRaises(ValueError):
            trade = self.trade_class.get_trade_example()
            self.db.add_trade(trade)
            self.db.amend_trade_with_field(1, "trader", "John Doe")
    
    def test_amend_trade_with_incorrect_num_contracts(self):
        with self.assertRaises(TypeError):
            trade = self.trade_class.get_trade_example()
            self.db.add_trade(trade)
            self.db.amend_trade_with_field(1, "num_contracts", "pi")
        
    def test_amend_futures_trade_with_incorrect_maturity(self):
        if self.trade_class == FuturesTrade:
            with self.assertRaises(ValueError):
                ft = FuturesTrade.get_trade_example()
                self.db.add_trade(ft)
                self.db.amend_trade_with_field(1, "year", 1999)
        
    def test_amend_trade_with_incorrect_type(self):
        with self.assertRaises(TypeError):
            ft = FuturesTrade.get_trade_example()
            self.db.add_trade(ft)
            spotfxt = SpotFXTrade.get_trade_example()
            self.db.amend_trade_with_trade(1, spotfxt)
        
    def test_amend_futures_trade_with_fields(self):
        if self.trade_class == FuturesTrade:
            ft = FuturesTrade.get_trade_example()
            self.db.add_trade(ft)
            amend_dict = {"price": 1234.56, "num_contracts": 654321}
            self.db.amend_trade_with_fields(1, amend_dict)
            amended_trade_from_db = self.db.select_trade_from_id(1)
            self.assertTrue(amended_trade_from_db.price == 1234.56 and 
                            amended_trade_from_db.num_contracts == 654321)

            
"""
# already defined as the base class
class TMSTestsFutures(TMSTests):
    trade_class = FuturesTrade
"""


class TMSTestsSpotFX(TMSTests):
    trade_class = SpotFXTrade


if __name__ == '__main__':
    unittest.main()