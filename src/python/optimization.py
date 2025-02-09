#!/usr/bin/python3

"""
File: optimization.py
Author: Wolfgang Fuerst
Date: 2025-02-02
Description: Optimize portfolio in general
Structure:
    1.    load portfolio & all data
    2.    portfolio calulation of
    2.1   - percentage within portfolio
    2.2   - overall portfolio virtual performance
    2.3   - recommanded share within the portfolio
    3.    store complete table
            isin, share, percentage, performance, vola, recommanded percentage
Issues:
    ...
Runtime: ...

Args:
    None
"""
from datetime import datetime
import time

import numpy as np                                              # numpy
import pandas as pd                                             # pandas

import mylib.config2 as config
from mylib import mysql_db  # database connection

from mylib.writeLog import writeLog                             # write log
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

METHOD = "optimization_1"
LOG_TEXT = ' general portfolio optimization'

# 1. load config file
CONFIG = config.load_config('config.json')["analytics"]

# log entry
log_id = CONFIG[METHOD]['log_id']

writeLog(CONFIG['file']['log'], 'Start'+LOG_TEXT+'', id = log_id)

# setup the connection to the source database
mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())

# 1.    load portfolio & all candidates from reference

"""
      symbol          isin                              companyName       all
167  EXSA.DE  DE0002635307  iShares STOXX Europe 600 UCITS ETF (DE)   544.200
195    GOOGL  US02079K3059                                 Alphabet   100.000
232     INTC  US4581401001                                    Intel   313.000
360   PHAU.L  JE00B1VS3770                 WisdomTree Physical Gold   897.662
427   TEG.DE  DE0008303504                        TAG Immobilien AG  1042.000
"""

# portfolio = get_portfolio()
# print(portfolio)

# ---

try:
    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_portfolio"])
    portfolio = mysql_db.get_mysql_data(connection_to_source, source, \
                                        columns = CONFIG[METHOD]["columns_source_portfolio"])
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading symbols from source', id = log_id)

try:
    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, \
                                    CONFIG[METHOD]["table_source_reference"])
    reference = mysql_db.get_mysql_data(connection_to_source, source, \
                                        columns = CONFIG[METHOD]["columns_source_reference"])
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading symbols from source', id = log_id)

# merge with the leading table is the portfolio, not to loose any
# 1. reference-items not in portfolio: reference.loc[~reference['isin'].isin(portfolio['isin'])]
# 2. concat & replace nan by 0
reference = reference.loc[~reference['isin'].isin(portfolio['isin'])]
portfolio = pd.concat([portfolio, reference])
portfolio['all'] = portfolio['all'].fillna(0)

# print(portfolio)

# 2.    portfolio calulation of
# 2.1   - percentage within portfolio

price = []
perf = []
vola = []
sr = []
ts_portfolio = pd.DataFrame(columns=['date'])
ts_portfolio.set_index('date', inplace=True)

# load timeseries / last 400 days - quick and dirty
first_date = datetime.now() + pd.DateOffset(days=-400)

for index, row in portfolio.iterrows():

    print(row['isin'], row['companyName'], row['symbol'], row['all']) # print info

    try:
        connection_to_source = sql_engine.connect()
        source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_ts"])
        ts = mysql_db.get_mysql_data(connection_to_source, source, \
                                     columns = CONFIG[METHOD]["columns_source_ts"], \
                                     filter_symbol = row['symbol'], \
                                     filter_date = first_date.strftime("%Y-%m-%d"), \
                                     order_desc = False)
        connection_to_source.close()
    except:
        writeLog(CONFIG['file']['log'], 'Error reading timeserie from source', id = log_id)

    ts.date = pd.to_datetime(ts.date)
    ts.set_index('date', inplace=True)
    ts_normalized = standardizeTimeSerie(ts, 'endDate-1year', 'lastBDay')   # std. to one-year
    if row['all'] > 0:
        ts_normalized = ts_normalized*row['all']
    else:
        ts_normalized = ts_normalized/ts_normalized.iloc[0]/10

    ts_portfolio[row['symbol']] = ts_normalized.close.copy()
portfolio.set_index('symbol', inplace=True) # perf, vola, sr per equity

ts_portfolio.loc[:,'total'] = ts_portfolio.sum(numeric_only=True, axis=1)   # sum of portfolio
portfolio['share'] = ts_portfolio.iloc[0]/ts_portfolio.iloc[0].iloc[-1] # portf.-share on last date

