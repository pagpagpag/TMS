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
from db_management import TMSDataBase, DB_CONFIG_DEFAULT


def get_db(trade_class, config=DB_CONFIG_DEFAULT):
    check_trade_class(trade_class)
    return TMSDataBase(trade_class, config)
        
def add_trade(trade, trade_class, config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).add_trade(trade)
    
def cancel_trade(trade_class, id_, config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).cancel_trade(id_)
    
def amend_trade_with_field(trade_class, id_, field, value, 
                           config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).amend_trade_with_field(id_, field, value)

def amend_trade_with_fields(trade_class, id_, fields_values, 
                            config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).amend_trade_with_fields(id_, fields_values)

def amend_trade_with_trade(trade_class, id_, trade, 
                           config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).amend_trade_with_trade(id_, trade)
        
def clean_table(trade_class, config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).clean_table()
    
def clean_all_tables(config=DB_CONFIG_DEFAULT):
    for trade_class in TRADE_CLASSES:
        clean_table(trade_class, config)
    
def display_table(trade_class, config=DB_CONFIG_DEFAULT):
    get_db(trade_class, config).display_table()
    
def display_all_tables(config=DB_CONFIG_DEFAULT):
    for trade_class in TRADE_CLASSES:
        display_table(trade_class, config)
    
def get_holdings_from_trades(trades, config=DB_CONFIG_DEFAULT):
    holdings = defaultdict(int)
    for trade in trades:
        for instrument, position in trade.instruments_positions.items():
            holdings[instrument] += position
    return dict(holdings)
    
def get_holdings(trade_class, config=DB_CONFIG_DEFAULT):
    trades = get_db(trade_class, config).get_all_table_as_trades()
    return get_holdings_from_trades(trades, config)

def display_holdings(trade_class, config=DB_CONFIG_DEFAULT):
    print("Holdings in %s" % trade_class.__name__)
    pprint.pprint(get_holdings(trade_class, config))
    
def display_all_holdings(config=DB_CONFIG_DEFAULT):
    for trade_class in TRADE_CLASSES:
        display_holdings(trade_class, config)