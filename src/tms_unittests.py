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
from db_models import TMSDataBaseFutures, TMSDataBaseSpotFX
from db_management import TMSDataBase, TEST_MODE_DEFAULT
from checking_tools import IntegrityError

class TMSTests(unittest.TestCase):
    
    def test_create_futures_trade_example(self):
        ft_example = FuturesTrade.get_trade_example()
        self.assertTrue(isinstance(ft_example, FuturesTrade))
        
    def test_create_spotfx_trade_example(self):
        spotfx_example = SpotFXTrade.get_trade_example()
        self.assertTrue(isinstance(spotfx_example, SpotFXTrade))
    
    def test_create_db_futures(self):
        self.assertTrue(isinstance(TMSDataBaseFutures(TEST_MODE_DEFAULT), TMSDataBase))

    def test_create_db_spotfx(self):
        self.assertTrue(isinstance(TMSDataBaseSpotFX(TEST_MODE_DEFAULT), TMSDataBase))
     
    def test_create_futures_trade(self):
        dt = datetime.datetime(2013, 9, 9, 9, 0, 0)
        ft = FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        self.assertTrue(isinstance(ft, FuturesTrade))
        
    def test_create_futures_trade_too_little_year(self):
        dt = datetime.datetime(20, 9, 9, 9, 0, 0)
        ft = FuturesTrade(-1, dt, "RX", 12, 2013, -15, 137.52, "pierre")
        self.assertTrue(isinstance(ft, FuturesTrade))
    
    def test_request_existing_trade(self):
        db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
        db.clean_table(force_clean=True, verbose=False)
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        self.assertTrue(db.select_trade_from_id(1) is not None)
        
    def test_immutability_field_trade(self):
        def test_immutability_field_trade_setattr1():
            ft = FuturesTrade.get_trade_example()
            setattr(ft, "price", 12.4543)
        def test_immutability_field_trade_setattr2():
            ft = FuturesTrade.get_trade_example()
            ft.__setattr__("price", 12.4543)
        self.assertRaises(IntegrityError, test_immutability_field_trade_setattr1)
        self.assertRaises(IntegrityError, test_immutability_field_trade_setattr2)
        
    def test_integrity_database(self):
        def test_integrity_database_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            db.clean_table(force_clean=True, verbose=False)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            ft_sql = db.select_trade_from_id(1)
            setattr(ft_sql, "price", 12.4543)
        self.assertRaises(IntegrityError, test_integrity_database_annex)
        
    def test_request_inexisting_trade(self):
        db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
        db.clean_table(force_clean=True, verbose=False)
        self.assertTrue(db.select_trade_from_id(1) is None)
    
    def test_cancel_trade(self):
        error_found = False
        db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
        db.clean_table(force_clean=True, verbose=False)
        error_found = error_found or (db.select_trade_from_id(1) is not None)
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        error_found = error_found or (db.select_trade_from_id(1) is None)
        db.cancel_trade(1)
        error_found = error_found or (db.select_trade_from_id(1) is not None)
        self.assertFalse(error_found)
        
    def test_cancel_inexisting_trade(self):
        def test_cancel_inexisting_trade_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            db.clean_table(force_clean=True, verbose=False)
            db.cancel_trade(1)
        self.assertRaises(ValueError, test_cancel_inexisting_trade_annex)
    
    def test_amend_trade_with_unknown_field(self):
        def test_amend_trade_with_unknown_field_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            db.clean_table(force_clean=True, verbose=False)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            db.amend_trade_with_field(1, "UNKNOWN", "pi")
        self.assertRaises(TypeError, test_amend_trade_with_unknown_field_annex)
        
    def test_amend_trade_with_incorrect_trader(self):
        def test_amend_trade_with_incorrect_trader_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            db.clean_table(force_clean=True, verbose=False)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            db.amend_trade_with_field(1, "trader", "John Doe")
        self.assertRaises(ValueError, test_amend_trade_with_incorrect_trader_annex)
    
    def test_amend_trade_with_incorrect_num_contracts(self):
        def test_amend_trade_with_incorrect_num_contracts_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            db.amend_trade_with_field(1, "num_contracts", "pi")
        self.assertRaises(TypeError, test_amend_trade_with_incorrect_num_contracts_annex)
    
    def test_amend_trade_with_incorrect_maturity(self):
        def test_amend_trade_with_incorrect_maturity_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            db.amend_trade_with_field(1, "year", 1999)
        self.assertRaises(ValueError, test_amend_trade_with_incorrect_maturity_annex)
    
    def test_amend_trade_with_incorrect_type(self):
        def test_amend_trade_with_incorrect_type_annex():
            db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
            ft = FuturesTrade.get_trade_example()
            db.add_trade(ft)
            spotfxt = SpotFXTrade.get_trade_example()
            db.amend_trade_with_trade(1, spotfxt)
        self.assertRaises(TypeError, test_amend_trade_with_incorrect_type_annex)
        
    def test_amend_trade_with_fields(self):
        db = TMSDataBaseFutures(TEST_MODE_DEFAULT)
        db.clean_table(True, verbose=False)
        ft = FuturesTrade.get_trade_example()
        db.add_trade(ft)
        amend_dict = {"price": 1234.56, "num_contracts": 654321}
        db.amend_trade_with_fields(1, amend_dict)
        amended_trade_from_db = db.select_trade_from_id(1)
        self.assertTrue(amended_trade_from_db.price == 1234.56 and 
                        amended_trade_from_db.num_contracts == 654321)
        
if __name__ == '__main__':
    unittest.main()