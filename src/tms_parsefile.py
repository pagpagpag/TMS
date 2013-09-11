#!/usr/bin/env python3
'''
Created on Sep 11, 2013

@author: pierreadrienguez
@status: production
@version: 1

parse a csv file with each line being
instruction,trade_type,tail
where (instruction, tail) is:
- (add, trade details without id)
- (cancel, id)
- (amend, id, field, value) 
'''
import csv
import datetime
from collections import defaultdict
from trade_models import FuturesTrade, SpotFXTrade
from db_helper import clean_all_tables, display_all_tables
from db_helper import get_holdings, display_all_holdings
from db_management import TMSDataBaseConfig, TMSDataBase
from tms_constants import TEST_MODE_PARSING, FORCE_CLEAN_PARSING,\
    VERBOSE_PARSING


DB_CONFIG_PARSING = TMSDataBaseConfig(test_mode=TEST_MODE_PARSING,
                                      force_clean=FORCE_CLEAN_PARSING,
                                      verbose=VERBOSE_PARSING)

INSTRUCTIONS_EXAMPLE_FILE_NAME = "instructions_example.csv"

#first instruction
INSTRUCTION_ADD = "add"
INSTRUCTION_CANCEL = "cancel"
INSTRUCTION_AMEND = "amend"

#second instruction
TRADE_TYPE_FUTURES = "futures"
TRADE_TYPE_SPOTFX = "spotfx"

#to parse datetime
ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

#link the text instruction to the specified trade class
TRADE_TYPES_CLASSES = {TRADE_TYPE_FUTURES: FuturesTrade,
                       TRADE_TYPE_SPOTFX: SpotFXTrade
                       }

TEST_MODE_PARSING = False

class ParseTradesFiles():
    def __init__(self, file_name, config=DB_CONFIG_PARSING):
        self.file_name = file_name
        self.config = config
        self.dbs = {}
        
    def run(self):
        """ read instruction in the file line per line"""
        with open(self.file_name, 'r') as csvfile:
            if self.config.verbose:
                print("Parsing %s" % self.file_name)
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            self.counter = defaultdict(int)
            for row in filereader:
                instruction, trade_type, *args = row
                self.manage_instruction(instruction, trade_type, *args)
                
    def manage_instruction(self, instruction, trade_type, *args):
        """ handle every instruction"""
        trade_class = get_trade_class(trade_type)
        db = self.get_db(trade_class)
        if instruction == INSTRUCTION_ADD:
            self.counter[trade_class] += 1
            id_ = self.counter[trade_class]
            trade = get_arg_to_add_trade_from_parsing(trade_class, id_, args)
            db.add_trade(trade)
        elif instruction == INSTRUCTION_AMEND:
            id_, field, value_typed = get_arg_to_amend_trade_from_parsing(trade_class, args)
            db.amend_trade_with_field(id_, field, value_typed)
        elif instruction == INSTRUCTION_CANCEL:
            id_ = get_arg_to_cancel_trade_from_parsing(trade_class, args)
            db.cancel_trade(id_)
        else:
            raise ValueError("Unknown instruction: %s" % instruction)
    
    def get_db(self, trade_class):
        if trade_class not in self.dbs:
            self.dbs[trade_class] = TMSDataBase(trade_class, self.config)
        return self.dbs[trade_class]

def get_arg_to_add_trade_from_parsing(trade_class, id_, args):
    check_len_args(len(trade_class.get_variables_names_no_id()), args)
    trade_kwargs = {}
    trade_kwargs["id"] = id_
    zipper = zip(trade_class.get_variables_names_no_id(), 
                 trade_class.get_variables_types_no_id(), args)
    for var_name, var_type, var_value in zipper:
        if var_name == "datetime":
            trade_kwargs[var_name] = parse_date(var_value)
        else:
            trade_kwargs[var_name] = var_type(var_value)
    print(trade_kwargs)
    trade = trade_class(**trade_kwargs)
    return trade

def get_arg_to_amend_trade_from_parsing(trade_class, args):
    check_len_args(3, args)
    id_, field, value = args
    possible_types = trade_class.get_variables_types_no_id()
    index_type = trade_class.get_variables_names_no_id().index(field)
    value_typed = possible_types[index_type](value)
    return (int(id_), field, value_typed)
    
def get_arg_to_cancel_trade_from_parsing(trade_class, args):
    check_len_args(1, args)
    id_ = int(args[0])
    return id_
    
def parse_date(datetime_iso):
    return datetime.datetime.strptime(datetime_iso, ISO_DATE_FORMAT)
    
def get_trade_class(trade_type):
    if trade_type not in TRADE_TYPES_CLASSES:
        raise TypeError("Unknown trade type: %s" % trade_type)
    return TRADE_TYPES_CLASSES[trade_type]

def check_len_args(n, args):
    if len(args) != n:
        raise TypeError("Wrong args")
    
if __name__ == '__main__':
    config = DB_CONFIG_PARSING
    instructions = INSTRUCTIONS_EXAMPLE_FILE_NAME
    clean_all_tables(config)
    #display_all_tables(config)
    ParseTradesFiles(instructions, config).run()
    print()
    display_all_tables(config)
    print()
    display_all_holdings(config)