#!/usr/bin/python3

"""
File: pvs.py
Author: Wolfgang Fuerst
Date: 2025-02-09
Description: Calculate performance & vola & sharp ratio over different periods from 1 to 10 years
Structure:
    Load config file
    Load data after 2015-01-01
    Calculate performance & vola & sharp ratio on annual normalization
    Save data
    Wait according config
Issues:
    ...
Runtime:
    15min for 500 items
Args:
    None
"""

import time                                                     # requ. to wait
import pandas as pd                                             # pandas

from mylib import config                                        # read configuration-data
from mylib.writeLog import writeLog                             # write log file
from mylib import mysql_db                                      # database connection
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

# basic config

METHOD = "performancevolasr"
LOG_TEXT = ' validate performance, vola & sr'

# load config file & write log entry for start
CONFIG = config.load_config('config.json')["analytics"]
log_id = CONFIG[METHOD]['log_id']
log_text = LOG_TEXT
writeLog(CONFIG['file']['log'], 'Start'+log_text+'', id = log_id)

# setup the connection to the source database
mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())

# define empty data-frame that will filled towards the restult

result = pd.DataFrame(columns=['symbol', 'max_date', 'min_date', 'period', 'perf', 'vola', 'sr'])

# load list of time series

"""
pks:

      symbol    max_date    min_date
0    1COV.DE  2025-01-17  2015-10-06
1    2222.SR  2025-01-19  2019-12-11
..       ...         ...         ...
491     ZION  2025-01-17  1972-04-03
492      ZTS  2025-01-17  2013-02-01

[493 rows x 3 columns]
"""

try:
    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source"])
    pks = mysql_db.get_mysql_min_max(connection_to_source, source)
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading symbols from source', id = log_id)

# iterate time series and do calculation

# DEBUG pks = pks[:5]

for index, row in pks.iterrows():
    try:
        connection_to_source = sql_engine.connect()
        source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source"])
        ts = mysql_db.get_mysql_data(connection_to_source, source, \
                                    columns = CONFIG[METHOD]["columns_source"], \
                                    filter_date = "2015-01-01", filter_symbol = row['symbol'], \
                                    order_by = "date", order_desc = True)
        connection_to_source.close()
    except:
        writeLog(CONFIG['file']['log'], 'Error reading timeserie from source', id = log_id)

    ts.date = pd.to_datetime(ts.date)
    ts.set_index('date', inplace=True)                          # set date as index
    ts_normalized = standardizeTimeSerie(ts, 'first', 'last')   # standardize ts
    for i in range(1,11):                                       # 10 years of caluclation
        pvs = performanceAndVolaAndSR(ts_normalized, i)         # calculate for 1y & add
        if pvs:                                                 # only attach successful calc.
            # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            result = pd.concat([result, pd.DataFrame([{'symbol': row['symbol'], \
                'max_date': row['max_date'], 'min_date': row['min_date'], 'period': i, \
                'perf': pvs[0].close, 'vola': pvs[1].close, 'sr': pvs[2].close}])], \
                ignore_index = True)
            """
            result = result.append({'symbol': row['symbol'], 'max_date': row['max_date'], \
                'min_date': row['min_date'], 'period': i, 'perf': pvs[0].close, \
                'vola': pvs[1].close, 'sr': pvs[2].close}, ignore_index = True)
            """
    print('.', end='', flush=True)                                      # show operation

# store data

try:
    connection_to_target = sql_engine.connect()
    target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target"])
    mysql_db.put_dataframe_to_mysql(connection_to_target, target, result, \
                                    CONFIG[METHOD]["pk_target"], update_timestamp = True)
    connection_to_target.close()
except:
    writeLog(CONFIG['file']['log'], 'Error writing to target - no update', id = log_id)

# log entry and wait

writeLog(CONFIG['file']['log'], 'End'+log_text+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+log_text+' for '\
         +str(CONFIG[METHOD]["delay"])+'s', id = log_id)
time.sleep(CONFIG[METHOD]["delay"])
