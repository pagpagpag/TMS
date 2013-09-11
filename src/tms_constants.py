'''
Created on Sep 11, 2013

@author: pierreadrienguez

constants here, no import
'''
TRADERS_LIST = ["damien", "pierre"]

DATABASE_FILE = 'trade_management_system.db'
DATABASE_FILE_TEST = 'trade_management_system_test.db'

DATABASE_PATH = "sqlite:///" + DATABASE_FILE
DATABASE_PATH_TEST = "sqlite:///" + DATABASE_FILE_TEST

# if you don't specify otherwise, you will:
# access the testing database
# be ask if you really want to clean a table
# get some messages
TEST_MODE_DEFAULT = True
FORCE_CLEAN_DEFAULT = False
VERBOSE_DEFAULT = True

TEST_MODE_UNITTEST = True
FORCE_CLEAN_UNITTEST = True
VERBOSE_UNITTEST = False

TEST_MODE_PARSING = False
FORCE_CLEAN_PARSING = True
VERBOSE_PARSING = True
