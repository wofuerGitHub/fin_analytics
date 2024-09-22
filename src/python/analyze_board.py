"""calculate validation board"""

#!/usr/bin/python3

import datetime as dt
import numpy as np
import pandas as pd

# from scipy.stats import linregress

from mylib.investment_db import get_edcbps_history
from mylib.investment_db import get_mysql_data
from mylib.investment_db import put_dataframe_to_table
from mylib.writeLog import writeLog

LOG_FILE = './analytics.log'                      # load log-file
writeLog(LOG_FILE,'validate board started', id = 'VAB')    # log-start

# --- BLOCK 1 - Split on years as annual_pivot on the last 7 years
# the generated table
#               value_2021  value_2020  value_2019  value_2018  value_2017  value_2016  ...    bps_2020    bps_2019    bps_2018    bps_2017    bps_2016    bps_2015
# isin
# US1270971039         NaN       12.70       15.30       20.72      23.722      21.531  ...   14.765850   16.106443   16.645486   16.909123    5.219710    4.435705
# US38141G1040         NaN      211.20      205.70      144.21     213.540     227.503  ...  226.668499  231.979151  214.372501  183.751051  209.270648  189.089080

pks = get_edcbps_history()
pks.date = pd.to_datetime(pks.date)             # date becomes datetime
pks['dps'] = pks['dps'].fillna(0)               # missing dividends are set to zero

pks['date'] = pks['date'].dt.strftime('%Y')     # change date to years

# print(pks.loc[pks['isin']=='JP3942600002'])

selected_columns = pks[["isin"]]
annual_pivot = selected_columns.copy()
annual_pivot = annual_pivot.drop_duplicates(subset=['isin'], keep='last')
annual_pivot = annual_pivot.set_index('isin')

for index, row in pks.iterrows():
    annual_pivot.at[row['isin'], 'eps_'+str(row['date'])] = row['eps']
    annual_pivot.at[row['isin'], 'dps_'+str(row['date'])] = row['dps']
    annual_pivot.at[row['isin'], 'cps_'+str(row['date'])] = row['cps']
    annual_pivot.at[row['isin'], 'bps_'+str(row['date'])] = row['bps']
    annual_pivot.at[row['isin'], 'close_'+str(row['date'])] = row['close']
annual_pivot = annual_pivot.sort_index(axis=1, ascending=False)

# print(annual_pivot.loc[['JP3942600002']])

# --- BLOCK 2 - interpolation the data based on 7 years
#                  name          isin  fun_pk   eps_mean  dps_mean   cps_mean    bps_mean  value_mean  eps_slope  dps_slope  cps_slope  bps_slope  value_slope
# ts_pk
# 2      Cabot Oil & Gas  US1270971039       1   1.970037  1.564203   3.360635   12.347053   18.408167   1.049473   0.566317   0.803749   2.399210    -1.158063
# 3        Goldman Sachs  US38141G1040       2  16.010493  2.957065  11.065701  209.188488  195.111333   1.981601   0.363350  -0.181399   8.182896     2.251327

pks = get_edcbps_history()
pks.date = pd.to_datetime(pks.date)         # date becomes datetime
pks['dps'] = pks['dps'].fillna(0)           # missing dividends are set to zero
pks['date_ordinal'] = pd.to_datetime(pks['date']).map(dt.datetime.toordinal)
    # toordinal = integer for linearregression

# print(pks)

selected_columns = pks[["isin"]]
interpolate = selected_columns.copy()
interpolate = interpolate.drop_duplicates()

pks = pks.drop(['symbol', 'symbol_fundamental'], axis=1)
grouped_pks = pks.groupby("isin")          # grouping by ts_pk
# print(grouped_pks.mean().head(10))

interpolate = pd.merge(interpolate, grouped_pks.mean(), on='isin')
interpolate = interpolate.drop(columns=['date_ordinal'])
interpolate = interpolate.rename(columns={'eps': 'eps_mean', 'dps': 'dps_mean', 'cps': 'cps_mean', \
    'bps': 'bps_mean', 'close': 'close_mean'})
# print(interpolate.head(10))

# apply linear regresion using numpy
def linregress(x, y):
    '''linear regression using numpy starting from two one dimensional numpy arrays'''
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return pd.Series({'slope':slope, 'intercept': intercept})

# print(interpolate.loc[interpolate['isin'] == 'JP3942600002'])

res = pks[pks.eps.notnull()].groupby('isin').apply(lambda x: linregress(x.date_ordinal, x.eps))
if not res.empty:
    res = res.drop(columns=['intercept'])
    res['slope'] = res['slope']*365
    res = res.rename(columns={'slope':'eps_slope'})
    interpolate = pd.merge_ordered(interpolate, res, on='isin',  fill_method=None)

res = pks[pks.dps.notnull()].groupby('isin').apply(lambda x: linregress(x.date_ordinal, x.dps))
if not res.empty:
    res = res.drop(columns=['intercept'])
    res['slope'] = res['slope']*365
    res = res.rename(columns={'slope':'dps_slope'})
    interpolate = pd.merge_ordered(interpolate, res, on='isin',  fill_method=None)

res = pks[pks.cps.notnull()].groupby('isin').apply(lambda x: linregress(x.date_ordinal, x.cps))
if not res.empty:
    res = res.drop(columns=['intercept'])
    res['slope'] = res['slope']*365
    res = res.rename(columns={'slope':'cps_slope'})
    interpolate = pd.merge_ordered(interpolate, res, on='isin',  fill_method=None)

res = pks[pks.bps.notnull()].groupby('isin').apply(lambda x: linregress(x.date_ordinal, x.bps))
if not res.empty:
    res = res.drop(columns=['intercept'])
    res['slope'] = res['slope']*365
    res = res.rename(columns={'slope':'bps_slope'})
    interpolate = pd.merge_ordered(interpolate, res, on='isin',  fill_method=None)

res = pks.groupby('isin').apply(lambda x: linregress(x.date_ordinal, x.close))
if not res.empty:
    res = res.drop(columns=['intercept'])
    res['slope'] = res['slope']*365
    res = res.rename(columns={'slope':'close_slope'})
    interpolate = pd.merge_ordered(interpolate, res, on='isin')

interpolate = interpolate.set_index('isin')

# --- BLOCK 3 - get the last value
last_value = get_mysql_data('quote_eur_last')
last_value = last_value.set_index('symbol')

# --- BLOCK 4 - get the lookup table - the items to provide
lookup = get_mysql_data('referencedata')
lookup = lookup.set_index('symbol')

# --- MERGE BLOCK 2 & 3 // & 1 // & 4
result = pd.merge(lookup, last_value, left_index=True, right_index=True)
result = result.drop(columns=['currency_x', 'longTimeSerie', 'comment', 'created_x', \
    'updated_x', 'open', 'high', 'low', 'created_y', 'checked'])
result = result.reset_index()
result = result.set_index('isin')

result = pd.merge(result, interpolate, how='left', left_index=True, right_index=True)
result = pd.merge(result, annual_pivot, how='left', left_index=True, right_index=True)

result = result.rename(columns={'currency_y': 'currency', 'updated_y': 'updated'})

result = result.reset_index()
put_dataframe_to_table(result, 'validation_board')

writeLog(LOG_FILE,'validate board stopped', id = 'VAB')    # log-stop
