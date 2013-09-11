#!/usr/bin/env python3
'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1
'''
import functools
import inspect
import datetime
from decorator import decorator
from tms_constants import TRADERS_LIST


class IntegrityError(Exception):
    pass

@decorator
def typecheck(function_, *args, **kws):
    """ useful type checking decorator from annotations when types are used
        potentially check parameters and return type
    """
    @functools.wraps(function_)
    def decorated(*args, **kws):
        for i, arg in enumerate(function_.__code__.co_varnames):
            argtype = function_.__annotations__.get(arg)
            # Only check if annotation exists and it is as a type
            if isinstance(argtype, type):
                # First len(args) are positional, after that keywords
                value_to_test = args[i] if i < len(args) else kws[arg]
                if not isinstance(value_to_test, argtype):
                    raise TypeError("%s is not of type %s when calling %s with %s" %
                    (value_to_test, argtype, function_.__qualname__, arg))
        # check the return type
        result = function_(*args, **kws)
        returntype = function_.__annotations__.get('return')
        if returntype is not None and not isinstance(returntype, type):
            raise TypeError("Wrong return type: " +
                             "%s is not of type %s when calling %s" %
                             (result, returntype, function_.__qualname__))
        return result
    return decorated(*args, **kws)

def check_trade(trade, trade_class):
    """ check if the instance trade belongs to the desired class"""
    if not isinstance(trade, trade_class):
        message = trade.to_string() if hasattr(trade, "to_string") else "Unknown"
        raise TypeError("The following is not a %s trade \n %s" %
                        (trade_class.__name__, message))
    return True

def datetime_check(datetime_):
    """ check if the datetime is not incorrect"""
    if not (datetime.datetime(1900, 1, 1) < datetime_ < datetime.datetime(2100, 1, 1)):
        raise ValueError("Please check the date %s" % datetime_)

def trader_check(trader):
    """ only authorized persons can trade"""
    if trader not in TRADERS_LIST:
        raise ValueError("Trader %s traded but is not in the list of traders"
                         % trader)

def symbol_check(symbol):
    """ check if the symbol exist"""
    if (len(symbol) == 0):
        raise ValueError("Symbol %s of length 0 detected" % symbol)
    # TODO: check if symbol is in the list of futures instrument
    pass

def currency_pair_check(currency_pair):
    """ check if this currency_pair exists"""
    if len(currency_pair) != 6:
        raise ValueError("%s is not a currency pair" % currency_pair)
    # TODO: check from a list of all existing currency pairs
    pass

def year_check(year):
    """ check if the maturity year is not stupid"""
    if year < 2000:
        raise ValueError("Please check the maturity year %s which looks expired"
                         % year)
    if year > 2100:
        raise ValueError("Please check the maturity year %s which looks too far"
                         % year)

def month_check(month):
    """ check if a month int value is correct"""
    if not 0 < month < 13:
        raise ValueError("Impossible month: %d" % month)

def check_integrity_columns(columns_sql, trade_class):
    """ check that columns names are exactly the class values
        integrity of the SQL / python mapping
    """
    def_names_sql = list((str(columns_sql[i]) for i in range(0, len(columns_sql))))
    def_names_class = inspect.signature(trade_class).parameters
    if set(def_names_class) != set(def_names_sql):
        raise IntegrityError("The integrity of the columns have been damaged")

def price_futures_check(price, symbol, month, year):
    # TODO: add systematic checks for all prices
    pass

def price_spotfx_check(price, currency_pair):
    # for example
    # TODO: add systematic checks for all prices
    if ((currency_pair == "EURGBP" and not (0.5 < price < 1.2))
            or (currency_pair == "EURUSD" and not (0.6 < price < 1.8))
            or (currency_pair == "GBPUSD" and not (0.7 < price < 2.3))):
        raise ValueError("Please check that you traded %d at %d" %
                         (currency_pair, price))
