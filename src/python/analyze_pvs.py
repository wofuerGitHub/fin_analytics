"""calculate performance & vola & sharpe ratio"""

#!/usr/bin/python3

import pandas as pd                                             # pandas

from mylib.writeLog import writeLog                             # write log
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

from mylib.investment_db import get_quote_eur_list
from mylib.investment_db import get_quote_eur_timeserie
from mylib.investment_db import put_dataframe_to_table

LOG_FILE = './fin_suite4.log'

writeLog(LOG_FILE,'validate performance, vola & sr started', id = 'FPV')    # log-start

# 0. define empty data-frame

result = pd.DataFrame(columns=['symbol', 'max_date', 'min_date', 'period', 'perf', 'vola', 'sr'])

# 1. load list of time series

pks = get_quote_eur_list()

# 2. iterate time series and do calculation

for index, row in pks.iterrows():                                       # iterate pk
    ts = get_quote_eur_timeserie(row['symbol'])
    ts.date = pd.to_datetime(ts.date)
    ts.set_index('date', inplace=True)                                  # set date as index
    ts_normalized = standardizeTimeSerie(ts, 'first', 'last')           # standardize ts
    for i in range(1,11):                                               # 10 years of caluclation
        pvs = performanceAndVolaAndSR(ts_normalized, i)                 # calculate for 1y & add
        if pvs:                                                         # only attach successful calculations
            """
            result = result.append({'symbol': row['symbol'], 'max_date': row['max_date'], \
                'min_date': row['min_date'], 'period': i, 'perf': pvs[0].close, \
                'vola': pvs[1].close, 'sr': pvs[2].close}, ignore_index = True)
            """
            result = result._append({'symbol': row['symbol'], 'max_date': row['max_date'], \
                'min_date': row['min_date'], 'period': i, 'perf': pvs[0], \
                'vola': pvs[1].close, 'sr': pvs[2].close}, ignore_index = True)
    print('.', end='', flush=True)                                      # show operation

# 3. store dataframe

put_dataframe_to_table(result, 'validation_pvs')

writeLog(LOG_FILE,'validate performance, vola & sr stopped', id = 'FVP')    # log-stop
