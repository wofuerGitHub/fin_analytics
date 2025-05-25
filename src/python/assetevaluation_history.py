#!/usr/bin/python3

"""
File: asssetevaluation.py
Author: Wolfgang Fuerst
Date: 2025-02-09
Description: Evaluate the true value of all assets
Structure:
    Load config file
    Load fundamental and timeserie-data
    Calculate intrinsic value
    Save data
    Wait according config
Issues:
    ...
Runtime: 
    ...
Args:
    None
"""
import datetime as dt
import json
import time                                                     # requ. to wait
import pandas as pd                                             # pandas
import numpy as np                                              # numpy

from scipy.optimize import curve_fit                            # interpolate
import matplotlib.pyplot as plt                                 # plot charts

from mylib import config                                        # read configuration-data
from mylib.writeLog import writeLog                             # write log file
from mylib import mysql_db                                      # database connection

# basic config

# end_date = dt.datetime.now().strftime('%Y-%m-%d')
end_date = '2023-10-01'

METHOD = "assetevaluation"
LOG_TEXT = ' asset evaluation'

# load config file & write log entry for start
CONFIG = config.load_config('config.json')["analytics"]
log_id = CONFIG[METHOD]['log_id']
log_text = LOG_TEXT
writeLog(CONFIG['file']['log'], 'Start'+log_text+'', id = log_id)

# functions for calculation

### FUNCTIONS START ###

def trend(known_data_y, known_data_x, new_data_x):
    """TREND - linear approximation"""
    if len(known_data_y[:]) > 0:
        polynomial_coefficients = np.polyfit(known_data_x, known_data_y, 1)
        f = np.poly1d(polynomial_coefficients)
        return f(new_data_x)
    else:
        return np.nan

def growth(known_data_y, known_data_x, new_data_x):
    """GROWTH - exponential approximation"""
    if len(known_data_y[:]) > 0:
        if min(known_data_y[:]) > 0:
            def func(x, a, b):
                return a*np.power(b,x/365)              # a*np.power(b,x/365)
            a = max(0.01, np.mean(known_data_y))        # min eps 0.1
            b = 1                                       # with a growth of 0% [-50% ... +50%] annual
            # print(a, b, c)
            popt, pcov = curve_fit(func, known_data_x, known_data_y, p0 = (a, b), \
                                bounds = ([-np.inf, .5], [np.inf, 1.5]), maxfev= 10000)
            # print(popt)
            # print(pcov)
            # print(np.sqrt(np.diag(pcov)))
            return func(new_data_x, *popt)
        else:
            return np.nan
    else:
        return np.nan

def last_percent(known_data_y, known_data_x, new_data_x, percent):
    """LAST-X% - exponential growth on the last 3 eps values"""
    # idx = max(known_data_y.index)
    def func(x, a, b, c):
        return a*np.power(b,(x-c)/365)
    a = np.mean(known_data_y[-3:])
    b = 1 + percent/100
    c = np.mean(known_data_x[-3:])
    return func(new_data_x, a, b, c)

def average_item(known_data_y, known_data_x, new_data_x, number_of_items):
    """AVERAGE - x points average forward evaluation"""
    return np.mean(known_data_y[-number_of_items:])

def rsq(known_data_x, known_data_y):
    """RSQ - root square"""
    if len(known_data_y[:].dropna()) > 0:
        corr_matrix = np.corrcoef(known_data_x, known_data_y)
        corr = corr_matrix[0,1]
        return corr**2
    else:
        return np.nan

### FUNCTIONS END ###

# setup the connection to the source database
mysql_db.set_configuration(**CONFIG["database"])
sql_engine = mysql_db.create_sql_engine(mysql_db.get_configuration())

# getting complete reference data

try:
    connection_to_source = sql_engine.connect()
    source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_reference"])
    result_table = mysql_db.get_mysql_data(connection_to_source, source, \
                                        columns = CONFIG[METHOD]["columns_source_reference"], \
                                        order_by = "symbol", order_desc = False)
    connection_to_source.close()
except:
    writeLog(CONFIG['file']['log'], 'Error reading symbols from source', id = log_id)

# DEBUG print(data)
# result_table = result_table.loc[166:]
# result_table = result_table.loc[790:]

