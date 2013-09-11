#!/usr/bin/env python3
'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1
'''
import datetime
from abc import abstractmethod, ABCMeta
from checking_tools import IntegrityError, typecheck, trader_check, \
    symbol_check, year_check, month_check, datetime_check, \
    currency_pair_check, price_futures_check, price_spotfx_check


# TRADE_CLASSES is defined at the bottom to avoid recursive import


class Trade(tuple):
    """ abstract class for trade object
        trades are immutable in order to keep the integrity of the database
        that's why we use tuple and __new__ instead of __init__
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_variables_names(cls):
        """ define the variables"""
        cls_, *var_names = cls.__new__.__code__.co_varnames
        return list(var_names)

    @classmethod
    def get_variables_types(cls):
        """ define the variables"""
        return [cls.__new__.__annotations__.get(arg)
                for arg in cls.get_variables_names()]

    @classmethod
    def get_variables_names_no_id(cls):
        """ define the variables"""
        cls_, id_, *var_names = cls.__new__.__code__.co_varnames
        return list(var_names)

    @classmethod
    def get_variables_types_no_id(cls):
        """ define the variables"""
        return [cls.__new__.__annotations__.get(arg)
                for arg in cls.get_variables_names_no_id()]

    def __setattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        raise IntegrityError("Cannot set attribute of an existing trade")

    def __delattr__(self, *ignored):
        """ trade are immutable objects
        in order to keep the integrity of the database"""
        raise IntegrityError("Cannot delete attribute of an existing trade")

    def __str__(self):
        variables_names = self.get_variables_names()
        return ", ".join(name + ": " + str(getattr(self, name))
                         for name in variables_names)

    def get_variables_dict(self):
        params = self.get_variables_names()
        return {param: getattr(self, param) for param in params}

    def get_variables_dict_no_id(self):
        params = self.get_variables_names_no_id()
        return {param: getattr(self, param) for param in params}

    @abstractmethod
    def instruments_positions(self):
        """ return a dict of {instrument: position}"""
        pass


class FuturesTrade(Trade):
    """
    Futures trades
    defined as (id_, datetime_, symbol, month, year, 
                num_contracts, price, trader).
    E.g., a sell of -15 Dec 13 bund contracts at 137.52 might be represented as 
    (id00001, 2013-09-09 09:00:00, RX, 12, 2013, -15, 137.52, pierre).
    """
    @typecheck
    def __new__(cls,
                id_: int,
                datetime_: datetime.datetime,
                symbol: str,
                month: int,
                year: int,
                num_contracts: int,
                price: float,
                trader: str):
        datetime_check(datetime_)
        symbol_check(symbol)
        month_check(month)
        year_check(year)
        trader_check(trader)
        price_futures_check(price, symbol, month, year)
        return tuple.__new__(cls,
            (id_, datetime_, symbol, month, year, num_contracts, price, trader))

    @property
    def instruments_positions(self):
        return {(self.symbol, self.month, self.year): self.num_contracts}

    @property
    def id_(self):
        return self[0]

    @property
    def datetime_(self):
        return self[1]

    @property
    def symbol(self):
        return self[2]

    @property
    def month(self):
        return self[3]

    @property
    def year(self):
        return self[4]

    @property
    def num_contracts(self):
        return self[5]

    @property
    def price(self):
        return self[6]

    @property
    def trader(self):
        return self[7]

    @staticmethod
    def get_trade_example():
        datetime_ = datetime.datetime(2013, 9, 9, 9, 0, 0)
        return FuturesTrade(-1, datetime_, "RX", 12, 2013, -15, 137.52, "pierre")


class SpotFXTrade(Trade):
    """
    Spot FX trades, 
    defined as (id_, datetime_, currency pair, size, price, trader).
    E.g., a buy of 1 million AUDUSD at 0.9205 would be represented as
    (id00002, 2013-09-09 09:00:00, AUDUSD, 1000000, 0.9205, damien).
    """
    @typecheck
    def __new__(cls,
                id_: int,
                datetime_: datetime.datetime,
                currency_pair: str,
                size: int,
                price: float,
                trader: str):
        datetime_check(datetime_)
        currency_pair_check(currency_pair)
        trader_check(trader)
        price_spotfx_check(price, currency_pair)
        return tuple.__new__(cls,
                             (id_, datetime_, currency_pair, size, price, trader))

    @property
    def instruments_positions(self):
        return {self.currency_pair[0:3]:-self.size,
                self.currency_pair[3:7]: self.size * self.price}

    @property
    def id_(self):
        return self[0]

    @property
    def datetime_(self):
        return self[1]

    @property
    def currency_pair(self):
        return self[2]

    @property
    def size(self):
        return self[3]

    @property
    def price(self):
        return self[4]

    @property
    def trader(self):
        return self[5]

    @staticmethod
    def get_trade_example():
        datetime_ = datetime.datetime(2013, 9, 9, 9, 0, 0)
        return SpotFXTrade(-1, datetime_, "AUDUSD", 1000000, 0.9205, "damien")


TRADE_CLASSES = [FuturesTrade, SpotFXTrade]

def check_trade_class(trade_class):
    if trade_class not in TRADE_CLASSES:
        raise TypeError("Please check the class %s" % trade_class.__name__)
