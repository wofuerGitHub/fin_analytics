#!/usr/bin/env python

"""
File: correlation.py
Author: Wolfgang Fuerst
Date: 2024-10-06
Description: Calulation of correlation between different assets
Issues:
    ...
Runtime: ...
"""

import time
from mylib import config
from mylib import writeLog
from mylib import mysql_db

# load config file
CONFIG = config.load_config('config.json')["analytics"]

# log entry
log_id = 'COR'
log_text = ' analyzing correlation'
writeLog(CONFIG['file']['log'], 'Start'+log_text+'', id = log_id)

# load data

# calculation

# store data

# log entry
writeLog(CONFIG['file']['log'], 'End'+log_text+'', id = log_id)
writeLog(CONFIG["file"]["log"], 'Wait'+log_text+' for '\
         +str(CONFIG["method"]["correlation"]["delay"])+'s', id = log_id)
time.sleep(CONFIG["method"]["correlation"]["delay"])