#!/usr/bin/env python

"""
File: correlation.py
Author: Wolfgang Fuerst
Date: 2025-02-09
Description: Calulation of correlation between different assets
Structure:
    Load config file
    Load data with the age of approx. 1 year
    Calculate correlation with normalized data for 1 year
    Save data
    Wait according config
Issues:
    ...
Runtime:
    30min for 500 items
"""
from datetime import datetime

import time                                                     # requ. to wait
import pandas as pd                                             # pandas

from mylib import config                                        # read configuration-data
from mylib.writeLog import writeLog                             # write log file
from mylib import mysql_db                                      # database connection
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

# basic config

METHOD = "correlation"
LOG_TEXT = ' analyzing correlation'

# load config file & write log entry for start
CONFIG = config.load_config('config.json')["analytics"]
log_id = CONFIG[METHOD]['log_id']
log_text = LOG_TEXT
writeLog(CONFIG['file']['log'], 'Start'+log_text+'', id = log_id)

# setup the connection to the source database
mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())

# load data

first_date = datetime.now() + pd.DateOffset(days=-400) # get last 400 days

try:
    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source"])
    data = mysql_db.get_mysql_data(connection_to_source, source, \
                                columns = CONFIG[METHOD]["columns_source"], \
                                filter_date = first_date.strftime("%Y-%m-%d"), \
                                order_desc = False)
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading from source', id = log_id)

# DEBUG
# data = data[~data['symbol'].isin(['0MKP.L', '1COV.DE', '6594.T'])] # exclude that items
# data = data[data['symbol'].isin(['0MKP.L', '1COV.DE'])] # only that items

# calculation
data['date'] = pd.to_datetime(data['date'])         # convert date to datetime

data_interpolated = pd.DataFrame()                  # empty dataframe
datagroup = data.groupby('symbol')                  # grouping by symbol
for name, group in datagroup:
    group.set_index(['date'], inplace = True)       # iterate through groups and interpolate
    data_interpolated = pd.concat([data_interpolated, \
                                standardizeTimeSerie(group, 'endDate-1year', 'lastBDay')])
data_interpolated.index.names = ['date']            # rename index colum

datagroup = data_interpolated.groupby('symbol')     # grouping by symbol

symbol = datagroup.size()
symbol = symbol.reset_index()
symbol = symbol['symbol']

result = pd.DataFrame(columns=['symbol_i', 'perf', 'vola', 'sr', 'symbol_j', 'corr_ij'])

start = datetime.now()
print('start at: ', start)

length_symbol = len(symbol)

for i in range(0, length_symbol):

    ts_i = datagroup.get_group(symbol[i]).copy()
    # ts_i.set_index('date', inplace = True)
    ts_i.drop(columns=['symbol'], inplace = True)
    pvs = performanceAndVolaAndSR(ts_i, years = 1)

    mid = datetime.now()

    for j in range(i, length_symbol):
        if symbol[i] != symbol[j]:
            ts_j = datagroup.get_group(symbol[j]).copy()
            # ts_j.set_index('date', inplace = True)
            ts_j.drop(columns=['symbol'], inplace = True)
            corr_ij = ts_i.pct_change().corrwith(ts_j.pct_change(), axis = 0)
            # df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            result = pd.concat([result, pd.DataFrame([{'symbol_i': symbol[i], \
                                                    'perf': float(pvs[0].close), \
                                                    'vola': float(pvs[1].close), \
                                                    'sr': float(pvs[2].close), \
                                                    'symbol_j': symbol[j], \
                                                    'corr_ij': float(corr_ij.close)}])], \
                                                    ignore_index = True)
    print(result)
    end = datetime.now()
    print(i, 'out of', length_symbol)
    print('Estimated finishing: ', start + length_symbol*(end - mid))
    # print('another_halfcycle: ', mid-start)
    # print('another_cycle: ', end-start)

result["symbol_ij"] = result["symbol_i"]+"_"+result["symbol_j"] # create pk

# store data

try:
    connection_to_target = sql_engine.connect()
    target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target"])
    mysql_db.put_dataframe_to_mysql(connection_to_target, target, \
                                result, CONFIG[METHOD]["pk_target"], update_timestamp = True)
    connection_to_target.close()
except:
    writeLog(CONFIG['file']['log'], 'Error writing to target - no update', id = log_id)

# log entry and wait

writeLog(CONFIG['file']['log'], 'End'+log_text+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+log_text+' for '\
         +str(CONFIG[METHOD]["delay"])+'s', id = log_id)
time.sleep(CONFIG[METHOD]["delay"])
