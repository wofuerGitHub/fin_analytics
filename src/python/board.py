#!/usr/bin/python3

"""
File: board.py
Author: Wolfgang Fuerst
Date: 2025-03-01
Description: Optimize portfolio specific on SR, EPR, BPR.
    Timeserie is interpolated, so that even on non-trading days, the ratios are calculated correct
Structure:
    1.    load _reference_map & got through if active
    2.    walk through and get timeserie and fundamental
    3.    calculate rations per_est, per_mean, ...
    4.    store result
Issues:
    ...
Runtime: 
    ...
Args:
    None
"""
from datetime import datetime
import time                                                     # requ. to wait
import pandas as pd                                             # pandas

from mylib import config                                        # read configuration-data
from mylib.writeLog import writeLog                             # write log file
from mylib import mysql_db                                      # database connection

# basic config

METHOD = "board"
LOG_TEXT = ' specific portfolio optimization'

# load config file & write log entry for start
CONFIG = config.load_config('config.json')["analytics"]
log_id = CONFIG[METHOD]['log_id']
log_text = LOG_TEXT
writeLog(CONFIG['file']['log'], 'Start'+log_text+'', id = log_id)

# setup the connection to the source database
mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())

# 1. load _reference_map

try:
    connection_to_source = sql_engine.connect()
    REFERENCE = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_reference"])
    ref_data = mysql_db.get_mysql_data(connection_to_source, REFERENCE, \
                                        columns = CONFIG[METHOD]["columns_source_reference"])
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading symbols from reference', id = log_id)

# print(ref_data)

# 2. walk through and get timeserie and fundamental

first_date = datetime.now() + pd.DateOffset(years =- CONFIG[METHOD]["period"])

for row in ref_data.itertuples():
    print(row.active, row.symbol, row.symbol_fundamental)

    if row.active and row.symbol_fundamental:
        try:
            connection_to_source = sql_engine.connect()
            EDBCS_REF = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_edcbps"])
            fun = mysql_db.get_mysql_data(connection_to_source, EDBCS_REF, \
                                        columns = CONFIG[METHOD]["columns_source_edcbps"], \
                                        filter_symbol = row.symbol_fundamental, \
                                        filter_date = first_date.strftime("%Y-%m-%d"), \
                                        order_desc = False)
            connection_to_source.close()
        except:
            writeLog(CONFIG['file']['log'], 'Error reading symbols from edbcs', id = log_id)

        # print(fun)

        try:
            connection_to_source = sql_engine.connect()
            TS_REF = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_ts"])
            ts = mysql_db.get_mysql_data(connection_to_source, TS_REF, \
                                        columns = CONFIG[METHOD]["columns_source_ts"], \
                                        filter_symbol = row.symbol, \
                                        filter_date = first_date.strftime("%Y-%m-%d"), \
                                        order_desc = False)
            connection_to_source.close()
        except:
            writeLog(CONFIG['file']['log'], 'Error reading symbols from edbcs', id = log_id)

        # print(ts)
        
        ts['date'] = pd.to_datetime(ts['date'])
        last_date = max(ts['date']).strftime('%Y-%m-%d')
        ts = ts.set_index('date').resample('D').ffill()
        ts.sort_index(ascending=True, inplace=True)
        ts['last_close'] = ts.iloc[-1].close

        fun['date'] =  pd.to_datetime(fun['date'])
        fun = fun.set_index('date')

 #       fun = fun.dropna(axis = 1)  # drops colomns that are empty

        output = pd.concat([fun, ts], axis = 1).dropna(axis = 0).mean(axis = 0, numeric_only = True)

# 3. calculate rations per_est, per_mean, ...
        output = output.dropna(axis = 0)

        print(output)

        data_set = {"date": last_date, "symbol": row.symbol, "companyName": row.companyName}        
        if 'grossProfitRatio' in output: data_set["grossProfitRatio"] = str(output.grossProfitRatio)
        if 'researchAndDevelopmentRatio' in output: data_set["researchAndDevelopmentRatio"] = str(output.researchAndDevelopmentRatio)
        if 'interestExpenseRatio' in output: data_set["interestExpenseRatio"] = str(output.interestExpenseRatio)
        if ('last_close' in output) and ('close' in output):
            if ('eps' in output) and output.eps != 0.0:
                data_set["per_est"] = str(output.last_close/output.eps)
                data_set["per_mean"] = str(output.close/output.eps)
            if ('dps' in output) and output.dps != 0.0:
                data_set["pdr_est"] = str(output.last_close/output.dps)
                data_set["pdr_mean"] = str(output.close/output.dps)
            if ('cps' in output) and output.cps != 0.0:
                data_set["pcr_est"] = str(output.last_close/output.cps)
                data_set["pcr_mean"] = str(output.close/output.cps)
            if ('bps' in output) and output.bps != 0.0:
                data_set["pbr_est"] = str(output.last_close/output.bps)
                data_set["pbr_mean"] =  str(output.close/output.bps)
            data_set["ppr_est"] = str(output.last_close/output.close)
            data_set["ppr_mean"] = str(output.close/output.close)

# 4. store result

        try:
            connection_to_target = sql_engine.connect()
            target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target_board"])
            mysql_db.put_dict_to_mysql(connection_to_target, target, data_set, \
                                        CONFIG[METHOD]["pk_target_board"], update_timestamp = True)
            connection_to_target.close()
        except:
            writeLog(CONFIG['file']['log'], 'Could not write '+row.symbol+' data to board', id = log_id)

# 5. log entry and wait
writeLog(CONFIG['file']['log'], 'End'+LOG_TEXT+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+LOG_TEXT+' for '\
         +str(CONFIG[METHOD]["delay"])+'s', id = log_id)
time.sleep(CONFIG[METHOD]["delay"])