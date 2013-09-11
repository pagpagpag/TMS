#!/usr/bin/env python3

'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1

all these functions work by themselves
'''
import pprint
from collections import defaultdict
from trade_models import SpotFXTrade, FuturesTrade, check_trade_class, TRADE_CLASSES
from db_management import TMSDataBase
from db_management import VERBOSE_DEFAULT, FORCE_CLEAN_DEFAULT,\
    TEST_MODE_DEFAULT


def get_db(trade_class, test_mode=TEST_MODE_DEFAULT):
    check_trade_class(trade_class)
    return TMSDataBase(trade_class)
        
def add_trade(trade, trade_class, test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).add_trade(trade)
    
def cancel_trade(trade_class, id_, test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).cancel_trade(id_)
    
def amend_trade_with_field(trade_class, id_, field, value, 
                           test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).amend_trade_with_field(id_, field, value)

def amend_trade_with_fields(trade_class, id_, fields_values, 
                            test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).amend_trade_with_fields(id_, fields_values)

def amend_trade_with_trade(trade_class, id_, trade, 
                           test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).amend_trade_with_trade(id_, trade)
        
def clean_table(trade_class, force_clean=FORCE_CLEAN_DEFAULT,
                verbose=VERBOSE_DEFAULT, test_mode=TEST_MODE_DEFAULT):
    get_db(trade_class, test_mode).clean_table(force_clean=force_clean, 
                                               verbose=verbose)
    
def clean_all_tables(force_clean=FORCE_CLEAN_DEFAULT, verbose=VERBOSE_DEFAULT, 
                     test_mode=TEST_MODE_DEFAULT):
    for trade_class in TRADE_CLASSES:
        clean_table(trade_class, force_clean, verbose, test_mode)
    
def display_table(trade_class, test_mode=TEST_MODE_DEFAULT, 
                  verbose=VERBOSE_DEFAULT):
    get_db(trade_class, test_mode).display_table(verbose=verbose)
    
def display_all_tables(test_mode=TEST_MODE_DEFAULT, verbose=VERBOSE_DEFAULT):
    for trade_class in TRADE_CLASSES:
        display_table(trade_class, test_mode, verbose)
    
def get_holdings_from_trades(trades, test_mode=TEST_MODE_DEFAULT):
    holdings = defaultdict(int)
    for trade in trades:
        for instrument, position in trade.instruments_positions.items():
            holdings[instrument] += position
    return dict(holdings)
    
def get_holdings(trade_class, test_mode=TEST_MODE_DEFAULT):
    trades = get_db(trade_class, test_mode).get_all_table_as_trades()
    return get_holdings_from_trades(trades, test_mode=test_mode)

def display_holdings(trade_class, test_mode=TEST_MODE_DEFAULT):
    print("Holdings in %s" % trade_class.__name__)
    pprint.pprint(get_holdings(trade_class, test_mode))
    
def display_all_holdings(test_mode=TEST_MODE_DEFAULT):
    for trade_class in TRADE_CLASSES:
        display_holdings(trade_class, test_mode)