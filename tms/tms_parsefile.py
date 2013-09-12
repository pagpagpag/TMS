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

launch from command line with:
python3 tms_parsefile.py my_file.csv clean_boolean
clean_boolean is optional (False if not specified)

a log file keep record of all the instructions sent to the database 
'''
import sys
import csv
import datetime
from collections import defaultdict
from trade_models import FuturesTrade, SpotFXTrade
from db_helper import clean_all_tables, display_all_tables
from db_helper import display_all_holdings
from db_management import TMSDataBaseConfig, TMSDataBase
from tms_constants import TEST_MODE_PARSING, FORCE_CLEAN_PARSING, \
    VERBOSE_PARSING, TEST_MODE_PARSING_EXAMPLE, \
    FORCE_CLEAN_PARSING_EXAMPLE, VERBOSE_PARSING_EXAMPLE, \
    LOG_FILE_PARSING_TEST, LOG_FILE_PARSING, \
    TRADE_TYPE_FUTURES, TRADE_TYPE_SPOTFX, \
    INSTRUCTION_ADD, INSTRUCTION_AMEND, INSTRUCTION_CANCEL, \
    ISO_DATE_FORMAT, INSTRUCTIONS_EXAMPLE_FILE_NAME, INSTRUCTIONS_FOLDER


DB_CONFIG_PARSING_EXAMPLE = TMSDataBaseConfig(test_mode=TEST_MODE_PARSING_EXAMPLE,
                                              force_clean=FORCE_CLEAN_PARSING_EXAMPLE,
                                              verbose=VERBOSE_PARSING_EXAMPLE)

DB_CONFIG_PARSING = TMSDataBaseConfig(test_mode=TEST_MODE_PARSING,
                                      force_clean=FORCE_CLEAN_PARSING,
                                      verbose=VERBOSE_PARSING)

# link the text instruction to the specified trade class
TRADE_TYPES_CLASSES = {TRADE_TYPE_FUTURES: FuturesTrade,
                       TRADE_TYPE_SPOTFX: SpotFXTrade
                       }

TEST_MODE_PARSING = False

class ParseTradesFiles(object):
    def __init__(self, file_name, config=DB_CONFIG_PARSING):
        self.file_name = file_name
        self.config = config
        self.dbs = {}
        self.counter = defaultdict(int)
        log_file_path = LOG_FILE_PARSING
        if self.config.test_mode:
            log_file_path = LOG_FILE_PARSING_TEST
        print(INSTRUCTIONS_FOLDER + log_file_path)
        self.log_file = open(log_file_path, 'a')

    def __del__(self):
        self.log_file.close()

    def run(self):
        """ read instruction in the file line per line
            do it two times, the first one just to check
            because we don't want to cut the file if there was an error in it
        """
        for check_mode in [True, False]:
            with open(INSTRUCTIONS_FOLDER + self.file_name, 'r') as csvfile:
                if self.config.verbose and not check_mode:
                    print("Parsing %s" % self.file_name)
                filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in filereader:
                    instruction, trade_type, *args = row
                    self.manage_instruction(check_mode, instruction, trade_type, *args)
                    if not check_mode:
                        self.save_log_row(row)

    def save_log_row(self, row):
        now_ = datetime.datetime.today().strftime(ISO_DATE_FORMAT)
        log_row = now_ + "," + ",".join(x for x in row) + "\n"
        self.log_file.write(log_row)

    def manage_instruction(self, check_mode, instruction, trade_type, *args):
        """ handle every instruction"""
        trade_class = get_trade_class(trade_type)
        db = self.get_db(trade_class)
        if instruction == INSTRUCTION_ADD:
            trade = get_arg_to_add_trade_from_parsing(trade_class, id_=-1, args=args)
            if not check_mode:
                db.add_trade(trade)
        elif instruction == INSTRUCTION_AMEND:
            id_, field, value_typed = get_arg_to_amend_trade_from_parsing(trade_class, args)
            if not check_mode:
                db.amend_trade_with_field(id_, field, value_typed)
        elif instruction == INSTRUCTION_CANCEL:
            id_ = get_arg_to_cancel_trade_from_parsing(trade_class, args)
            if not check_mode:
                db.cancel_trade(id_)
        else:
            raise ValueError("Unknown instruction: %s" % instruction)

    def save_executed_row(self, test_mode, row):
        """ keep record of all the executed rows"""




    def get_db(self, trade_class):
        if trade_class not in self.dbs:
            self.dbs[trade_class] = TMSDataBase(trade_class, self.config)
        return self.dbs[trade_class]

def get_arg_to_add_trade_from_parsing(trade_class, id_, args):
    check_len_args(len(trade_class.get_variables_names_no_id()), args)
    trade_kwargs = {}
    trade_kwargs["id_"] = id_
    zipper = zip(trade_class.get_variables_names_no_id(),
                 trade_class.get_variables_types_no_id(), args)
    for var_name, var_type, var_value in zipper:
        if var_name == "datetime_":
            trade_kwargs[var_name] = parse_date(var_value)
        else:
            trade_kwargs[var_name] = var_type(var_value)
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

def check_len_args(expected_arg_size, args):
    if len(args) != expected_arg_size:
        raise TypeError("Wrong args")

def get_instructions_from_cmd_line():
    instructions = INSTRUCTIONS_EXAMPLE_FILE_NAME
    example = True
    if len(sys.argv) > 1:
        instructions = sys.argv[1]
        example = False
        if instructions[-4::1] != ".csv":
            raise TypeError("%s is not a csv file" % instructions)
    return (instructions, example)

def get_clean_boolean_from_cmd_line():
    clean_ = False
    if len(sys.argv) > 2:
        if sys.argv[2] not in ["True", "False"]:
            raise TypeError("Please enter True or False as second argument")
        if sys.argv[2] == "True":
            clean_ = True
    return clean_

def launcher():
    # get the csv file
    instructions, example = get_instructions_from_cmd_line()
    clean_ = example or get_clean_boolean_from_cmd_line()
    config = DB_CONFIG_PARSING_EXAMPLE if example else DB_CONFIG_PARSING
    if clean_:
        clean_all_tables(config)
    else:
        display_all_tables(config)
    ParseTradesFiles(instructions, config).run()
    print()
    display_all_tables(config)
    print()
    display_all_holdings(config)

if __name__ == '__main__':
    launcher()
