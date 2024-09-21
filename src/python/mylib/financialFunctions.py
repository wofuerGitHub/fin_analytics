#!/usr/bin/python3

# financialFunctions.py
# set of financial functions
# 12.04.2022

import pandas as pd
import numpy as np
from datetime import datetime, date

def standardizeTimeSerie(timeSerie, startDate = 'first', endDate = 'last'):
    """
    Standardize time-series based on business-days and fill up days in advance or at the end.
    The order of the time-series is secured.

    Parameters

    startDate:str or date-time like  
        'first' to pick the first date of the time series / 'today-1year' / date in format YYYY-MM-DD / datetime-like
    endDate:str or date-time like     
        'last' to pick the last date of the time series / 'today' / date in format YYYY-MM-DD / datetime-like  
    """
    if timeSerie.index[0] <= timeSerie.index[-1]:
        ascendingOrder = True
    else:
        ascendingOrder = False

    timeSerie.sort_index(ascending=True, inplace=True) # sort index ascending
    
    if endDate == 'last':               # if endDate = 'last', use idx[-1]-date 
        endDate = timeSerie.index[-1]
    elif endDate == 'today':              # if endDate = 'today', use todays-date
        now = datetime.now()
        endDate = date(year = now.year, month = now.month, day = now.day)
    else:
        endDate = datetime.strptime(endDate, "%Y-%m-%d")

    
    if startDate == 'first':            # if startDate = 'first', use idx[0]-date
        startDate = timeSerie.index[0]
    elif startDate == 'today-1year':      # if startDate = 'today-1year', use todays-date minus 1 year
        now = datetime.now()
        startDate = date(year = now.year-1, month = now.month, day = now.day)
    elif startDate == 'endDate-1year':      # if startDate = 'endDate-1year', use endDate-date minus 1 year
        startDate = date(year = endDate.year-1, month = endDate.month, day = endDate.day)
    else:
        startDate = datetime.strptime(startDate, "%Y-%m-%d")
    
    timeSerie = timeSerie.resample('D').ffill()           # generate sample size one-day and fill-forward missing elements / 'D' = calender day
    selection = pd.date_range(startDate, endDate, freq='B') # generate selection from startDate to endDate with weekdays / 'B' business weekday
    timeSerie = timeSerie.asof(selection)                 # get subset of ts according selection and interpolate remaining ()
    # timeSerie = timeSerie.fillna(method='bfill')                       # fill-up also dates before the first original one
    timeSerie = timeSerie.bfill()                       # fill-up also dates before the first original one
    timeSerie.sort_index(ascending = ascendingOrder, inplace = True)    # ensure descending sorting (idx 0 = newest date)
    return timeSerie

def performanceAndVolaAndSR(timeSerie, years = 1):
    """
    Calculate performance, volatility and sharpe-ratio on an annual base.
    In Case the period is requested period is longer than the first date of the
    timeSerie it will return "False"

    Parameters

    years:int
        number of years to normalize, default = 1
    """
    if timeSerie.index[0] <= timeSerie.index[-1]:
        ascendingOrder = True
    else:
        ascendingOrder = False    
    
    timeSerie.sort_index(ascending = True, inplace = True)                              # sort index ascending
    max_date = max(timeSerie.index)                                                     # max. date within index
    min_date = max(timeSerie.index)
    min_date += pd.DateOffset(days = 1)
    if max_date.isoweekday() == 5:                                                      # case 'friday', max_date = 'monday'
        min_date += pd.DateOffset(days = 3)
    if max_date.isoweekday() == 6:                                                      # case 'saturday', max_date = 'monday'
        min_date += pd.DateOffset(days = 2)
    if max_date.isoweekday() == 7:                                                      # case 'sunday', max_date = 'monday'
        min_date += pd.DateOffset(days = 1)                
    min_date -= pd.DateOffset(years = years)                                            # min. date calculated on param
    if min_date >= min(timeSerie.index):                                                # if ts is sufficient
        delta = np.log(timeSerie.loc[min_date:max_date].pct_change()+1)                 # calculate based on log to dampen outliner
        # performance = (np.power(np.power(1+np.mean(delta),len(delta)),1/years)-1)*100   # performance (annualized)
        performance = (np.power(np.power(1+np.mean(delta, axis = 0),len(delta)),1/years)-1)*100
        vola = np.std(delta, axis = 0)*np.sqrt(len(delta))*100/np.sqrt(years)                     # vola (annualized)
        sharpeRatio = performance/vola                                                   # sharpe-ratio (annualized)
        timeSerie.sort_index(ascending = ascendingOrder, inplace = True)                # ensure descending sorting (idx 0 = newest date)
        return performance, vola, sharpeRatio
    timeSerie.sort_index(ascending = ascendingOrder, inplace = True)                    # ensure descending sorting (idx 0 = newest date)
    return False
    