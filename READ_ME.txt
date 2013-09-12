Here is the list of ".py" files, in order of dependency:
- tms_constants: constants and config
- checking_tools: independent tools for checking
- trade_models: trade classes, immutable instances to keep the integrity of the tables
- db_management: all the sql request are done here. tables are created automatically from the signature of trade classes
- db_helper: day to day easy functions to see how to interact nicely with the database
- tms_unittests: unittest for the database (use a test database) with each type of trade
- tms_parsefile: parse the instructions of a csv file to feed the database (an example file is set up by default in the test base)

Please note there are two databases: one and one for tests
A log file system is setup when parsing a file to keep record of the instructions
TODO: A similar one could be created to monitor the database manipulation

TODO: Some tests are not written, like the existence of an instrument in a flat file or prices being between bounds
seeTODO in checking_tools.py

#######################################

Exemple to check all the files:

python3 tms_constants.py
python3 checking_tools.py
python3 trade_models.py
python3 db_management.py
python3 tms_unittests.py
python3 db_helper.py
python3 tms_parsefile.py
python3 tms_parsefile.py instructions_futures_day1.csv
python3 tms_parsefile.py instructions_spotfx_day1.csv
python3 tms_parsefile.py instructions_futures_day2.csv
python3 tms_parsefile.py instructions_spotfx_day2.csv
python3 db_helper.py

have a look at: log_file_parsing_test.csv and trade_management_system_test.db fed from instructions_example.csv

have a look at: log_file_parsing.csv and trade_management_system.db fed from the files instructions_XXX_day_Y.csv

#######################################

Example of parsing:
delete trade_management_system_test.db if it exists
cmd > python3 tms_parsefile.py
look at trade_management_system_test.db

#######################################

Example of multiple files use:
delete trade_management_system.db if it exists
python3 tms_parsefile.py instructions_futures_day1.csv
python3 tms_parsefile.py instructions_spotfx_day1.csv
python3 tms_parsefile.py instructions_futures_day2.csv
python3 tms_parsefile.py instructions_spotfx_day2.csv
look at trade_management_system.db
python3 db_helper.py

#######################################

Example of printing tables and holdings:
python3 db_helper.py

#######################################
