"""calculate correlations"""

#!/usr/bin/python3

from datetime import datetime
import pandas as pd                                             # pandas
from mylib.writeLog import writeLog                             # write log
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr
from mylib.investment_db import get_quote_eur_timeserie_all_1y
from mylib.investment_db import put_dataframe_to_table

LOG_FILE = './analytics.log'                                            # load log-file

writeLog(LOG_FILE,'calculate correlations started', id = 'FCA')    # log-start

data = get_quote_eur_timeserie_all_1y()
data['date'] = pd.to_datetime(data['date'])         # convert date to datetime

data_interpolated = pd.DataFrame()                  # empty dataframe
datagroup = data.groupby('symbol')                  # grouping by symbol
for name, group in datagroup:
    group.set_index(['date'], inplace = True)       # iterate through groups and interpolate
    data_interpolated = pd.concat([data_interpolated, standardizeTimeSerie(group, 'today-1year', 'today')])
data_interpolated.index.names = ['date']            # rename index colum

datagroup = data_interpolated.groupby('symbol')     # grouping by symbol

symbol = datagroup.size()
symbol = symbol.reset_index()
symbol = symbol['symbol']

result = pd.DataFrame(columns=['symbol_i', 'perf', 'vola', 'sr', 'symbol_j', 'corr_ij'])

start = datetime.now()

for i in range(0, len(symbol)):

    ts_i = datagroup.get_group(symbol[i]).copy()
    # ts_i.set_index('date', inplace = True)
    ts_i.drop(columns=['symbol'], inplace = True)
    pvs = performanceAndVolaAndSR(ts_i, years = 1)

    mid = datetime.now()

    for j in range(i, len(symbol)):
        if symbol[i] != symbol[j]:
            ts_j = datagroup.get_group(symbol[j]).copy()
            # ts_j.set_index('date', inplace = True)
            ts_j.drop(columns=['symbol'], inplace = True)
            corr_ij = ts_i.pct_change().corrwith(ts_j.pct_change(), axis = 0)
            """
            result = result.append({'symbol_i': symbol[i], 'perf': pvs[0].close, \
                'vola': pvs[1].close, 'sr': pvs[2].close, \
                'symbol_j': symbol[j], 'corr_ij': corr_ij.close}, ignore_index = True)
            """
            result = result._append({'symbol_i': symbol[i], 'perf': pvs[0], \
                'vola': pvs[1].close, 'sr': pvs[2].close, \
                'symbol_j': symbol[j], 'corr_ij': corr_ij.close}, ignore_index = True)
    print(result)
    end = datetime.now()
    print('another_halfcycle: ', mid-start)
    print('another_cycle: ', end-start)

# 3. store dataframe

put_dataframe_to_table(result, 'validation_correlation')

writeLog(LOG_FILE,'calculate correlations stopped', id = 'FCA')    # log-stop