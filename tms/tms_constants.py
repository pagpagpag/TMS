'''
Created on Sep 11, 2013

@author: pierreadrienguez

constants here, no import
'''
TRADERS_LIST = ["damien", "pierre"]

DATA_FOLDER = "data/"
INSTRUCTIONS_FOLDER = "instructions/"

DATABASE_FILE = DATA_FOLDER + "trade_management_system.db"
DATABASE_FILE_TEST = DATA_FOLDER + "trade_management_system_test.db"

DATABASE_PATH = "sqlite:///" + DATABASE_FILE
DATABASE_PATH_TEST = "sqlite:///" + DATABASE_FILE_TEST

LOG_FILE_PARSING = DATA_FOLDER + "log_file_parsing.csv"
LOG_FILE_PARSING_TEST = DATA_FOLDER + "log_file_parsing_test.csv"

INSTRUCTIONS_EXAMPLE_FILE_NAME = "instructions_example.csv"

# if you don't specify otherwise, you will:
# access the real database
# be ask if you really want to clean a table
# get some messages
TEST_MODE_DEFAULT = False
FORCE_CLEAN_DEFAULT = False
VERBOSE_DEFAULT = True

TEST_MODE_UNITTEST = True
FORCE_CLEAN_UNITTEST = True
VERBOSE_UNITTEST = False

TEST_MODE_PARSING = False
FORCE_CLEAN_PARSING = False
VERBOSE_PARSING = True

TEST_MODE_PARSING_EXAMPLE = True
FORCE_CLEAN_PARSING_EXAMPLE = True
VERBOSE_PARSING_EXAMPLE = True

# first instruction
INSTRUCTION_ADD = "add"
INSTRUCTION_CANCEL = "cancel"
INSTRUCTION_AMEND = "amend"

# second instruction
TRADE_TYPE_FUTURES = "futures"
TRADE_TYPE_SPOTFX = "spotfx"

# to parse datetime
ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