# portfolio['share'] = ts_portfolio.iloc[-1]/ts_portfolio.iloc[-1].iloc[-1] # ... on first date

pvs = performanceAndVolaAndSR(ts_portfolio['total'], 1) # pvs of portfolio
portfolio['perf_all'] = pvs[0]
portfolio['vola_all'] = pvs[1]
portfolio['sr_all'] = pvs[2]

# normalize every item to start value & start optimization calculation
ts_portfolio = ts_portfolio/ts_portfolio.iloc[-1]

perf = ts_portfolio.iloc[:0,:].copy()   # dataframe for performance, vola and sr
vola = ts_portfolio.iloc[:0,:].copy()
sr = ts_portfolio.iloc[:0,:].copy()

# iterate through change of investigated element vs. portfolio
steps = np.concatenate([np.arange(0,.1,.001),np.arange(.1,1.01,.01)])
for i in steps:
    pvs = performanceAndVolaAndSR((i*ts_portfolio).add(ts_portfolio.total*(1-i), axis = 0),1)
    perf = perf._append(pvs[0], ignore_index = True)
    vola = vola._append(pvs[1], ignore_index = True)
    sr = sr._append(pvs[2], ignore_index = True)

perf.index = steps  # change the index of dataframes to split
vola.index = steps
sr.index = steps

# portfolio['recommanded_max_perf'] = perf[:].idxmax()
portfolio['recommended_min_vola'] = vola[:].idxmin()
portfolio['recommended_max_sr'] = sr[:].idxmax()

portfolio['one_percent_perf'] = perf[:].loc[perf.index == 0.01].transpose()
portfolio['one_percent_vola'] = vola[:].loc[vola.index == 0.01].transpose()

# plt.plot(vola[546],perf[546])
# plt.show()

perf_new = []
vola_new = []
sr_new = []

for index, row in portfolio.iterrows():
    perf_new.append(perf.loc[row['recommended_min_vola'], index])
    vola_new.append(vola.loc[row['recommended_min_vola'], index])
    sr_new.append(sr.loc[row['recommended_min_vola'], index])
portfolio['perf_min_vola_rec'] = perf_new
portfolio['vola_min_vola_rec'] = vola_new
portfolio['sr_min_vola_rec'] = sr_new

portfolio['sector'] = 4
for index, row in portfolio.iterrows():
    if portfolio.loc[index, 'perf_all'] < portfolio.loc[index, 'perf_min_vola_rec'] and \
        portfolio.loc[index, 'vola_all'] > portfolio.loc[index, 'vola_min_vola_rec']:
        portfolio.loc[index, 'sector'] = 1
    if portfolio.loc[index, 'perf_all'] > portfolio.loc[index, 'perf_min_vola_rec'] and \
        portfolio.loc[index, 'vola_all'] > portfolio.loc[index, 'vola_min_vola_rec']:
        portfolio.loc[index, 'sector'] = 3
    if portfolio.loc[index, 'sector'] == 4:
        if portfolio.loc[index, 'perf_all'] < portfolio.loc[index, 'one_percent_perf']:
            portfolio.loc[index, 'sector'] = 2

portfolio['change_perf'] = portfolio['one_percent_perf']-portfolio['perf_all']
portfolio['change_vola'] = portfolio['one_percent_vola']-portfolio['vola_all']
portfolio['change_sensitivity'] = abs(portfolio['change_perf']/portfolio['change_vola'])

portfolio.sort_values(by = ['sector', 'change_perf'], ascending=[True, False], inplace = True)

# store data
try:
    connection_to_target = sql_engine.connect()
    target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target"])
    mysql_db.put_dataframe_to_mysql(connection_to_target, target, \
                                    portfolio, CONFIG[METHOD]["pk_target"], update_timestamp = True)
    connection_to_target.close()
except:
    writeLog(CONFIG['file']['log'], 'Error writing to target - no update', id = log_id)

# plt.plot(vola, perf)
# plt.legend(portfolio['name'])
# plt.show()

# 4. log entry and wait
writeLog(CONFIG['file']['log'], 'End'+LOG_TEXT+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+LOG_TEXT+' for '\
         +str(CONFIG[METHOD]["delay"])+'s', id = log_id)
time.sleep(CONFIG[METHOD]["delay"])