for row in result_table.itertuples():

    companyName = row.companyName
    symbol = row.symbol
    symbol_fundamental = row.symbol_fundamental
    print(companyName, symbol)
    debug_message = ''+companyName+' : '+symbol+'\n'

    # getting historical edcbps values
    if symbol_fundamental is not None:
        try:
            connection_to_source = sql_engine.connect()
            source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_edcbps"])
            ts = mysql_db.get_mysql_data(connection_to_source, source, \
                                        columns = CONFIG[METHOD]["columns_source_edcbps"], \
                                        filter_symbol = symbol_fundamental, \
                                        filter_end_date = end_date, \
                                        order_by = "date", \
                                        order_desc = True, limit = 10)
            connection_to_source.close()
        except:
            debug_message = debug_message + 'Could not query edcbps_eur\n'
            print(debug_message)
            continue
        ts = ts.dropna() # deleting NaN eps rows

    # getting actual eps value
    try:
        connection_to_source = sql_engine.connect()
        source = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_source_ts"])
        query_result = mysql_db.get_mysql_data(connection_to_source, source, \
                                            columns = CONFIG[METHOD]["columns_source_ts"], \
                                            filter_symbol = symbol, \
                                            filter_end_date = end_date, \
                                            order_by = "date", \
                                            order_desc = True, limit = 1)
        connection_to_source.close()
        ts_last = query_result[['date','eps']]
        close = query_result.at[0,'close']
    except:
        debug_message = debug_message + 'Could not query ts_eur\n'
        print(debug_message)
        continue

    if ts_last['eps'].any() == 0:   # catch items that have no actual eps like Gold --> 0.0
        ts_last.loc[:, 'eps'] = np.nan
        debug_message = debug_message + 'Catch eps = 0.0\n'

    if symbol_fundamental is not None:
        ts = pd.concat(df.dropna(axis=1, how='all') for df in [ts_last, ts])
        # hint: ts = pd.concat([ts_last, ts]) issues with NaN only ts_last
    else:
            ts = ts_last
    ts.loc[:, 'date'] = pd.to_datetime(ts['date'], format='%Y%m%d')

    # adding the future
    ts_future = pd.DataFrame()
    ts_future['date'] = pd.date_range(start = \
        dt.date(max(ts_last['date']).year+1, max(ts_last['date']).month, \
            max(ts_last['date']).day), \
            periods = 20, freq = "365d") # approx. 1 year intervals

    ts_future = pd.concat([ts_future, ts])
    ts_future['eps*'] = ts_future['eps']
    ts_future['date_ordinal'] = pd.to_datetime(ts_future['date']).map(dt.datetime.toordinal)
    ts_future.sort_values('date_ordinal', inplace = True)
    ts_future.reset_index(drop = True, inplace = True)
    # ts_future['date'] = ts_future['date'].dt.strftime('%Y-%m-%d')

    if len(ts_future['eps'].dropna()) < 11:
        years = 11 - len(ts_future['eps'].dropna())
        ts_past = pd.DataFrame()
        ts_past['date'] = pd.date_range(start = \
            dt.date(min(ts_future['date']).year-years, min(ts_future['date']).month, \
                    min(ts_future['date']).day), \
                    periods = years, freq = "365d") # approx. 1 year intervals
        ts_past['eps'] = ts_future.loc[0,'eps']
        ts_past['eps*'] = ts_future.loc[0,'eps*']
        ts_past['date_ordinal'] = pd.to_datetime(ts_past['date']).map(dt.datetime.toordinal)
        ts_future = pd.concat([ts_future, ts_past])
        ts_future.sort_values('date_ordinal', inplace = True)
        ts_future.reset_index(drop = True, inplace = True)
        debug_message = debug_message + 'Catch insuficient amount (<11) of fundamental values\n'

    # eps* eleminating single negative data
    if len(ts_future.loc[ts_future['eps'] <= 0]) == 1:                      # one negative value
        idx = ts_future.loc[ts_future['eps'] <= 0].index
        if (idx >= 1) & (idx <= max(ts_future['eps'].dropna().index)-1):    # idx: first+1,last-1
            eps_est = (ts_future.iloc[idx-1]['eps'].values[0] +\
                    ts_future.iloc[idx]['eps'].values[0] + \
                    ts_future.iloc[idx+1]['eps'].values[0])/3
            ts_future.loc[idx-1, 'eps*'] = eps_est
            ts_future.loc[idx, 'eps*'] = eps_est
            ts_future.loc[idx+1, 'eps*'] = eps_est
        if idx == max(ts_future['eps'].dropna().index):
            eps_est = (ts_future.iloc[idx-1]['eps'].values[0] +\
                    ts_future.iloc[idx]['eps'].values[0])/2
            ts_future.loc[idx-1, 'eps*'] = eps_est
            ts_future.loc[idx, 'eps*'] = eps_est
        if idx == 0:
            eps_est = (ts_future.iloc[idx+1]['eps'].values[0] +\
                    ts_future.iloc[idx]['eps'].values[0])/2
            ts_future.loc[idx+1, 'eps*'] = eps_est
            ts_future.loc[idx, 'eps*'] = eps_est
        debug_message = debug_message + 'Corrected 1 eps value <= 0 \n'

    ts_future['date_ordinal'] = ts_future['date_ordinal'] - min(ts_future['date_ordinal'])
    ts = ts_future.iloc[ts_future['eps'].dropna().index]    # ts of the ones with eps values

    # TREND - calculating the trend (allways successfull)
    ts_future['TREND'] = np.round(trend(ts['eps'], \
                                        ts['date_ordinal'], ts_future['date_ordinal']),3)

    # 7Y-AVG - calculating the average of the last 7 years (always successfull)
    ts_future['7Y-AVG'] = np.round(average_item(ts['eps'], \
                                        ts['date_ordinal'], ts_future['date_ordinal'], 7), 3)

    # GROWTH - calculating growth (might fail based on negative eps values)
    ts_future['GROWTH'] = np.round(growth(ts['eps'], \
                                        ts['date_ordinal'], ts_future['date_ordinal']),3)

    # GROWTH* - calculating growth* with corrected eps values (might fail on negative eps values)
    ts_future['GROWTH*'] = np.round(growth(ts['eps*'], \
                                        ts['date_ordinal'], ts_future['date_ordinal']),3)

    # LAST-x% - putting in relation the last change to the average go on based on this [-33%,8%]
    try:
        percent = min(8, (ts_future.iloc[max(ts_future['eps'].dropna().index)+1]['TREND'] \
                        - ts_future.iloc[max(ts_future['eps'].dropna().index)]['TREND']) \
                        / np.abs(ts_future.iloc[max(ts_future['eps'].dropna().index)]['7Y-AVG']) \
                        * 100)
        percent = max(percent, -33)
        ts_future['LAST-X%'] = np.round(last_percent(ts['eps'], ts['date_ordinal'], \
                                                    ts_future['date_ordinal'], percent), 3)
    except:
        percent = np.nan
        ts_future['LAST-X%'] = np.nan

    # LAST-8% - calculating growth of 8% with the last 3 values (always successful)
    ts_future['LAST-8%'] = np.round(last_percent(ts['eps'], ts['date_ordinal'], \
                                                 ts_future['date_ordinal'], 8), 3)

    result = {}
    try:
        idx = max(ts_future['eps'].dropna().index)
    except:
        idx = 10
    investment_types = ['TREND', 'GROWTH', 'GROWTH*', 'LAST-X%', 'LAST-8%', '7Y-AVG']
    for type in investment_types:
        result[type] = {}
        if type == 'LAST-X%':
            result[type]['Value'] = percent
        else:
            result[type]['Value'] = np.round((ts_future.iloc[idx+1][type] \
                                            - ts_future.iloc[idx][type]) \
                                            / np.abs(ts_future.iloc[idx][type])*100,1)
        if type != '7Y-AVG':
            result[type]['RSQ'] = np.round(rsq(ts_future[:idx+1]['eps'], ts_future[:idx+1][type]),3)
        else:
            result[type]['RSQ'] = np.nan
        result[type]['7Y'] = np.round(ts_future.iloc[idx+1:idx+7][type].sum(),3)
        result[type]['15Y'] = np.round(ts_future.iloc[idx+1:idx+15][type].sum(),3)
        result[type]['20Y'] = np.round(ts_future.iloc[idx+1:idx+20][type].sum(),3)

    ts_future.set_index('date_ordinal', inplace = True)

    result_str = json.dumps(result, indent=4)
    # print(result_str)

    # decision tree
    INVESTMENT_TYPE = ''
    INVESTMENT_TYPE_2 = ''
    if result['GROWTH']['Value'] <= 8:
        # all positive eps - straight forward calculation (best)
        INVESTMENT_TYPE = 'GROWTH'
    elif result['GROWTH']['Value'] > 8:
        # all positive eps, >8% - limited to 8% forward calc. on last 3 values (best)
        INVESTMENT_TYPE = 'LAST-8%'
        result[INVESTMENT_TYPE]['Value'] = result['GROWTH']['Value']
    elif result['GROWTH*']['Value'] <= 8:
        # like GROWTH (2nd best)
        INVESTMENT_TYPE = 'GROWTH*'
    elif result['GROWTH*']['Value'] > 8:
        # like LAST-8% (2nd best)
        INVESTMENT_TYPE = 'LAST-8%'
        INVESTMENT_TYPE_2 = '*' # workaround: add '*' to 'LAST-8%' based on 'GROWTH*'
        result[INVESTMENT_TYPE]['Value'] = result['GROWTH*']['Value']
    elif not np.isnan(result['LAST-X%']['Value']):
        # last value with x%
        INVESTMENT_TYPE = 'LAST-X%'
    else:
        # absolute exception, normally going down
        INVESTMENT_TYPE = 'TREND'

    if result['TREND']['20Y'] <= 0:
        result['Risk'] = 1
        HINT = ' - RISK'
    else:
        result['Risk'] = 0
        HINT = ''

    # print(INVESTMENT_TYPE)

    # plot
    if CONFIG[METHOD]["plot_chart"]:
        plt.plot(ts_future['date'], ts_future['eps'], 'k+')
        plt.plot(ts_future['date'], ts_future['GROWTH'], 'g-')
        plt.plot(ts_future['date'], ts_future['GROWTH*'], '*g--')
        plt.plot(ts_future['date'], ts_future['LAST-X%'], 'xr--')
        plt.plot(ts_future['date'], ts_future['LAST-8%'], 'r-')
        plt.plot(ts_future['date'], ts_future['TREND'], 'b-')
        plt.plot(ts_future['date'], ts_future['7Y-AVG'], 'b--')
        plt.xlabel('Time')
        plt.ylabel('Earning Per Share')
        # plt.yscale('symlog')
        plt.ylim([min(ts['eps'])-5, max(ts['eps'])*3])
        plt.title(''+companyName+', '+symbol+', Projection: '+INVESTMENT_TYPE+' / ' \
                    +str(result[INVESTMENT_TYPE]['RSQ'])+HINT+' ' \
                    +dt.datetime.now().strftime('%Y-%m-%d'))
        plt.legend(['RAW', 'GROWTH', 'GROWTH*', 'LAST-X%', 'LAST-8%', 'TREND', '7Y-AVG'])
        plt.grid(True)
        plt.savefig('./plot/'+"".join([x if x.isalnum() else "_" for x in companyName]) \
                    +' '+symbol+' '+dt.datetime.now().strftime('%Y-%m-%d')+'.png')
        # plt.show()
        plt.close()

    ts_future['symbol'] = symbol
    ts_future['created'] = dt.datetime.now().strftime('%Y-%m-%d')
    ts_future = ts_future[['symbol', 'date', 'eps', 'eps*', 'GROWTH', 'GROWTH*', 'LAST-8%', \
                           'LAST-X%', 'TREND', '7Y-AVG', 'created']]
    ts_future = ts_future.rename(columns={'eps*': 'epsStar', 'GROWTH': 'growth', \
                                        'GROWTH*': 'growthStar', 'LAST-8%': 'lastEight', \
                                        'LAST-X%': 'lastX', 'TREND':'trend', \
                                        '7Y-AVG':'sevenYearAvg'})

    try:
        connection_to_target = sql_engine.connect()
        target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target_eps_raw"])
        mysql_db.put_dataframe_to_mysql(connection_to_target, target, ts_future, \
                                    CONFIG[METHOD]["pk_target_eps_raw"], \
                                    update_timestamp = True)
        connection_to_target.close()
    except:
        debug_message = debug_message + 'Could not write raw-data\n'

    WRITE_INVESTMENT_TYPE = INVESTMENT_TYPE + INVESTMENT_TYPE_2 # add '*' to 'LAST-8%'
    dataset = {'symbol': [symbol], 'date': [end_date], \
            'type': [WRITE_INVESTMENT_TYPE], 'risk': [result['Risk']], \
            'rsq': [result[INVESTMENT_TYPE]['RSQ']], 'close': close, \
            'sevenYears': [result[INVESTMENT_TYPE]['7Y']], \
            'fifteenYears': [result[INVESTMENT_TYPE]['15Y']], \
            'twentyYears': [result[INVESTMENT_TYPE]['20Y']], \
            'interest': [result[INVESTMENT_TYPE]['Value']]}
    condensedView = pd.DataFrame(data=dataset)

    # DEBUG
    print(condensedView)

    try:
        connection_to_target = sql_engine.connect()
        target = mysql_db.get_metatable(sql_engine, CONFIG[METHOD]["table_target_eps"])
        mysql_db.put_dataframe_to_mysql(connection_to_target, target, condensedView, \
                                    CONFIG[METHOD]["pk_target_eps"], update_timestamp = True)
        connection_to_target.close()
    except:
        debug_message = debug_message + 'Could not write analyzing-result\n'

# DEBUG print(debug_message)

# log entry and wait

writeLog(CONFIG['file']['log'], 'End'+log_text+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+log_text+' for '\
         +str(CONFIG[METHOD]["delay"])+'s', id = log_id)
time.sleep(CONFIG[METHOD]["delay"])
