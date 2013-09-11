#!/usr/bin/env python3

'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1
'''
import pprint
import inspect
from abc import abstractmethod, ABCMeta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.engine.result import ResultProxy
from checking_tools import check_trade, check_integrity_columns

DATABASE_FILE = 'trade_management_system.db'
DATABASE_FILE_TEST = 'trade_management_system_test.db'
DATABASE_PATH = "sqlite:///" + DATABASE_FILE
DATABASE_PATH_TEST = "sqlite:///" + DATABASE_FILE_TEST

TEST_MODE_DEFAULT = True

class TMSDataBase(object):
    """ all the operations within the data base have to be encapsulated here
        use an abstract trade_class
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, test_mode=TEST_MODE_DEFAULT):
        """ use test_mode by being True by default such that you have to stipulate
            test_mode=False if you want to access the real database
        """
        self.test_mode = test_mode
        self._define_trade_class() # from a child class
        self.table_name = self.trade_class.__name__
        self.__table = self.__get_table()
        
    @abstractmethod
    def _define_trade_class(self):
        self.trade_class = None
        raise TypeError("The abstract TMSDataBase cannot be instantiated")
    
    @abstractmethod
    def _get_columns_sql(self):
        """ full documented __table
            the names have to match the names of the class
            (this will be checked)
            return a tuple of 'sqlalchemy.schema.Column'
        """
    
    def __get_table(self):
        db = create_engine(DATABASE_PATH if not self.test_mode else DATABASE_PATH_TEST)
        db.echo = False  # turn off verbose mode
        columns_sql = self._get_columns_sql()
        check_integrity_columns(columns_sql, self.trade_class)
        table = Table(self.table_name, MetaData(db), *columns_sql)
        # create the table if it doesn't exist
        table.create(checkfirst=True)
        return table
        
    def __mapper(self, result_proxy):
        """ return the list of trades from a SQL select query
            yes, it does the job of orm.__mapper but here we can keep our own classes
            however, this could be rewritten #TODO:s
        """
        columns_sql = self._get_columns_sql()
        columns = list((str(columns_sql[i]) for i in range(0, len(columns_sql))))
        kwargs_columns_entry = list({col: field 
                                     for (col, field) in zip(columns, entry)}
                                     for entry in list(result_proxy))
        return list(self.trade_class(**columns_entry) 
                    for columns_entry in kwargs_columns_entry)
    
    def add_trade(self, trade):
        if check_trade(trade, self.trade_class):
            self.__table.insert().execute(**trade.get_variables_dict_no_id())
            
    def select_trade_from_id(self, id):
        list_of_trades = self.__mapper(self.__table.select()
                           .where(self.__table.c.id == id).execute())
        return None if not list_of_trades else list_of_trades[0]
        
    def cancel_trade(self, id):
        if not self.select_trade_from_id(id):
            raise ValueError("Cannot cancel trade %d because it doesn't exist" % id)
        self.__table.delete().where(self.__table.c.id == id).execute()
        
    def amend_trade_with_trade(self, id, trade):
        if check_trade(trade, self.trade_class):
            if self.select_trade_from_id(id) is None:
                raise ValueError("Cannot amend trade %d because it doesn't exist" % id)
            columns_sql_with_trade_values = {column: getattr(trade, str(column)) 
                                             for column in self._get_columns_sql()
                                             if str(column) != "id"}
            update_req = self.__table.update().where(self.__table.c.id == id)
            update_req.values(columns_sql_with_trade_values).execute()
        
    def amend_trade_with_fields(self, id, fields_values_dict):
        """ amend multiple fields of a trade from its id """
        trade_original = self.select_trade_from_id(id)
        if trade_original is None:
            raise ValueError("Cannot amend trade %d because it doesn't exist" % id)
        var_dict = trade_original.get_variables_dict()
        for field in fields_values_dict:
            var_dict[field] = fields_values_dict[field]
        amended_trade = self.trade_class(**var_dict)
        self.amend_trade_with_trade(id, amended_trade)
        
    def amend_trade_with_field(self, id, field, value):
        """ amend only a field of a trade from its id """
        self.amend_trade_with_fields(id, {field: value})
        
    def display_table(self):
        pprint.pprint([row for row in self.__table.select().execute()])
        
    def get_all_table_as_trades(self):
        return self.__mapper(self.__table.select().execute())
        
    def clean_table(self, force_clean=False, verbose=True):
        """ dangerous function"""
        if force_clean or input("Are you sure you want to DELETE the __table %s ? (Y/N)"
                     % self.table_name) == 'Y':
            self.__table.delete().execute()
            if verbose:
                print("Table %s is now empty" % self.table_name)