"""portfolio optimization"""

# --- concept 
# 1.    load portfolio
# 2.    load timeseries & additonal parameters
# 3.    first optimization: sharpe ratio
# 3.1   calculate performance, vola, sharpe ratio
# 3.2   calculate optimal portfolio based on sharpe ratio
# 4.    de-compose optimal sharpe ratio in performance and vola
# 5.    second optimization: around optimal sharpe ratio incude other parameters
# 5.1   normalize parameters, like e.g. 1/opt_perf*perf + 1/opt_vola*vola + 1/target_dividend*dividend + 1/target_bookvalue*bookvalue + 1/target_eps*eps
# 5.2   calculate optimal portfolio based on parameter set 

#!/usr/bin/python3

import numpy as np                                              # numpy
import pandas as pd                                             # pandas

from mylib.writeLog import writeLog                             # write log
from mylib.financialFunctions import standardizeTimeSerie       # standardize ts
from mylib.financialFunctions import performanceAndVolaAndSR    # caluclate performance, vola, sr

from mylib.investment_db import get_portfolio                   # get portfolio
from mylib.investment_db import get_quote_eur_timeserie
from mylib.investment_db import get_last_earning_price_ratio
from mylib.investment_db import get_last_bookvalue_price_ratio
from mylib.investment_db import put_dataframe_to_table

import scipy.optimize as opt

# [DEBUG]
# import matplotlib
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')
# matplotlib.use( 'tkagg' )

LOG_FILE = './analytics.log'                                    # load log-file

writeLog(LOG_FILE,'Portfolio optimization started', id = 'PO2') # log-start

# 1.    load portfolio

print('load portfolio')

my_portfolio = get_portfolio()                                              # load portfolio
my_portfolio = my_portfolio[my_portfolio['all'] != 0]                       # remove all = 0 / assets not in portfolio

print(my_portfolio)                                                            # print portfolio

# 2.    load timeseries
print('\nload timeseries')

price = []                                                                  # price per equity
perf = []                                                                   # performance per equity
vola = []                                                                   # vola per equity
sr = []                                                                     # sharpe ratio per equity
ts_portfolio = pd.DataFrame(columns=['date'])                               # portfolio timeserie
ts_portfolio.set_index('date', inplace=True)                                # set index to date
for index, row in my_portfolio.iterrows():                                     # iterate over portfolio
    print(row['isin'], row['companyName'], row['symbol'], row['all'])       # print info
    ts = get_quote_eur_timeserie(row['symbol'])                             # get timeserie
   
    ts.date = pd.to_datetime(ts.date)                                       # convert date to datetime 
    ts.set_index('date', inplace=True)                                      # set index to date
    ts_normalized = standardizeTimeSerie(ts, 'endDate-1year', 'today')      # standardize ts to one-year
    if row['all'] > 0:                                                      # all = number off assets
        ts_normalized = ts_normalized*row['all']                            # calculate the volume of the asset within the portfolio
    else:
        ts_normalized = ts_normalized/ts_normalized.iloc[0]/10              # sets the value to 0.1 of the last value to ensure it is part of the portfolio with a small share

    ts_portfolio[row['symbol']] = ts_normalized.close
my_portfolio.set_index('symbol', inplace=True)                                 # set index to symbol

# print(ts_portfolio)                                                       # complete ts of the assets and tota;

#             ANDR.VI   BEI.DE   BMW.DE     EXSA.DE  LEN.DE       OMV.DE       STR.VI   VAS.DE   VIG.VI
# date                                                                                                 
# 2023-05-24  7235.80  7643.20  5927.20  15880.2655  4725.6  4224.350000  7422.700000  5266.80  6076.00
# 2023-05-23  7235.80  7643.20  5927.20  15880.2655  4725.6  4224.350000  7422.700000  5266.80  6076.00
# ...             ...      ...      ...         ...     ...          ...          ...      ...      ...
# 2022-05-25  5147.34  6466.80  4870.10  15534.0725  5563.8  5005.199854  8168.949841  4222.68  5549.25
# 2022-05-24  5106.20  6485.84  4822.98  15428.7870  5478.0  5005.199854  8288.350298  4167.24  5500.25

# [262 rows x 9 columns]

ts_portfolio = ts_portfolio.sort_index(axis=0)                              # sort by date (ascending)
ts_total = ts_portfolio.sum(numeric_only=True, axis=1)   # sum of portfolio

pvs = performanceAndVolaAndSR(ts_portfolio, 1)                              # performance, vola and sharpe ratio of every item
my_portfolio['perf'] = pd.DataFrame(pvs[0])
my_portfolio['vola'] = pd.DataFrame(pvs[1])
my_portfolio['sr'] = pd.DataFrame(pvs[2])

for index, row in my_portfolio.iterrows():                                  # iterate over portfolio and add earning price ratio
    try:
        epr = get_last_earning_price_ratio(index)
        if np.isnan(epr['epr'][0]):
            my_portfolio.loc[index,'epr'] = 0
        else:
            my_portfolio.loc[index,'epr'] = epr['epr'][0]
    except:
        my_portfolio.loc[index,'epr'] = 0

