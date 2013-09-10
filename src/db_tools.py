'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
from db_models import TMSDataBaseSpotFX, TMSDataBaseFutures
from trade_models import SpotFXTrade, FuturesTrade

def add_trade(trade):
    """ we can check the type before the connection, so let's do it"""
    if isinstance(trade, SpotFXTrade):
        add_spot_fx_trade(trade)
    elif isinstance(trade, FuturesTrade):
        add_futures_trade(trade)
    else:
        raise TypeError("Unknown trade type %s" % type(trade))
    
def add_spot_fx_trade(trade):
    TMSDataBaseSpotFX().add_trade(trade)
    
def add_futures_trade(trade):
    TMSDataBaseFutures().add_trade(trade)

def delete_spotfx_trade(id_: int):
    TMSDataBaseSpotFX().delete_trade(id_)

def delete_futures_trade(id_: int):
    TMSDataBaseFutures().delete_trade(id_)
    
if __name__ == '__main__':
    pass