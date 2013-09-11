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
from db_helper import add_trade, amend_trade_with_field, cancel_trade
from db_helper import clean_all_tables, display_all_tables
from db_helper import get_holdings, display_all_holdings


INSTRUCTIONS_EXAMPLE_FILE_NAME = "instructions_example.csv"

#first instruction
INSTRUCTION_ADD = "add"
INSTRUCTION_CANCEL = "cancel"
INSTRUCTION_AMEND = "amend"

#second instruction
TRADE_TYPE_FUTURES = "futures"
TRADE_TYPE_SPOTFX = "spotfx"

#tail of instruction depends on the first one:
#
ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

TRADE_TYPES_CLASSES = {TRADE_TYPE_FUTURES: FuturesTrade,
                    TRADE_TYPE_SPOTFX: SpotFXTrade
                    }

TEST_MODE_PARSING = False


def parse_trades_file(file_name):
    with open(file_name, 'r') as csvfile:
        print("Parsing %s" % file_name)
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        counter = defaultdict(int)
        for row in filereader:
            instruction, trade_type, *args = row
            trade_class = get_trade_class(trade_type)
            if instruction == INSTRUCTION_ADD:
                counter[trade_class] += 1
                add_trade_from_parsing(trade_class, counter[trade_class], args)
            elif instruction == INSTRUCTION_AMEND:
                amend_trade_from_parsing(trade_class, args)
            elif instruction == INSTRUCTION_CANCEL:
                cancel_trade_from_parsing(trade_class, args)
            else:
                raise ValueError("Unknown instruction: %s" % instruction)

def add_trade_from_parsing(trade_class, id_, args):
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
    trade = trade_class(**trade_kwargs)
    add_trade(trade, trade_class, test_mode=TEST_MODE_PARSING)

def amend_trade_from_parsing(trade_class, args):
    check_len_args(3, args)
    id_, field, value = args
    possible_types = trade_class.get_variables_types_no_id()
    index_type = trade_class.get_variables_names_no_id().index(field)
    value_typed = possible_types[index_type](value)
    amend_trade_with_field(trade_class, int(id_), field, value_typed, 
                           test_mode=TEST_MODE_PARSING)
    
def cancel_trade_from_parsing(trade_class, args):
    check_len_args(1, args)
    id_ = int(args[0])
    cancel_trade(trade_class, id_, test_mode=TEST_MODE_PARSING)
    
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
    clean_all_tables(force_clean=True, verbose=False, test_mode=TEST_MODE_PARSING)
    #display_all_tables()
    parse_trades_file(INSTRUCTIONS_EXAMPLE_FILE_NAME)
    print()
    display_all_tables(TEST_MODE_PARSING)
    print()
    display_all_holdings(test_mode=TEST_MODE_PARSING)