for index, row in my_portfolio.iterrows():                                  # iterate over portfolio and add earning price ratio
    try:
        bpr = get_last_bookvalue_price_ratio(index)
        if np.isnan(bpr['bpr'][0]):
            my_portfolio.loc[index,'bpr'] = 0
        else:
            my_portfolio.loc[index,'bpr'] = bpr['bpr'][0]
    except:
        my_portfolio.loc[index,'bpr'] = 0

my_portfolio['start_weight'] = ts_portfolio.iloc[0]/ts_total.iloc[0]     # share of portfolio as of the first date
my_portfolio['end_weight'] = ts_portfolio.iloc[-1]/ts_total.iloc[-1]     # share of portfolio as of the last date

# --- limits for the optimization for individual shares

share_min = min(1/len(my_portfolio)/2,0.0025)                                # min. 0.25% of indiviual asset or 1/2 times a portfolio asset
share_max = max(1/len(my_portfolio)*2,0.03)                                  # max. 3.00% of indiviual asset or 2 times a portfolio asset

# --- optimization for sharpes ratio only


# Kudo to https://medium.datadriveninvestor.com/portfolio-optimization-with-python-using-scipy-optimize-monte-carlo-method-a5b4e89e0548



def calc_returns(price_data, resample=None, ret_type="arithmatic"):         # calculate returns
    """
    Parameters
        price_data: price timeseries pd.DataFrame object.
        resample:   DateOffset, Timedelta or str. `None` for not resampling. Default: None
                    More on Dateoffsets : https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
        ret_type:   return calculation type. \"arithmatic\" or \"log\"

    Returns:
        returns timeseries pd.DataFrame object
    """
    if ret_type=="arithmatic":
        ret = price_data.pct_change().dropna()
    elif ret_type=="log":
        ret = np.log(price_data/price_data.shift()).dropna()
    else:
        raise ValueError("ret_type: return calculation type is not valid. use \"arithmatic\" or \"log\"")

    if resample != None:
        if ret_type=="arithmatic":
            ret = ret.resample(resample).apply(lambda df: (df+1).cumprod(axis=0).iloc[-1]) - 1
        elif ret_type=="log":
            ret = ret.resample(resample).apply(lambda df: df.sum(axis=0))
    return(ret)
def calc_returns_stats(returns):                                            # calculate mean returns and covariance matrix
    """
    Parameters
        returns: returns timeseries pd.DataFrame object

    Returns:
        mean_returns: Avereage of returns
        cov_matrix: returns Covariance matrix
    """
    mean_returns = returns.mean(axis=0)
    cov_matrix = returns.cov()
    return(mean_returns, cov_matrix)
def portfolio(weights, mean_returns, cov_matrix):                           # calculate portfolio return, variance and std
    portfolio_return = np.dot(weights.reshape(1,-1), mean_returns.values.reshape(-1,1))
    portfolio_var = np.dot(np.dot(weights.reshape(1,-1), cov_matrix.values), weights.reshape(-1,1))
    portfolio_std = np.sqrt(portfolio_var)

    return(np.squeeze(portfolio_return),np.squeeze(portfolio_var),np.squeeze(portfolio_std))

daily_ret = calc_returns(ts_portfolio, resample=None, ret_type="log")       # calculate daily returns
mean_returns, cov_matrix = calc_returns_stats(daily_ret)                    # calculate mean returns and covariance matrix

# print(mean_returns)
# print(cov_matrix)

# functions to minimize
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):  # calculate negative sharpe ratio
    portfolio_return, portfolio_var, portfolio_std = portfolio(weights, mean_returns, cov_matrix)
    sr = ((portfolio_return - risk_free_rate)/portfolio_std) * (252**0.5) # annualized
    return(-sr)
def optimize_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate=0, w_bounds=(0,1)):
    "This function finds the portfolio weights which minimize the negative sharpe ratio"

    init_guess = np.array([1/len(mean_returns) for _ in range(len(mean_returns))])
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    result = opt.minimize(fun=neg_sharpe_ratio,
                          x0=init_guess,
                          args=args,
                          method='SLSQP',
                          bounds=tuple(w_bounds for _ in range(len(mean_returns))),
                          constraints=constraints,
                          )
    
    if result['success']:
        print(result['message'])
        opt_sharpe = - result['fun']
        opt_weights = result['x']
        opt_return, opt_variance, opt_std = portfolio(opt_weights, mean_returns, cov_matrix)
        return(opt_sharpe, opt_weights, opt_return.item()*252, opt_variance.item()*252, opt_std.item()*(252**0.5))
    else:
        print("Optimization was not succesfull!")
        print(result['message'])
        return(None)
    
# max sharpe portfolio
opt_sharpe, opt_weights, opt_return, opt_variance, opt_std = optimize_sharpe_ratio(
                                                                mean_returns,
                                                                cov_matrix,
                                                                risk_free_rate=0, w_bounds=(share_min, share_max))
my_portfolio['opt_sr'] = opt_weights

