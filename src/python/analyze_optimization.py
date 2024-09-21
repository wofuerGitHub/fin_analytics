"""portfolio optimization"""

#!/usr/bin/python3

import numpy as np                                              # numpy
import pandas as pd                                             # pandas

from mylib.writeLog import writeLog                             # write log
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

from mylib.investment_db import get_portfolio
from mylib.investment_db import get_quote_eur_timeserie
from mylib.investment_db import put_dataframe_to_table

# import matplotlib.pyplot as plt

LOG_FILE = './analytics.log'                                   # load log-file

writeLog(LOG_FILE,'Portfolio optimization started', id = 'POP') # log-start

# 1.    load portfolio & all data
# 2.    portfolio calulation of
# 2.1   - percentage within portfolio
# 2.2   - overall portfolio virtual performance
# 2.3   - recommanded share within the portfolio
# 3.    store complete table
    # isin, share, percentage, performance, vola, recommanded percentage

# 1.    load portfolio

portfolio = get_portfolio()
print(portfolio)

# 2.    portfolio calulation of
# 2.1   - percentage within portfolio

price = []
perf = []
vola = []
sr = []
ts_portfolio = pd.DataFrame(columns=['date'])
ts_portfolio.set_index('date', inplace=True)

for index, row in portfolio.iterrows():
    print(row['isin'], row['companyName'], row['symbol'], row['all'])       # print info
    ts = get_quote_eur_timeserie(row['symbol'])
   
    ts.date = pd.to_datetime(ts.date)
    ts.set_index('date', inplace=True)
    ts_normalized = standardizeTimeSerie(ts, 'endDate-1year', 'today')      # standardize ts to one-year
    if row['all'] > 0:
        ts_normalized = ts_normalized*row['all']
    else:
        ts_normalized = ts_normalized/ts_normalized.iloc[0]/10

    ts_portfolio[row['symbol']] = ts_normalized.close.copy()
portfolio.set_index('symbol', inplace=True)                                 # perf, vola, sr per equity


# pvs = performanceAndVolaAndSR(ts_portfolio, 1)
# portfolio['perf'] = pd.DataFrame(pvs[0])
# portfolio['vola'] = pd.DataFrame(pvs[1])
# portfolio['sr'] = pd.DataFrame(pvs[2])

ts_portfolio.loc[:,'total'] = ts_portfolio.sum(numeric_only=True, axis=1)   # sum of portfolio

portfolio['share'] = ts_portfolio.iloc[0]/ts_portfolio.iloc[0].iloc[-1]     # share of portfolio as of the last date
# portfolio['share'] = ts_portfolio.iloc[-1]/ts_portfolio.iloc[-1].iloc[-1] # share of portfolio as of the first date

pvs = performanceAndVolaAndSR(ts_portfolio['total'], 1)                     # pvs of portfolio
portfolio['perf_all'] = pvs[0]
portfolio['vola_all'] = pvs[1]
portfolio['sr_all'] = pvs[2]

# normalize every item to start value & start optimization calculation
ts_portfolio = ts_portfolio/ts_portfolio.iloc[-1]

perf = ts_portfolio.iloc[:0,:].copy()                                       # dataframe for performance, vola and sr
vola = ts_portfolio.iloc[:0,:].copy()
sr = ts_portfolio.iloc[:0,:].copy()

steps = np.concatenate([np.arange(0,.1,.001),np.arange(.1,1.01,.01)])       # iterate through change of investigated element vs. portfolio
for i in steps:
    pvs = performanceAndVolaAndSR((i*ts_portfolio).add(ts_portfolio.total*(1-i), axis = 0),1)
    perf = perf._append(pvs[0], ignore_index = True)
    vola = vola._append(pvs[1], ignore_index = True)
    sr = sr._append(pvs[2], ignore_index = True)

perf.index = steps                                                          # change the index of dataframes to split
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

put_dataframe_to_table(portfolio, 'validation_optimization')

# plt.plot(vola, perf)
# plt.legend(portfolio['name'])
# plt.show()

writeLog(LOG_FILE,'Portfolio optimization stopped', id = 'POP')    # log-stop
