"""config module"""

#!/usr/bin/python3

""" {
    "database": {
      "host": "127.0.0.1",
      "schema": "fmg",
      "user": "fmg",
      "password": "fmg"
    },
    "fmg": {
      "apiKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "speed": 1
    },
    "file": {
      "log": "./fin_suite4.log",
      "debug": "./fin_suite4_debug.log",
      "speedControl": "./fmg_speed.ctl"
    },
    "debug":true
  } """

import json

def load_config(file = "config.json"):
    with open(file, "r") as f:
        config = json.load(f)
    return config['analytics']

def getDatabaseHost():
    config = load_config()
    return config['database']['host']

def getDatabasePort():
    config = load_config()
    return config['database']['port']

def getDatabaseSchema():
    config = load_config()
    return config['database']['schema']

def getDatabaseUser():
    config = load_config()
    return config['database']['user']

def getDatabasePassword():
    config = load_config()
    return config['database']['password']

# ---

def getFmgApiKey():
    config = load_config()
    return config['fmg']['apiKey']

def getFmgSpeed():
    config = load_config()
    return config['fmg']['speed']

# ---

def getFileLog():
    config = load_config()
    return config['file']['log']

def getFileDebug():
    config = load_config()
    return config['file']['debug']

def getFileSpeedControl():
    config = load_config()
    return config['file']['speedControl']

# ---

def getDebug():
    config = load_config()
    return config['debug']