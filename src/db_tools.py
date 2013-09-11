#!/usr/bin/env python3

'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1

all these functions work by themselves
'''
from db_models import TMSDataBaseSpotFX, TMSDataBaseFutures
from trade_models import SpotFXTrade, FuturesTrade

def create_futures_table(test_mode=True):
    TMSDataBaseFutures(test_mode)

def create_spotfx_table(test_mode=True):
    TMSDataBaseSpotFX(test_mode)
    
def add_futures_trade(trade, test_mode=True):
    TMSDataBaseFutures(test_mode).add_trade(trade)

def add_spot_fx_trade(trade, test_mode=True):
    TMSDataBaseSpotFX(test_mode).add_trade(trade)
    
def cancel_futures_trade(id, test_mode=True):
    TMSDataBaseFutures(test_mode).cancel_trade(id)
    
def cancel_spotfx_trade(id, test_mode=True):
    TMSDataBaseSpotFX(test_mode).cancel_trade(id)

def amend_futures_trade_with_trade(id, trade, test_mode=True):
    TMSDataBaseFutures(test_mode).amend_trade_with_trade(id, trade)
        
def amend_futures_trade_with_field(self, id, field, value, test_mode=True):
    TMSDataBaseFutures(test_mode).amend_trade_with_field(id, field, value)

def amend_futures_trade_with_fields(self, id, fields_values, test_mode=True):
    TMSDataBaseFutures(test_mode).amend_trade_with_fields(id, fields_values)

def amend_spot_fx_trade_with_trade(id, trade, test_mode=True):
    TMSDataBaseSpotFX(test_mode).amend_trade_with_trade(id, trade)
        
def amend_spot_fx_trade_with_field(self, id, field, value, test_mode=True):
    TMSDataBaseSpotFX(test_mode).amend_trade_with_field(id, field, value)

def amend_spot_fx_trade_with_fields(self, id, fields_values, test_mode=True):
    TMSDataBaseSpotFX(test_mode).amend_trade_with_fields(id, fields_values)

def clean_futures_table(test_mode=True):
    TMSDataBaseFutures(test_mode).clean_table()

def clean_spotfx_table(test_mode=True):
    TMSDataBaseSpotFX(test_mode).clean_table()