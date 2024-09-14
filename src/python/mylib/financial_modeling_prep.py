"""financial modeling prep module"""

#!/usr/bin/python3

from urllib.request import urlopen, HTTPError
import time
import json
import certifi

from mylib.config import getFmgSpeed
from mylib.config import getFileSpeedControl

from mylib.config import getDebug
from mylib.config import getFileDebug

from mylib.writeLog import writeLog

def control_speed():
    """
    transforming the number of queries/time allowed by fmg in some wait time.

    Parameters
    ----------
    none

    Returns
    -------
    none
    """
    set_speed = 1/getFmgSpeed()                 # set allowed queries per minute (e.g. 300 queries per 60 seconds & buffer (set to 90 queries per 60 seconds))
    file = getFileSpeedControl()                # log file for waiting
    with open(file, 'r') as f:                  # read the timestamp, when it is allowed to query
        ts_allowed = float(f.readlines()[-1])
    ts_now = time.time()                        # get the actual timestamp
    if (ts_now < ts_allowed):                   # if it is not allowed to query yet
        time_to_wait = ts_allowed - ts_now      # calculate time_to_wait
        ts_allowed = ts_allowed + set_speed     # calculate the next allowed moment
    else:
        time_to_wait = 0                        # if it is allowed to query, don't wait
        ts_allowed = ts_now + set_speed         # calculate the next allowed moment
    with open(file, 'w') as f:                  # write the timestamp, when it is allowed to query
        f.write(str(ts_allowed))
    print(ts_allowed)
    time.sleep(time_to_wait)                    # sleep if necessary to control speed

def get_jsonparsed_data(url:str):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    try:
        control_speed()                         # wait till it is allowed to execute the query
        if getDebug():
            writeLog(getFileDebug(),url)
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        return json.loads(data)
    except HTTPError as err:
        control_speed()                         # wait in case of error - most time timeout
        print(err)
        return {}

def get_fx_eur(api:str, currency:str, **kwargs):
    """
    Receive the exchange rate to EUR.
    https://site.financialmodelingprep.com/developer/docs/historical-stock-data-free-api/#Historical-Daily-Prices-with-change-and-volume-interval
    https://financialmodelingprep.com/api/v3/historical-price-full/EURUSD?from=2018-03-12&to=2022-06-31&apikey=YOUR_API_KEY

    Parameters
    ----------
    api : str
    currency : str
    startDate : str
    endDate : str

    Returns
    -------
    list
    """
    startDate = kwargs.get('startDate', None)
    endDate = kwargs.get('endDate', None)
    timeseries = str(kwargs.get('timeseries', None))


    url = "https://financialmodelingprep.com/api/v3/historical-price-full/EUR"+currency+"?"
    if startDate:
        url = url+"from="+startDate+"&"
    if endDate:
        url = url+"to="+endDate+"&"
    if timeseries:
        url = url+"timeseries="+timeseries+"&"        
    url = url+"apikey="+api
    data =  get_jsonparsed_data(url)
    try:
        return data['historical']
    except: # pylint: disable=bare-except
        return {}

def get_quote_serie(api:str, symbol:str, **kwargs):
    """
    Receive the quote.
    https://site.financialmodelingprep.com/developer/docs/historical-stock-data-free-api/#Historical-Daily-Prices-with-change-and-volume-interval
    https://financialmodelingprep.com/api/v3/historical-price-full/EURUSD?from=2018-03-12&to=2022-06-31&apikey=YOUR_API_KEY

    Parameters
    ----------
    api : str
    currency : str
    startDate : str
    endDate : str

    Returns
    -------
    list
    """
    startDate = kwargs.get('startDate', None)
    endDate = kwargs.get('endDate', None)
    timeseries = kwargs.get('timeseries', None)

    # url = "https://financialmodelingprep.com/api/v3/historical-price-full/AUS.DE?serietype=line&"

    url = "https://financialmodelingprep.com/api/v3/historical-price-full/"+symbol+"?serietype=line&"
    if startDate:
        url = url+"from="+startDate+"&"
    if endDate:
        url = url+"to="+endDate+"&"
    if timeseries:
        url = url+"timeseries="+timeseries+"&"        
    url = url+"apikey="+api
    print(url)
    data =  get_jsonparsed_data(url)
    try:
        return data['historical']
    except: # pylint: disable=bare-except
        return {}

def get_financial_statement_list(api:str):
    """
    Receive the financial statement list.
    https://site.financialmodelingprep.com/developer/docs#Financial-Statements-List

    Parameters
    ----------
    api : str

    Returns
    -------
    list
    """
    url = "https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey="+api
    return get_jsonparsed_data(url)

def get_symbols_list(api:str, **kwargs):
    """
    Receive the financial statement list.
    https://site.financialmodelingprep.com/developer/docs#Financial-Statements-List

    Parameters
    ----------
    api : str
    type : str

    Returns
    -------
    list
    """
    type = kwargs.get('type', 'stock')
    if type == 'etf':
        url = "https://financialmodelingprep.com/api/v3/etf/list?apikey="+api
    else:
        url = "https://financialmodelingprep.com/api/v3/stock/list?apikey="+api
    return get_jsonparsed_data(url)

def get_company_key_stats(company:str, api:str):
    """
    Receive the company key stats.
    https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api#Python

    Parameters
    ----------
    api : str
    company : str

    Returns
    -------
    dict
    """
    url = "https://financialmodelingprep.com/api/v3/profile/"+company+"?apikey="+api
    return get_jsonparsed_data(url)

def get_income_statement(company:str, api:str):
    """
    Receive the company key stats.
    https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api#Python

    Parameters
    ----------
    api : str
    company : str

    Returns
    -------
    dict
    """
    url = "https://financialmodelingprep.com/api/v3/income-statement/"+company+"?limit=10&apikey="+api
    return get_jsonparsed_data(url)

def get_balance_sheet_statement(company:str, api:str):
    """
    Receive the company key stats.
    https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api#Python

    Parameters
    ----------
    api : str
    company : str

    Returns
    -------
    dict
    """
    url = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+company+"?limit=10&apikey="+api
    return get_jsonparsed_data(url)

def get_cash_flow_statement(company:str, api:str):
    """
    Receive the company key stats.
    https://site.financialmodelingprep.com/developer/docs/companies-key-stats-free-api#Python

    Parameters
    ----------
    api : str
    company : str

    Returns
    -------
    dict
    """
    url = "https://financialmodelingprep.com/api/v3/cash-flow-statement/"+company+"?limit=10&apikey="+api
    return get_jsonparsed_data(url)

def get_quote(api:str, symbol:str):
    """
    Receive the financial statement list.
    https://site.financialmodelingprep.com/developer/docs#Financial-Statements-List

    Parameters
    ----------
    api : str

    Returns
    -------
    list
    """
    url = "https://financialmodelingprep.com/api/v3/quote/"+symbol+"?apikey="+api
    return get_jsonparsed_data(url)[0]
# print(get_company_key_stats('aapl', 'API_KEY'))

# print(get_fx_eur('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'USD', startDate = '2022-06-20'))
# https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
