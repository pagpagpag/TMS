'''
Created on Sep 9, 2013

@author: pierreadrienguez
'''
import pprint
import inspect
from os.path import exists
from abc import abstractmethod, ABCMeta
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.engine.result import ResultProxy
from futurestrade import FuturesTrade
from spotfxtrade import SpotFXTrade
from checking_tools import check_trade

DATABASE_FILE = 'trade_management_system.db'    
DATABASE_PATH = "sqlite:///" + DATABASE_FILE

class TMSDataBase(object):
    """ all the operations within the data base have to be encapsulated here"""
    __metaclass__ = ABCMeta
    
    def __init__(self):
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
        db = create_engine(DATABASE_PATH)
        db.echo = False  # turn off verbose mode
        metadata = MetaData(db)
        if not exists(DATABASE_FILE):
            self.__create_table_if_first_time(metadata)
        return Table(self.table_name, metadata, autoload=True)
        
    def __create_table_if_first_time(self, metadata):
        """ create the sql table only the first time"""
        columns_sql = self._get_columns_sql()
        self.__check_integrity_columns_first_time(columns_sql)
        table = Table(self.table_name, metadata, *columns_sql)
        table.create()
        
    def __check_integrity_columns_first_time(self, columns_sql):
        """ check that columns names are exactly the class values
            we need this for the mapping SQL / python
        """
        def_names_sql = self.__get_columns_from_sql_formating(columns_sql)
        def_names_class = inspect.signature(self.trade_class).parameters
        if set(def_names_class) != set(def_names_sql):
            raise NameError("")
        
    def __get_columns_from_sql_formating(self, columns_sql):
        return list((str(columns_sql[i]) for i in range(0, len(columns_sql))))
        
    def __mapper(self, result_proxy):
        """ return the list of trades from a SQL select query
            yes, it does the job of orm.__mapper but here we can keep our own classes
            however, this could be rewritten #TODO
        """
        columns = self.__get_columns_from_sql_formating(self._get_columns_sql())
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
        """ return True if the trade was canceled"""
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
        
    def amend_trade_with_field(self, id, field, value):
        """ amend only a field of a trade from its id """
        trade_original = self.select_trade_from_id(id)
        if trade_original is None:
            raise ValueError("Cannot amend trade %d because it doesn't exist" % id)
        var_dict = trade_original.get_variables_dict()
        var_dict[field] = value # replace in the dict
        trade_copy = self.trade_class(**var_dict)
        print("B", trade_copy.__str__)
        self.amend_trade_with_trade(id, trade_copy)
        
    def display_table(self):
        select_cmd = self.__table.select()
        select_cmd_res = select_cmd.execute()
        pprint.pprint([row for row in select_cmd_res])
        
    def get_all_table_as_trades(self):
        return self.__mapper(self.__table.select().execute())
        
    def clean_table(self):
        """ dangerous function"""
        if input("Are you sure you want to DELETE the __table %s ? (Y/N)"
                     % self.table_name) == 'Y':
            self.__table.delete().execute()
            print("Table %s is now empty" % self.table_name)