# --- optimize portfolio for linear in addition (e.g. earnings, bookvalue) --> latest information on the assets

# functions to minimize
def neg_performance_linear_weight(weights, mean_returns, cov_matrix, linear, linear_weight = 1, risk_free_rate = 0):  # calculate negative sharpe ratio
    portfolio_return, portfolio_var, portfolio_std = portfolio(weights, mean_returns, cov_matrix)
    opt = portfolio_return*100*252 + np.dot(weights, linear)*linear_weight # S&P long term perf ~ 7% / epr ~ 0.066 --> factor 105 = long term equality
    return(-opt)

def optimize_performance_linear_weight(mean_returns, cov_matrix, linear, linear_weight, risk_free_rate=0, w_bounds=(0,1)):  # optimize for performance and epr
    "This function finds the portfolio weights which minimize the negative sharpe ratio"

    init_guess = np.array([1/len(mean_returns) for _ in range(len(mean_returns))])
    args = (mean_returns, cov_matrix, linear, linear_weight, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    result = opt.minimize(fun=neg_performance_linear_weight,
                          x0=init_guess,
                          args=args,
                          method='SLSQP',
                          bounds=tuple(w_bounds for _ in range(len(mean_returns))),
                          constraints=constraints,
                          )
    
    if result['success']:
        print(result['message'])
        opt_sharpe = - result['fun']
        opt_weights = result['x']
        opt_return, opt_variance, opt_std = portfolio(opt_weights, mean_returns, cov_matrix)
        return(opt_sharpe, opt_weights, opt_return.item()*252, opt_variance.item()*252, opt_std.item()*(252**0.5))
    else:
        print("Optimization was not succesfull!")
        print(result['message'])
        return(None)
    
# max sharpe portfolio & epr
opt_sharpe, opt_weights, opt_return, opt_variance, opt_std = optimize_performance_linear_weight(
                                                                mean_returns,
                                                                cov_matrix,
                                                                my_portfolio['epr'],
                                                                155,                       # S&P long term perf ~ 7% / epr ~ 0.066 --> factor 7 / 0.066 = 105 = long term equality
                                                                risk_free_rate=0, 
                                                                w_bounds=(share_min, share_max))
my_portfolio['opt_perf_epr'] = opt_weights

# max shapre portfolio & bpr
opt_sharpe, opt_weights, opt_return, opt_variance, opt_std = optimize_performance_linear_weight(
                                                                mean_returns,
                                                                cov_matrix,
                                                                my_portfolio['bpr'],
                                                                30,                       # S&P long term perf ~ 7% / bpr ~ 1/2.81 = 0.35 --> factor 7 / 0.35 = 20 = long term equality
                                                                risk_free_rate=0, 
                                                                w_bounds=(share_min, share_max))
my_portfolio['opt_perf_bpr'] = opt_weights


# --- putting the results together
my_portfolio_opt = pd.DataFrame()
variation = ['start_weight', 'end_weight', 'opt_sr', 'opt_perf_epr', 'opt_perf_bpr']
for x in variation:
    performance, variance, standard_deviation = portfolio(my_portfolio[x].values, mean_returns, cov_matrix)
    # print('PVS - '+x, performance*100*252, standard_deviation*100*(252**0.5), performance*(252**.5)/standard_deviation, np.dot(my_portfolio[x], my_portfolio['epr']),  1/np.dot(my_portfolio[x], my_portfolio['epr']))
    append_dict = {'name':x, 'perf':performance*100*252, 'vola': standard_deviation*100*(252**0.5), 'sr':performance*(252**.5)/standard_deviation, 'epr': np.dot(my_portfolio[x], my_portfolio['epr']), 'per':1/np.dot(my_portfolio[x], my_portfolio['epr']), 'bpr': np.dot(my_portfolio[x], my_portfolio['bpr']), 'pbr':1/np.dot(my_portfolio[x], my_portfolio['bpr'])}
    temp = pd.DataFrame({k:[v] for k,v in append_dict.items()})
    my_portfolio_opt = pd.concat([my_portfolio_opt,temp],ignore_index=True)
my_portfolio_opt.set_index('name', inplace=True) 
my_portfolio.sort_values(by=['sr'], inplace=True, ascending=False)

my_portfolio = my_portfolio.reset_index()
my_portfolio_opt = my_portfolio_opt.reset_index()

print(my_portfolio)
print(my_portfolio_opt)

put_dataframe_to_table(dataframe = my_portfolio, table = 'portfolio')
put_dataframe_to_table(dataframe = my_portfolio_opt, table = 'portfolio_opt')

# [DEBUG]
# plot portfolio.perf against portfolio.vola
# plt.scatter(my_portfolio.vola, my_portfolio.perf, color='red')              # individual stocks
# plt.scatter(my_portfolio_opt.vola, my_portfolio_opt.perf, color='blue')                        # original portfolio   
# plt.xlabel('vola')
# plt.ylabel('perf')
# plt.show()

writeLog(LOG_FILE,'Portfolio optimization stopped', id = 'PO2') # log-end