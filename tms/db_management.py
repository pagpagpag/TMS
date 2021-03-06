#!/usr/bin/env python3
'''
Created on Sep 9, 2013

@author: pierreadrienguez
@status: production
@version: 1
'''
import pprint
import datetime
from collections import namedtuple
from sqlalchemy import create_engine, MetaData, Table, String, DateTime, Float
from sqlalchemy import Column, Integer
from checking_tools import check_trade, check_integrity_columns
from trade_models import check_trade_class
from tms_constants import TEST_MODE_DEFAULT, FORCE_CLEAN_DEFAULT, \
    VERBOSE_DEFAULT, DATABASE_PATH, DATABASE_PATH_TEST



TYPE_TO_SQL_TYPE = {datetime.datetime: DateTime,
                    str: String,
                    int: Integer,
                    float: Float,
                    str: String}

TMSDataBaseConfig = namedtuple("TMSDataBaseConfig",
                               ("test_mode", "force_clean", "verbose"))

DB_CONFIG_DEFAULT = TMSDataBaseConfig(TEST_MODE_DEFAULT,
                                      FORCE_CLEAN_DEFAULT,
                                      VERBOSE_DEFAULT)

class TMSDataBase(object):
    """ all the operations within the database have to be encapsulated here
    """
    def __init__(self, trade_class, config=DB_CONFIG_DEFAULT):
        check_trade_class(trade_class)
        self.trade_class = trade_class
        self.config = config
        self.table_name = self.trade_class.__name__
        self.__table = self.__get_table()

    def __get_columns_sql(self):
        """ get the columns from the "signature" of the Trade class
            (bit of white magic)
        """
        ccc = [Column('id_', Integer, primary_key=True)]
        for name, type_ in zip(self.trade_class.get_variables_names_no_id(),
                          self.trade_class.get_variables_types_no_id()):
            ccc.append(Column(name, TYPE_TO_SQL_TYPE[type_]))
        return ccc

    def __get_table(self):
        path = DATABASE_PATH if not self.config.test_mode else DATABASE_PATH_TEST
        database = create_engine(path)
        database.echo = False  # turn off verbose mode
        columns_sql = self.__get_columns_sql()
        check_integrity_columns(columns_sql, self.trade_class)
        table = Table(self.table_name, MetaData(database), *columns_sql)
        # create the table if it doesn't exist
        table.create(checkfirst=True)
        return table

    def __mapper(self, result_proxy):
        """ return the list of trades from a SQL select query
            yes, it does the job of orm.__mapper but here we can keep our own classes
        """
        result_proxy_list = list(result_proxy)
        columns = self.trade_class.get_variables_names()
        kwargs_columns_entry = list({col: field
                         for (col, field) in zip(columns, entry)}
                         for entry in result_proxy_list)
        return list(self.trade_class(**columns_entry)
                    for columns_entry in kwargs_columns_entry)

    def add_trade(self, trade):
        if check_trade(trade, self.trade_class):
            self.__table.insert().execute(**trade.get_variables_dict_no_id())

    def select_trade_from_id(self, id_):
        list_of_trades = self.__mapper(self.__table.select()
                           .where(self.__table.c.id_ == id_).execute())
        return None if not list_of_trades else list_of_trades[0]

    def cancel_trade(self, id_):
        if not self.select_trade_from_id(id_):
            raise ValueError("Cannot cancel trade %d in %s because it doesn't exist"
                             % (id_, self.table_name))
        self.__table.delete().where(self.__table.c.id_ == id_).execute()

    def amend_trade_with_trade(self, id_, trade):
        if check_trade(trade, self.trade_class):
            if self.select_trade_from_id(id_) is None:
                raise ValueError("Cannot amend trade %d because it doesn't exist" % id_)
            columns_sql_with_trade_values = {column: getattr(trade, str(column))
                                             for column in self.__get_columns_sql()
                                             if str(column) != "id_"}
            update_req = self.__table.update().where(self.__table.c.id_ == id_)
            update_req.values(columns_sql_with_trade_values).execute()

    def amend_trade_with_fields(self, id_, fields_values_dict):
        """ amend multiple fields of a trade from its id """
        trade_original = self.select_trade_from_id(id_)
        if trade_original is None:
            raise ValueError("Cannot amend trade %d because it doesn't exist"
                             % id_)
        var_dict = trade_original.get_variables_dict()
        for field, var in fields_values_dict.items():
            var_dict[field] = var
        amended_trade = self.trade_class(**var_dict)
        self.amend_trade_with_trade(id_, amended_trade)

    def amend_trade_with_field(self, id_, field, value):
        """ amend only a field of a trade from its id """
        self.amend_trade_with_fields(id_, {field: value})

    def display_table(self):
        if self.config.verbose:
            print("Table %s:" % self.trade_class.__name__)
        pprint.pprint([str(row) for row in self.get_all_table_as_trades()])

    def clean_table(self):
        """ dangerous function, it can clean a table"""
        ok_to_cancel = self.config.force_clean
        if not self.config.force_clean:
            message = "Are you sure you want to DELETE the __table %s ? (Y/N)"
            self.config.force_clean = input(message % self.table_name) == 'Y'
        if ok_to_cancel:
            self.__table.delete().execute()
            if self.config.verbose:
                if self.config.test_mode:
                    message = "(TEST MODE) "
                message += "Table %s is now empty"
                print(message % self.table_name)


    def get_all_table_as_trades(self):
        """ useful request to get all info from the table
            functions using it should be written in db_tools module, not here
        """
        return self.__mapper(self.__table.select().execute())
