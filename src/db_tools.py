'''
Created on Sep 9, 2013

@author: pierreadrienguez

all this functions work by themselves
'''
from db_models import TMSDataBaseSpotFX, TMSDataBaseFutures
from trade_models import SpotFXTrade, FuturesTrade

def create_futures_table():
    TMSDataBaseFutures()

def create_spotfx_table():
    TMSDataBaseSpotFX()
    
def add_futures_trade(trade):
    TMSDataBaseFutures().add_trade(trade)

def add_spot_fx_trade(trade):
    TMSDataBaseSpotFX().add_trade(trade)
    
def cancel_futures_trade(id):
    TMSDataBaseFutures().cancel_trade(id)
    
def cancel_spotfx_trade(id):
    TMSDataBaseSpotFX().cancel_trade(id)

def amend_futures_trade_with_trade(id, trade):
    TMSDataBaseFutures().amend_trade_with_trade(id, trade)
        
def amend_futures_trade_with_field(self, id, field, value):
    TMSDataBaseFutures().amend_trade_with_field(id, field, value)

def amend_futures_trade_with_fields(self, id, fields_values):
    TMSDataBaseFutures().amend_trade_with_fields(id, fields_values)

def amend_spot_fx_trade_with_trade(id, trade):
    TMSDataBaseSpotFX().amend_trade_with_trade(id, trade)
        
def amend_spot_fx_trade_with_field(self, id, field, value):
    TMSDataBaseSpotFX().amend_trade_with_field(id, field, value)

def amend_spot_fx_trade_with_fields(self, id, fields_values):
    TMSDataBaseSpotFX().amend_trade_with_fields(id, fields_values)

def clean_futures_table():
    TMSDataBaseFutures().clean_table()

def clean_spotfx_table():
    TMSDataBaseSpotFX().clean_table()

if __name__ == '__main__':
    create_spotfx_table()